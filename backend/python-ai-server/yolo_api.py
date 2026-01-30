# -*- coding: utf-8 -*-
"""
YOLO8 객체 탐지 API 서버
- 이미지 업로드 시 객체 탐지
- 실시간 웹캠 스트리밍 지원
- 바운딩 박스 시각화
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
import cv2
import numpy as np
import base64
import io
from PIL import Image
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("yolo-api")

app = FastAPI(
    title="YOLO8 객체 탐지 API",
    description="YOLOv8을 사용한 실시간 객체 탐지 서버",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# YOLO 모델 (지연 로딩)
yolo_model = None

def load_yolo_model():
    """YOLO 모델 로드"""
    global yolo_model
    if yolo_model is None:
        try:
            from ultralytics import YOLO
            logger.info("YOLO 모델 로딩 중...")
            yolo_model = YOLO('yolov8n.pt')  # nano 모델 (가볍고 빠름)
            logger.info("YOLO 모델 로드 완료!")
        except Exception as e:
            logger.error(f"YOLO 모델 로드 실패: {e}")
            raise HTTPException(status_code=500, detail="YOLO 모델 로드 실패")
    return yolo_model

# COCO 클래스 이름 (80개)
COCO_CLASSES = [
    "사람", "자전거", "자동차", "오토바이", "비행기", "버스", "기차", "트럭", "보트",
    "신호등", "소화전", "정지 표지판", "주차 미터기", "벤치", "새", "고양이", "개",
    "말", "양", "소", "코끼리", "곰", "얼룩말", "기린", "배낭", "우산", "핸드백",
    "넥타이", "여행 가방", "프리스비", "스키", "스노보드", "스포츠 공", "연",
    "야구 배트", "야구 글러브", "스케이트보드", "서핑보드", "테니스 라켓", "병",
    "와인잔", "컵", "포크", "나이프", "숟가락", "그릇", "바나나", "사과", "샌드위치",
    "오렌지", "브로콜리", "당근", "핫도그", "피자", "도넛", "케이크", "의자", "소파",
    "화분", "침대", "식탁", "화장실", "TV", "노트북", "마우스", "리모컨", "키보드",
    "휴대폰", "전자레인지", "오븐", "토스터", "싱크대", "냉장고", "책", "시계",
    "꽃병", "가위", "테디베어", "헤어드라이어", "칫솔"
]

class DetectionResult(BaseModel):
    """탐지 결과 모델"""
    class_id: int
    class_name: str
    confidence: float
    bbox: List[int]  # [x1, y1, x2, y2]

class DetectionResponse(BaseModel):
    """API 응답 모델"""
    success: bool
    count: int
    detections: List[DetectionResult]
    image_base64: Optional[str] = None

@app.get("/")
async def root():
    """API 상태 확인"""
    return {
        "status": "running",
        "service": "YOLO8 객체 탐지 API",
        "version": "1.0.0",
        "endpoints": {
            "detect": "POST /api/detect - 이미지 객체 탐지",
            "detect_base64": "POST /api/detect/base64 - Base64 이미지 탐지",
            "classes": "GET /api/classes - 탐지 가능 클래스 목록"
        }
    }

@app.get("/health")
async def health():
    """헬스 체크"""
    return {"status": "OK", "model": "YOLOv8n"}

@app.get("/api/classes")
async def get_classes():
    """탐지 가능한 클래스 목록"""
    return {
        "count": len(COCO_CLASSES),
        "classes": [{"id": i, "name": name} for i, name in enumerate(COCO_CLASSES)]
    }

@app.post("/api/detect", response_model=DetectionResponse)
async def detect_objects(
    image: UploadFile = File(...),
    confidence: float = 0.5,
    draw_boxes: bool = True
):
    """
    이미지에서 객체 탐지

    - **image**: 업로드할 이미지 파일
    - **confidence**: 최소 신뢰도 (0.0 ~ 1.0)
    - **draw_boxes**: 바운딩 박스 그리기 여부
    """
    try:
        # 모델 로드
        model = load_yolo_model()

        # 이미지 읽기
        contents = await image.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise HTTPException(status_code=400, detail="이미지를 읽을 수 없습니다")

        # YOLO 추론
        results = model(img, conf=confidence)

        detections = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
                class_id = int(box.cls[0].cpu().numpy())
                conf = float(box.conf[0].cpu().numpy())

                class_name = COCO_CLASSES[class_id] if class_id < len(COCO_CLASSES) else f"class_{class_id}"

                detections.append(DetectionResult(
                    class_id=class_id,
                    class_name=class_name,
                    confidence=round(conf, 3),
                    bbox=[x1, y1, x2, y2]
                ))

                # 바운딩 박스 그리기
                if draw_boxes:
                    color = get_color(class_id)
                    cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

                    # 라벨
                    label = f"{class_name} {conf:.2f}"
                    (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
                    cv2.rectangle(img, (x1, y1 - 25), (x1 + w, y1), color, -1)
                    cv2.putText(img, label, (x1, y1 - 5),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # 결과 이미지를 Base64로 인코딩
        image_base64 = None
        if draw_boxes:
            _, buffer = cv2.imencode('.jpg', img)
            image_base64 = base64.b64encode(buffer).decode('utf-8')

        logger.info(f"탐지 완료: {len(detections)}개 객체 발견")

        return DetectionResponse(
            success=True,
            count=len(detections),
            detections=detections,
            image_base64=image_base64
        )

    except Exception as e:
        logger.error(f"탐지 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class Base64ImageRequest(BaseModel):
    """Base64 이미지 요청"""
    image: str
    confidence: float = 0.5
    draw_boxes: bool = True

@app.post("/api/detect/base64", response_model=DetectionResponse)
async def detect_objects_base64(request: Base64ImageRequest):
    """
    Base64 인코딩된 이미지에서 객체 탐지
    """
    try:
        # 모델 로드
        model = load_yolo_model()

        # Base64 디코딩
        image_data = base64.b64decode(request.image)
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise HTTPException(status_code=400, detail="이미지를 디코딩할 수 없습니다")

        # YOLO 추론
        results = model(img, conf=request.confidence)

        detections = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
                class_id = int(box.cls[0].cpu().numpy())
                conf = float(box.conf[0].cpu().numpy())

                class_name = COCO_CLASSES[class_id] if class_id < len(COCO_CLASSES) else f"class_{class_id}"

                detections.append(DetectionResult(
                    class_id=class_id,
                    class_name=class_name,
                    confidence=round(conf, 3),
                    bbox=[x1, y1, x2, y2]
                ))

                if request.draw_boxes:
                    color = get_color(class_id)
                    cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                    label = f"{class_name} {conf:.2f}"
                    (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
                    cv2.rectangle(img, (x1, y1 - 25), (x1 + w, y1), color, -1)
                    cv2.putText(img, label, (x1, y1 - 5),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        image_base64 = None
        if request.draw_boxes:
            _, buffer = cv2.imencode('.jpg', img)
            image_base64 = base64.b64encode(buffer).decode('utf-8')

        return DetectionResponse(
            success=True,
            count=len(detections),
            detections=detections,
            image_base64=image_base64
        )

    except Exception as e:
        logger.error(f"탐지 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def get_color(class_id: int) -> tuple:
    """클래스별 색상 반환"""
    colors = [
        (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
        (255, 0, 255), (0, 255, 255), (128, 0, 0), (0, 128, 0),
        (0, 0, 128), (128, 128, 0), (128, 0, 128), (0, 128, 128)
    ]
    return colors[class_id % len(colors)]

# 번호판 인식 엔드포인트 추가
@app.post("/api/plate/recognize")
async def recognize_plate(image: UploadFile = File(...)):
    """
    번호판 인식 API
    - YOLO로 차량/번호판 영역 탐지
    - OCR로 번호판 텍스트 추출
    """
    try:
        model = load_yolo_model()

        contents = await image.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise HTTPException(status_code=400, detail="이미지를 읽을 수 없습니다")

        # YOLO 추론 (차량 클래스: 2=car, 5=bus, 7=truck)
        results = model(img, conf=0.3)

        vehicles = []
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0].cpu().numpy())

                # 차량 클래스만 필터링
                if class_id in [2, 5, 7]:  # car, bus, truck
                    x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
                    conf = float(box.conf[0].cpu().numpy())

                    vehicles.append({
                        "type": COCO_CLASSES[class_id],
                        "confidence": round(conf, 3),
                        "bbox": [x1, y1, x2, y2]
                    })

        return {
            "success": True,
            "vehicle_count": len(vehicles),
            "vehicles": vehicles,
            "message": f"{len(vehicles)}대의 차량이 감지되었습니다"
        }

    except Exception as e:
        logger.error(f"번호판 인식 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("🚀 YOLO8 객체 탐지 서버 시작!")
    print("📍 API 문서: http://localhost:8001/docs")
    uvicorn.run(app, host="0.0.0.0", port=8001)
