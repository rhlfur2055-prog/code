from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
from ultralytics import YOLO
import PIL.Image

# Pillow 10.x 호환성 패치
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

import easyocr
import os
import re

app = Flask(__name__)
CORS(app)

# YOLO 모델 로드
model = YOLO('yolov8n.pt')

# [v3.0] EasyOCR Reader 초기화 (한국어, 영어) - Allowlist 확장 (영문 포함)
print("📚 EasyOCR 모델 로딩 중... (v3.0 Low-Light + Foreign Support)")
# 허용 문자 목록 정의 (영문 대문자 추가)
VALID_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ가나다라마거너더러머버서어저고노도로모보소오조구누두루무부수우주아바사자하허호배"
reader = easyocr.Reader(['ko', 'en'], gpu=False)
print("✅ EasyOCR 모델 로드 완료")

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'status': 'running',
        'version': '2.8',
        'message': 'License Plate Recognition API Server (Multi-Pass v2.8 + ValidChars)',
        'endpoints': {
            'health': '/health',
            'recognize': '/api/parking/recognize (POST)'
        }
    })

def preprocess_base(img):
    """
    기본 전처리 파이프라인
    """
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
        
    # 노이즈 제거 (Gaussian Blur)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # CLAHE (대비 강화)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    enhanced = clahe.apply(blurred)
    
    # Adaptive Threshold (이진화)
    binary = cv2.adaptiveThreshold(
        enhanced, 
        255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 
        11, 
        2
    )
    
    # Median Blur (소금-후추 노이즈 제거)
    denoised_binary = cv2.medianBlur(binary, 3)
    
    return denoised_binary

def preprocess_variants(img):
    """
    [v2.6] 다양한 전처리 변형 생성 (Multi-Pass)
    """
    variants = []
    
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
        
    # 1. 기본 전처리
    variants.append(preprocess_base(img))
    
    # 2. 원본 그레이스케일
    variants.append(gray)
    
    # 3. 반전 (Invert) - 흰색 글자/검은 배경 대응
    variants.append(cv2.bitwise_not(gray))
    
    # 4. 선명화 (Sharpening)
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpened = cv2.filter2D(gray, -1, kernel)
    variants.append(sharpened)
    
    # 5. [v3.0] 감마 보정 (Gamma Correction) - 저조도 대응
    # 어두운 영역을 밝게 (Gamma < 1.0)
    gamma = 0.4
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    gamma_corrected = cv2.LUT(gray, table)
    variants.append(gamma_corrected)
    
    # 6. [v3.1] High Contrast (CLAHE + Threshold) - 야간 번호판 강조
    clahe_strong = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8,8))
    contrast_enhanced = clahe_strong.apply(gray)
    _, high_contrast_binary = cv2.threshold(contrast_enhanced, 150, 255, cv2.THRESH_BINARY)
    variants.append(high_contrast_binary)

    return variants

def filter_and_merge_text(results):
    """
    [v2.5] OCR 결과 필터링 및 스마트 병합
    - 수직(Y축)으로 멀리 떨어진 노이즈 제거
    - 수평(X축)으로 정렬하여 병합
    """
    if not results:
        return []

    # results structure: ([[x1,y1],[x2,y2],[x3,y3],[x4,y4]], text, conf)
    
    # 1. 박스 중심 좌표 계산
    boxes = []
    for (bbox, text, conf) in results:
        (tl, tr, br, bl) = bbox
        center_y = int((tl[1] + br[1]) / 2)
        center_x = int((tl[0] + br[0]) / 2)
        height = int(bl[1] - tl[1])
        boxes.append({
            'text': text,
            'conf': conf,
            'center_y': center_y,
            'center_x': center_x,
            'height': height,
            'bbox': bbox
        })

    # 2. 메인 텍스트 라인 찾기 (가장 신뢰도가 높거나 글자가 많은 라인)
    if not boxes:
        return []

    # 전체 박스의 Median Y 계산
    ys = [b['center_y'] for b in boxes]
    median_y = sorted(ys)[len(ys)//2]
    
    # 평균 높이 계산
    hs = [b['height'] for b in boxes]
    avg_h = sum(hs) / len(hs)
    
    # 3. Y축 기준 필터링 (Median Y에서 높이의 1.5배 이상 벗어나면 노이즈로 간주)
    valid_boxes = []
    threshold_y = max(avg_h * 1.5, 20) # 최소 20px 여유
    
    for b in boxes:
        if abs(b['center_y'] - median_y) < threshold_y:
            valid_boxes.append(b)
        else:
            print(f"🗑️ [DEBUG] Discarding vertical noise: {b['text']} (diff: {abs(b['center_y'] - median_y)})")

    # 4. X축 정렬
    valid_boxes.sort(key=lambda x: x['center_x'])
    
    # 5. 병합
    merged_candidates = []
    
    # Option A: 공백 없이 병합
    text_nospace = "".join([b['text'] for b in valid_boxes])
    avg_conf = sum([b['conf'] for b in valid_boxes]) / len(valid_boxes) if valid_boxes else 0
    merged_candidates.append((None, text_nospace, avg_conf))
    
    # Option B: 공백 포함 병합
    text_space = " ".join([b['text'] for b in valid_boxes])
    merged_candidates.append((None, text_space, avg_conf))
    
    return merged_candidates

def recognize_text(img_roi):
    """
    단일 이미지 영역에 대해 OCR 수행 (Multi-Pass)
    """
    # [v2.8] 다양한 전처리 이미지 시도
    images_to_try = preprocess_variants(img_roi)
        
    configs = [
        {
            'detail': 1,
            'text_threshold': 0.3,
            'low_text': 0.3,
            'link_threshold': 0.3,
            'mag_ratio': 1.5,
            'allowlist': VALID_CHARS  # [v2.8] 허용 문자만 인식
        },
        {
            'detail': 1,
            'mag_ratio': 2.0,
            'text_threshold': 0.3,
            'contrast_ths': 0.3, 
            'adjust_contrast': 0.8,
            'allowlist': VALID_CHARS  # [v2.8] 허용 문자만 인식
        }
    ]
    
    final_results = []
    
    for img in images_to_try:
        for config in configs:
            try:
                raw_res = reader.readtext(img, **config)
                if raw_res:
                    # [v2.5] 스마트 병합 로직 적용
                    merged = filter_and_merge_text(raw_res)
                    final_results.extend(merged)
            except Exception:
                pass
            
    return final_results

def correct_chars(text):
    """
    [v2.8] 오인식 문자 교정 (번호판 특화)
    """
    corrections = {
        'O': '0', 'o': '0', 'Q': '0', 'D': '0',
        'I': '1', 'l': '1', '|': '1', 'i': '1',
        'Z': '2', 'z': '2',
        'A': '4',
        'S': '5', 's': '5',
        'G': '6',
        'B': '8',
        'U': '0',
        # [v2.8] 자주 발생하는 오인식 추가 (밥 -> 바)
        '밥': '바', '박': '바', '반': '바',
        '차': '자', # 차 -> 자 (번호판에 '차'는 없음)
        '가': '가', '나': '나', '다': '다', '라': '라', '마': '마',
        '거': '거', '너': '너', '더': '더', '러': '러', '머': '머', '버': '버', '서': '서', '어': '어', '저': '저',
        '고': '고', '노': '노', '도': '도', '로': '로', '모': '모', '보': '보', '소': '소', '오': '오', '조': '조',
        '구': '구', '누': '누', '두': '두', '루': '루', '무': '무', '부': '부', '수': '수', '우': '우', '주': '주',
        '아': '아', '바': '바', '사': '사', '자': '자', '배': '배',
        '하': '하', '허': '허', '호': '호'
    }
    
    # 받침 제거 로직 (번호판은 받침이 거의 없음)
    # 유니코드: 가(0xAC00) ~ 힣(0xD7A3)
    # 초성: ((code - 0xAC00) / 28) / 21
    # 중성: ((code - 0xAC00) / 28) % 21
    # 종성: (code - 0xAC00) % 28
    # 종성이 0이면 받침 없음
    
    corrected = ""
    for char in text:
        # 1. 매핑 테이블 확인
        if char in corrections:
            corrected += corrections[char]
            continue
            
        # 2. 한글 받침 제거 시도
        if '가' <= char <= '힣':
            code = ord(char) - 0xAC00
            jongseong = code % 28
            if jongseong != 0:
                # 받침이 있는 경우, 받침 제거한 문자로 변환
                new_code = code - jongseong
                new_char = chr(new_code + 0xAC00)
                # 제거한 문자가 유효한지 확인? (일단 변환)
                corrected += new_char
            else:
                corrected += char
        else:
            corrected += corrections.get(char, char)
            
    return corrected

def clean_and_validate(text, conf):
    """
    [v2.9] 텍스트 정제 및 검증 강화 (Garbage Filter + Structure Correction)
    """
    if not text:
        return None, 0.0

    # [v3.0] 문자 교정 (영문 포함 시 주의)
    # text = correct_chars(text) # 영문 번호판 오인식 방지를 위해 일단 주석 처리 or 로직 개선 필요
    # 여기서는 한글/숫자 위주의 오타 수정만 적용하고, 영문은 건드리지 않도록 조건부 적용
    
    is_foreign = bool(re.search(r'[A-Z]', text))
    if not is_foreign:
        text = correct_chars(text)

    # 1. 기본 정제 (영문 대문자 추가 허용)
    clean = re.sub(r'[^0-9가-힣A-Z]', '', text)
    
    # [v2.9] 구조 기반 노이즈 제거 (Heuristic Structure Correction)
    # 한국 번호판: [숫자들][한글][숫자4자리]
    match = re.search(r'([0-9]+)([가-힣])([0-9]+)', clean)
    if match:
        prefix, hangul, suffix = match.groups()
        
        # Suffix Correction (뒷번호는 무조건 4자리여야 함)
        if len(suffix) > 4:
            # 1. 앞뒤에 '1'이 있는지 확인하고 제거 시도 (볼트/프레임 오인식)
            temp_suffix = suffix
            while len(temp_suffix) > 4 and temp_suffix.startswith('1'):
                temp_suffix = temp_suffix[1:]
            
            # 앞에서 제거했는데도 길면, 뒤에서 제거 시도
            if len(temp_suffix) > 4:
                temp_suffix = suffix # 리셋
                while len(temp_suffix) > 4 and temp_suffix.endswith('1'):
                    temp_suffix = temp_suffix[:-1]
            
            # 앞/뒤 중 하나만 제거해서 4자리가 되면 채택
            if len(suffix) > 4:
                while len(suffix) > 4 and suffix.startswith('1'):
                    suffix = suffix[1:]
                while len(suffix) > 4 and suffix.endswith('1'):
                    suffix = suffix[:-1]
        
        # Prefix Correction (앞번호는 2~3자리)
        if len(prefix) > 3:
             while len(prefix) > 3 and prefix.startswith('1'):
                prefix = prefix[1:]
             while len(prefix) > 3 and prefix.endswith('1'):
                prefix = prefix[:-1]

        # 재조립
        clean = f"{prefix}{hangul}{suffix}"

    digit_count = len(re.findall(r'\d', clean))
    hangul_count = len(re.findall(r'[가-힣]', clean))
    alpha_count = len(re.findall(r'[A-Z]', clean)) # [v3.0] 영문 개수
    total_len = len(clean)
    
    # 2. 길이 및 구조 필터링
    if total_len < 3 or total_len > 10:
        return None, 0.0
        
    score = conf
    
    # 3. 정규식 패턴 검사 (엄격 -> 완화 순)
    pattern_new = re.compile(r'^(\d{3})[가-힣](\d{4})$')
    pattern_old = re.compile(r'^(\d{2})[가-힣](\d{4})$')
    pattern_local = re.compile(r'^[가-힣]{2}(\d{2})[가-힣](\d{4})$')
    # [v3.0] 해외/영문 번호판 패턴 (예: VED 4147 -> VED4147)
    pattern_foreign = re.compile(r'^[A-Z]{1,3}\d{1,4}$') 
    
    if pattern_new.match(clean):
        score += 2.0 
    elif pattern_old.match(clean):
        score += 2.0
    elif pattern_local.match(clean):
        score += 2.0
    elif pattern_foreign.match(clean): # [v3.0]
        score += 1.5
    elif hangul_count == 1 and digit_count >= 3:
        score += 0.5
    elif alpha_count > 0 and digit_count > 0: # [v3.0] 영문+숫자 조합
        score += 1.0
    else:
        # [v3.0] 한글이 없어도 영문이 있으면 허용
        if hangul_count == 0 and alpha_count == 0:
            return None, 0.0 
        score -= 0.5
        
    return clean, score

@app.route('/api/parking/recognize', methods=['POST'])
def recognize_plate():
    try:
        if 'image' not in request.files:
            return jsonify({'error': '이미지가 없습니다'}), 400
        
        file = request.files['image']
        img_array = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        
        # 1. YOLO로 차량 감지
        results = model(img)
        
        detected_plates = []
        best_plate = None
        best_score = 0.0
        
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                
                # [v2.5] Padding 유지 (30%)
                h, w, _ = img.shape
                pad_x = int((x2 - x1) * 0.30) 
                pad_y = int((y2 - y1) * 0.30) 
                
                crop_y1 = max(0, int(y1) - pad_y)
                crop_y2 = min(h, int(y2) + pad_y)
                crop_x1 = max(0, int(x1) - pad_x)
                crop_x2 = min(w, int(x2) + pad_x)
                
                plate_img = img[crop_y1:crop_y2, crop_x1:crop_x2]
                
                ocr_results = recognize_text(plate_img)
                
                for (_, text, conf) in ocr_results:
                    clean, score = clean_and_validate(text, conf)
                    if clean and score > 0.5: # 최소 점수 기준
                        if score > best_score:
                            best_plate = clean
                            best_score = score
                        
                        detected_plates.append({
                            'plate_number': clean,
                            'confidence': float(box.conf[0]),
                            'ocr_confidence': float(conf),
                            'score': score, 
                            'position': {'x1':int(x1), 'y1':int(y1), 'x2':int(x2), 'y2':int(y2)}
                        })

        # 2. Fallback: 리사이즈 스캔
        if not detected_plates or best_score < 1.0:
            print("⚠️ [DEBUG] Trying resize scan...")
            h, w = img.shape[:2]
            ratio = 1024 / w
            resized = cv2.resize(img, (1024, int(h * ratio)))
            ocr_results = recognize_text(resized)

            for (_, text, conf) in ocr_results:
                clean, score = clean_and_validate(text, conf)
                if clean and score > best_score:
                    best_plate = clean
                    best_score = score
                    detected_plates.append({
                        'plate_number': clean,
                        'confidence': 0.0,
                        'ocr_confidence': float(conf),
                        'score': score,
                        'position': {'x1':0, 'y1':0, 'x2':0, 'y2':0}
                    })

        detected_plates.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        unique_plates = []
        seen = set()
        for p in detected_plates:
            if p['plate_number'] not in seen:
                unique_plates.append(p)
                seen.add(p['plate_number'])

        return jsonify({
            'success': True,
            'count': len(unique_plates),
            'plates': unique_plates,
            'message': '인식 완료'
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK', 'service': 'License Plate Recognition v3.0 (Low-Light + Foreign)'})

if __name__ == '__main__':
    print('🚗 번호판 인식 서버 v3.0 (Low-Light + Foreign) 시작!')
    app.run(host='0.0.0.0', port=5000, debug=False)
