"""
K-MaaS FastAPI AI Server
- 번호판 인식 (YOLO + OCR)
- 객체 탐지 (YOLO)
- 음성 인식 (Whisper)
- 배경 제거

Spring Boot와 연동되는 AI 처리 서버
"""
from fastapi import FastAPI, UploadFile, File, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional
import io
import base64
import tempfile
import os
import time
import logging
import uuid

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(name)s] %(message)s'
)
logger = logging.getLogger("ai-server")

app = FastAPI(
    title="K-MaaS AI Server",
    description="번호판 인식, 객체 탐지, 음성 인식 API",
    version="2.0.0"
)

# CORS 설정 (Spring Boot 연동용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== 모델 관리 ====================

# 모델 로딩 (지연 로딩)
yolo_model = None
whisper_model = None
ocr_reader = None

def get_yolo_model():
    """YOLO 모델 로드 (싱글톤)"""
    global yolo_model
    if yolo_model is None:
        logger.info("YOLO 모델 로딩 중...")
        from ultralytics import YOLO
        yolo_model = YOLO("yolov8n.pt")
        logger.info("YOLO 모델 로딩 완료")
    return yolo_model

def get_whisper_model():
    """Whisper 모델 로드 (싱글톤)"""
    global whisper_model
    if whisper_model is None:
        logger.info("Whisper 모델 로딩 중...")
        import whisper
        whisper_model = whisper.load_model("base")
        logger.info("Whisper 모델 로딩 완료")
    return whisper_model

def get_ocr_reader():
    """EasyOCR 리더 로드 (싱글톤)"""
    global ocr_reader
    if ocr_reader is None:
        logger.info("OCR 리더 로딩 중...")
        import easyocr
        ocr_reader = easyocr.Reader(['ko', 'en'])
        logger.info("OCR 리더 로딩 완료")
    return ocr_reader


# ==================== Pydantic 모델 (Spring DTO와 매핑) ====================

class BoundingBox(BaseModel):
    """번호판 영역 좌표"""
    x: int
    y: int
    width: int
    height: int

class PlateInfo(BaseModel):
    """개별 번호판 정보"""
    plate_number: str = Field(..., description="인식된 번호판 번호")
    confidence: float = Field(..., ge=0, le=1, description="인식 신뢰도")
    bounding_box: BoundingBox

class LicensePlateResponse(BaseModel):
    """
    번호판 인식 응답 모델
    Spring Boot의 LicensePlateResponse.java와 1:1 매핑
    """
    success: bool
    request_id: Optional[str] = None
    plate_number: Optional[str] = Field(None, description="대표 번호판 번호")
    confidence: Optional[float] = Field(None, ge=0, le=1)
    bounding_box: Optional[BoundingBox] = None
    vehicle_type: Optional[str] = None
    processing_time_ms: Optional[int] = None
    plates: Optional[List[PlateInfo]] = Field(default=[], description="탐지된 모든 번호판")
    error_message: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "request_id": "550e8400-e29b-41d4-a716-446655440000",
                "plate_number": "12가3456",
                "confidence": 0.95,
                "bounding_box": {"x": 100, "y": 200, "width": 150, "height": 50},
                "vehicle_type": "승용차",
                "processing_time_ms": 234,
                "plates": []
            }
        }

class Detection(BaseModel):
    """객체 탐지 결과"""
    class_name: str
    confidence: float
    bbox: List[float]

class DetectionResponse(BaseModel):
    """객체 탐지 응답"""
    success: bool
    detections: List[Detection]
    count: int

class TranscriptionResponse(BaseModel):
    """음성 인식 응답"""
    success: bool
    text: str
    language: Optional[str] = None


class TextAnalysisRequest(BaseModel):
    """텍스트 분석 요청"""
    text: str = Field(..., min_length=1, max_length=10000, description="분석할 텍스트")


class SentimentResult(BaseModel):
    """감성 분석 결과"""
    label: str = Field(..., description="감성 레이블 (positive/negative/neutral)")
    score: float = Field(..., ge=0, le=1, description="신뢰도 점수")
    details: Optional[dict] = None


class SentimentResponse(BaseModel):
    """감성 분석 응답"""
    success: bool
    sentiment: Optional[SentimentResult] = None
    processing_time_ms: Optional[int] = None
    error_message: Optional[str] = None


class KeywordsResponse(BaseModel):
    """키워드 추출 응답"""
    success: bool
    keywords: List[dict] = Field(default=[], description="추출된 키워드 목록")
    processing_time_ms: Optional[int] = None
    error_message: Optional[str] = None


class ChatRequest(BaseModel):
    """ChatGPT 요청"""
    message: str = Field(..., min_length=1, max_length=5000, description="사용자 메시지")
    system_prompt: Optional[str] = Field(None, description="시스템 프롬프트")
    max_tokens: Optional[int] = Field(500, ge=1, le=4000, description="최대 토큰 수")
    temperature: Optional[float] = Field(0.7, ge=0, le=2, description="창의성 수준")


class ChatResponse(BaseModel):
    """ChatGPT 응답"""
    success: bool
    response: Optional[str] = None
    model: Optional[str] = None
    usage: Optional[dict] = None
    error_message: Optional[str] = None


class SummaryRequest(BaseModel):
    """텍스트 요약 요청"""
    text: str = Field(..., min_length=50, max_length=50000, description="요약할 텍스트")
    max_length: Optional[int] = Field(150, ge=50, le=500, description="요약 최대 길이")


class SummaryResponse(BaseModel):
    """텍스트 요약 응답"""
    success: bool
    summary: Optional[str] = None
    original_length: Optional[int] = None
    summary_length: Optional[int] = None
    processing_time_ms: Optional[int] = None
    error_message: Optional[str] = None


# ==================== 헬스체크 ====================

@app.get("/")
def root():
    """서버 상태 확인"""
    return {"status": "ok", "message": "K-MaaS AI Server Running", "version": "2.0.0"}

@app.get("/health")
def health():
    """헬스체크 엔드포인트"""
    return {"status": "healthy", "service": "ai-server"}


# ==================== 🚗 번호판 인식 API (K-MaaS 핵심) ====================

@app.post("/api/v1/license-plate/detect", response_model=LicensePlateResponse)
async def detect_license_plate(
    file: UploadFile = File(..., description="차량 이미지"),
    x_request_id: Optional[str] = Header(None, alias="X-Request-ID")
):
    """
    🚗 K-MaaS 번호판 인식 API

    - YOLO로 번호판 영역 탐지
    - EasyOCR로 번호판 텍스트 인식
    - Spring Boot의 AiService.detectLicensePlate()에서 호출

    Returns:
        LicensePlateResponse: 번호판 인식 결과
    """
    start_time = time.time()
    request_id = x_request_id or str(uuid.uuid4())

    logger.info(f"[{request_id}] 번호판 인식 요청 - 파일: {file.filename}")

    try:
        from PIL import Image
        import numpy as np

        # 1. 이미지 로드
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        image_np = np.array(image)

        # 2. YOLO로 객체 탐지 (번호판 또는 차량)
        model = get_yolo_model()
        results = model(image)

        plates = []
        main_plate = None
        main_confidence = 0

        # 3. 탐지된 객체에서 번호판 영역 추출
        for r in results:
            for box in r.boxes:
                class_name = r.names[int(box.cls)]
                confidence = float(box.conf)

                # 차량 또는 번호판 클래스인 경우
                if class_name in ['car', 'truck', 'bus', 'motorcycle', 'license_plate']:
                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

                    # 번호판 영역 크롭 (차량 하단 30% 영역을 번호판으로 가정)
                    if class_name != 'license_plate':
                        plate_y1 = y1 + int((y2 - y1) * 0.7)
                        plate_region = image_np[plate_y1:y2, x1:x2]
                    else:
                        plate_region = image_np[y1:y2, x1:x2]

                    # 4. OCR로 번호판 텍스트 인식
                    if plate_region.size > 0:
                        try:
                            reader = get_ocr_reader()
                            ocr_results = reader.readtext(plate_region)

                            if ocr_results:
                                # OCR 결과 조합
                                plate_text = ''.join([text for _, text, _ in ocr_results])
                                # 한국 번호판 형식으로 정규화 (간단 버전)
                                plate_text = plate_text.replace(' ', '').upper()

                                plate_info = PlateInfo(
                                    plate_number=plate_text,
                                    confidence=confidence,
                                    bounding_box=BoundingBox(
                                        x=x1, y=y1,
                                        width=x2-x1, height=y2-y1
                                    )
                                )
                                plates.append(plate_info)

                                # 가장 신뢰도 높은 것을 대표로
                                if confidence > main_confidence:
                                    main_confidence = confidence
                                    main_plate = plate_info

                        except Exception as ocr_err:
                            logger.warning(f"[{request_id}] OCR 실패: {ocr_err}")

        processing_time = int((time.time() - start_time) * 1000)

        if main_plate:
            logger.info(f"[{request_id}] 번호판 인식 성공 - {main_plate.plate_number} ({processing_time}ms)")
            return LicensePlateResponse(
                success=True,
                request_id=request_id,
                plate_number=main_plate.plate_number,
                confidence=main_plate.confidence,
                bounding_box=main_plate.bounding_box,
                vehicle_type="승용차",  # TODO: 실제 분류 로직 추가
                processing_time_ms=processing_time,
                plates=plates
            )
        else:
            logger.warning(f"[{request_id}] 번호판 탐지 실패 ({processing_time}ms)")
            return LicensePlateResponse(
                success=False,
                request_id=request_id,
                processing_time_ms=processing_time,
                error_message="번호판을 찾을 수 없습니다"
            )

    except Exception as e:
        processing_time = int((time.time() - start_time) * 1000)
        logger.error(f"[{request_id}] 처리 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== 📝 텍스트 분석 API ====================

@app.post("/api/v1/text/sentiment", response_model=SentimentResponse)
async def analyze_sentiment(request: TextAnalysisRequest):
    """
    📝 감성 분석 API

    텍스트의 감성을 분석하여 긍정/부정/중립을 판단합니다.

    Returns:
        SentimentResponse: 감성 분석 결과
    """
    start_time = time.time()
    logger.info(f"감성 분석 요청 - 텍스트 길이: {len(request.text)}")

    try:
        # 간단한 키워드 기반 감성 분석 (실제 프로덕션에서는 ML 모델 사용)
        positive_words = ['좋아', '훌륭', '최고', '감사', '행복', '사랑', 'good', 'great', 'excellent', 'happy', 'love', 'amazing', 'wonderful']
        negative_words = ['싫어', '나쁜', '최악', '짜증', '화나', '슬퍼', 'bad', 'terrible', 'awful', 'hate', 'angry', 'sad', 'horrible']

        text_lower = request.text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)

        total = positive_count + negative_count
        if total == 0:
            label = "neutral"
            score = 0.5
        elif positive_count > negative_count:
            label = "positive"
            score = positive_count / total
        else:
            label = "negative"
            score = negative_count / total

        processing_time = int((time.time() - start_time) * 1000)

        return SentimentResponse(
            success=True,
            sentiment=SentimentResult(
                label=label,
                score=score,
                details={
                    "positive_indicators": positive_count,
                    "negative_indicators": negative_count,
                    "text_length": len(request.text)
                }
            ),
            processing_time_ms=processing_time
        )

    except Exception as e:
        logger.error(f"감성 분석 오류: {str(e)}")
        return SentimentResponse(
            success=False,
            error_message=str(e)
        )


@app.post("/api/v1/text/keywords", response_model=KeywordsResponse)
async def extract_keywords(request: TextAnalysisRequest):
    """
    🔑 키워드 추출 API

    텍스트에서 주요 키워드를 추출합니다.

    Returns:
        KeywordsResponse: 추출된 키워드 목록
    """
    start_time = time.time()
    logger.info(f"키워드 추출 요청 - 텍스트 길이: {len(request.text)}")

    try:
        import re
        from collections import Counter

        # 불용어 (한국어 + 영어)
        stopwords = {
            '이', '그', '저', '것', '수', '등', '들', '및', '에', '의', '을', '를',
            '이다', '하다', '있다', '되다', '않다', '없다', '같다', '보다', '위해',
            'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'to', 'of', 'in', 'for',
            'on', 'with', 'at', 'by', 'from', 'as', 'into', 'through', 'during',
            'and', 'or', 'but', 'if', 'then', 'else', 'when', 'up', 'down', 'out',
            'it', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'they', 'we'
        }

        # 단어 추출 (한글 + 영문)
        words = re.findall(r'[가-힣]{2,}|[a-zA-Z]{3,}', request.text.lower())

        # 불용어 제거 및 빈도 계산
        filtered_words = [w for w in words if w not in stopwords]
        word_counts = Counter(filtered_words)

        # 상위 10개 키워드 추출
        top_keywords = word_counts.most_common(10)

        keywords = [
            {"word": word, "count": count, "score": count / len(filtered_words) if filtered_words else 0}
            for word, count in top_keywords
        ]

        processing_time = int((time.time() - start_time) * 1000)

        return KeywordsResponse(
            success=True,
            keywords=keywords,
            processing_time_ms=processing_time
        )

    except Exception as e:
        logger.error(f"키워드 추출 오류: {str(e)}")
        return KeywordsResponse(
            success=False,
            error_message=str(e)
        )


@app.post("/api/v1/text/summary", response_model=SummaryResponse)
async def summarize_text(request: SummaryRequest):
    """
    📋 텍스트 요약 API

    긴 텍스트를 짧게 요약합니다.

    Returns:
        SummaryResponse: 요약된 텍스트
    """
    start_time = time.time()
    logger.info(f"텍스트 요약 요청 - 원문 길이: {len(request.text)}")

    try:
        # 간단한 추출적 요약 (문장 단위)
        import re

        # 문장 분리
        sentences = re.split(r'[.!?。]\s*', request.text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]

        if not sentences:
            return SummaryResponse(
                success=False,
                error_message="요약할 충분한 문장이 없습니다."
            )

        # 문장 점수 계산 (단어 빈도 기반)
        words = re.findall(r'[가-힣]+|[a-zA-Z]+', request.text.lower())
        word_freq = Counter(words)

        sentence_scores = []
        for sentence in sentences:
            sent_words = re.findall(r'[가-힣]+|[a-zA-Z]+', sentence.lower())
            score = sum(word_freq.get(w, 0) for w in sent_words) / (len(sent_words) + 1)
            sentence_scores.append((sentence, score))

        # 상위 문장 선택
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        target_length = request.max_length
        summary_sentences = []
        current_length = 0

        for sentence, _ in sentence_scores:
            if current_length + len(sentence) <= target_length:
                summary_sentences.append(sentence)
                current_length += len(sentence)

        # 원래 순서대로 정렬
        summary_sentences = sorted(
            summary_sentences,
            key=lambda s: sentences.index(s) if s in sentences else 0
        )

        summary = '. '.join(summary_sentences)
        if summary and not summary.endswith('.'):
            summary += '.'

        processing_time = int((time.time() - start_time) * 1000)

        return SummaryResponse(
            success=True,
            summary=summary,
            original_length=len(request.text),
            summary_length=len(summary),
            processing_time_ms=processing_time
        )

    except Exception as e:
        logger.error(f"텍스트 요약 오류: {str(e)}")
        return SummaryResponse(
            success=False,
            error_message=str(e)
        )


@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    """
    🤖 ChatGPT 연동 API

    OpenAI GPT 모델을 사용하여 대화합니다.
    OPENAI_API_KEY 환경 변수가 필요합니다.

    Returns:
        ChatResponse: AI 응답
    """
    logger.info(f"ChatGPT 요청 - 메시지 길이: {len(request.message)}")

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key or api_key == "sk-your-openai-api-key-here":
        # OpenAI API 키가 없으면 간단한 에코 응답
        logger.warning("OpenAI API 키가 설정되지 않음 - 에코 모드")
        return ChatResponse(
            success=True,
            response=f"[에코 모드] 입력하신 메시지: {request.message}\n\n(OPENAI_API_KEY를 설정하면 실제 GPT 응답을 받을 수 있습니다)",
            model="echo-mode"
        )

    try:
        import httpx

        async with httpx.AsyncClient() as client:
            messages = []

            if request.system_prompt:
                messages.append({"role": "system", "content": request.system_prompt})
            else:
                messages.append({"role": "system", "content": "You are a helpful assistant."})

            messages.append({"role": "user", "content": request.message})

            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": messages,
                    "max_tokens": request.max_tokens,
                    "temperature": request.temperature
                },
                timeout=30.0
            )

            if response.status_code != 200:
                error_data = response.json()
                raise Exception(f"OpenAI API 오류: {error_data.get('error', {}).get('message', 'Unknown error')}")

            data = response.json()

            return ChatResponse(
                success=True,
                response=data["choices"][0]["message"]["content"],
                model=data["model"],
                usage=data.get("usage")
            )

    except Exception as e:
        logger.error(f"ChatGPT 오류: {str(e)}")
        return ChatResponse(
            success=False,
            error_message=str(e)
        )


# ==================== 기존 API (호환성 유지) ====================

@app.post("/detect", response_model=DetectionResponse)
async def detect_objects(file: UploadFile = File(...)):
    """YOLO 객체 탐지 API"""
    try:
        from PIL import Image

        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        model = get_yolo_model()
        results = model(image)

        detections = []
        for r in results:
            for box in r.boxes:
                detections.append(Detection(
                    class_name=r.names[int(box.cls)],
                    confidence=float(box.conf),
                    bbox=box.xyxy[0].tolist()
                ))

        return DetectionResponse(
            success=True,
            detections=detections,
            count=len(detections)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(file: UploadFile = File(...)):
    """Whisper 음성 인식 API"""
    try:
        contents = await file.read()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(contents)
            tmp_path = tmp.name

        try:
            model = get_whisper_model()
            result = model.transcribe(tmp_path)

            return TranscriptionResponse(
                success=True,
                text=result["text"],
                language=result.get("language")
            )
        finally:
            os.unlink(tmp_path)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/remove-background")
async def remove_background(file: UploadFile = File(...)):
    """배경 제거 API"""
    try:
        from rembg import remove

        contents = await file.read()
        output = remove(contents)

        return JSONResponse({
            "success": True,
            "image": base64.b64encode(output).decode("utf-8")
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/caption")
async def image_caption(file: UploadFile = File(...)):
    """이미지 캡션 생성 API"""
    try:
        from transformers import BlipProcessor, BlipForConditionalGeneration
        from PIL import Image

        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

        inputs = processor(image, return_tensors="pt")
        output = model.generate(**inputs, max_length=50)
        caption = processor.decode(output[0], skip_special_tokens=True)

        return {"success": True, "caption": caption}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== 서버 실행 ====================

if __name__ == "__main__":
    import uvicorn
    logger.info("K-MaaS AI Server 시작...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
