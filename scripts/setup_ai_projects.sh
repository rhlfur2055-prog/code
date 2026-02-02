#!/bin/bash

# ============================================
# AI 실습 프로젝트 자동 설치 스크립트 (Mac/Linux)
# CodeMaster Next - AI Practice Setup
# ============================================

set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 배너 출력
echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                                                           ║${NC}"
echo -e "${CYAN}║     🤖 AI 실습 프로젝트 자동 설치 스크립트 v1.0          ║${NC}"
echo -e "${CYAN}║                                                           ║${NC}"
echo -e "${CYAN}║     포함 프로젝트:                                        ║${NC}"
echo -e "${CYAN}║     1. YOLO 객체 인식                                     ║${NC}"
echo -e "${CYAN}║     2. 얼굴 인식 시스템                                   ║${NC}"
echo -e "${CYAN}║     3. 음성 챗봇                                          ║${NC}"
echo -e "${CYAN}║                                                           ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# OS 감지
OS="$(uname -s)"
case "${OS}" in
    Linux*)     MACHINE=Linux;;
    Darwin*)    MACHINE=Mac;;
    *)          MACHINE="UNKNOWN:${OS}"
esac
echo -e "${BLUE}[INFO]${NC} 운영체제: ${MACHINE}"

# Python 확인
echo ""
echo -e "${YELLOW}[1/6]${NC} Python 확인 중..."

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3이 설치되어 있지 않습니다!${NC}"
    echo ""
    if [ "$MACHINE" == "Mac" ]; then
        echo "설치 방법:"
        echo "  brew install python3"
    else
        echo "설치 방법:"
        echo "  sudo apt update && sudo apt install python3 python3-pip python3-venv"
    fi
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1)
echo -e "${GREEN}✅ ${PYTHON_VERSION} 확인됨${NC}"

# pip 업그레이드
echo ""
echo -e "${YELLOW}[2/6]${NC} pip 업그레이드 중..."
python3 -m pip install --upgrade pip --quiet

# 프로젝트 디렉토리 생성
PROJECT_DIR="$HOME/AIProjects"
echo ""
echo -e "${YELLOW}[3/6]${NC} 프로젝트 폴더 생성 중: ${PROJECT_DIR}"

mkdir -p "$PROJECT_DIR/yolo_detector"
mkdir -p "$PROJECT_DIR/face_detector"
mkdir -p "$PROJECT_DIR/voice_chatbot"

echo -e "${GREEN}✅ 폴더 생성 완료${NC}"

# 패키지 설치
echo ""
echo -e "${YELLOW}[4/6]${NC} 필수 패키지 설치 중... (약 2-5분 소요)"
echo ""

# 공통 패키지
echo "     📦 OpenCV 설치 중..."
pip3 install opencv-python --quiet

echo "     📦 NumPy 설치 중..."
pip3 install numpy --quiet

# YOLO 패키지
echo "     📦 Ultralytics (YOLO) 설치 중..."
pip3 install ultralytics --quiet

# 얼굴 인식 패키지
echo "     📦 face-recognition 설치 중..."
if [ "$MACHINE" == "Mac" ]; then
    # Mac에서 dlib 먼저 설치
    if ! command -v brew &> /dev/null; then
        echo "     ⚠️ Homebrew가 필요합니다. cmake 설치 건너뜀"
    else
        brew install cmake --quiet 2>/dev/null || true
    fi
fi
pip3 install face-recognition --quiet 2>/dev/null || {
    echo "     ⚠️ face-recognition 설치 실패, dlib 먼저 설치 시도..."
    pip3 install cmake --quiet
    pip3 install dlib --quiet
    pip3 install face-recognition --quiet
}

# 음성 인식 패키지
echo "     📦 SpeechRecognition 설치 중..."
pip3 install SpeechRecognition --quiet

echo "     📦 gTTS 설치 중..."
pip3 install gtts --quiet

echo "     📦 PyAudio 설치 중..."
if [ "$MACHINE" == "Mac" ]; then
    brew install portaudio --quiet 2>/dev/null || true
    pip3 install pyaudio --quiet 2>/dev/null || echo "     ⚠️ PyAudio 설치 실패 (음성 입력 기능 제한)"
else
    sudo apt-get install -y portaudio19-dev python3-pyaudio --quiet 2>/dev/null || true
    pip3 install pyaudio --quiet 2>/dev/null || echo "     ⚠️ PyAudio 설치 실패 (음성 입력 기능 제한)"
fi

# 음성 재생 도구
if [ "$MACHINE" == "Linux" ]; then
    echo "     📦 mpg321 설치 중..."
    sudo apt-get install -y mpg321 --quiet 2>/dev/null || true
fi

echo ""
echo -e "${GREEN}✅ 패키지 설치 완료${NC}"

# Python 파일 생성
echo ""
echo -e "${YELLOW}[5/6]${NC} 프로젝트 파일 생성 중..."

# YOLO 프로젝트
cat > "$PROJECT_DIR/yolo_detector/yolo_detector.py" << 'EOF'
from ultralytics import YOLO
import cv2

# YOLO 모델 로드
model = YOLO('yolov8n.pt')

# 웹캠 초기화
cap = cv2.VideoCapture(0)

print("YOLO 객체 인식 시작! 종료하려면 'q'를 누르세요.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("웹캠을 열 수 없습니다.")
        break

    # YOLO로 객체 탐지
    results = model(frame, verbose=False)
    annotated_frame = results[0].plot()

    # 화면에 표시
    cv2.imshow('YOLO Object Detection', annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("프로그램 종료")
EOF

# 얼굴 인식 프로젝트
cat > "$PROJECT_DIR/face_detector/face_detector.py" << 'EOF'
import cv2

# Haar Cascade 분류기 로드
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

cap = cv2.VideoCapture(0)

print("얼굴 인식 시작! 종료하려면 'q'를 누르세요.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, 'Face', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.putText(frame, f'Faces: {len(faces)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imshow('Face Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
EOF

# 음성 챗봇 프로젝트
cat > "$PROJECT_DIR/voice_chatbot/voice_chatbot.py" << 'EOF'
import speech_recognition as sr
from gtts import gTTS
import os
import platform
from datetime import datetime

def speak(text):
    print(f"AI: {text}")
    tts = gTTS(text=text, lang='ko')
    tts.save('response.mp3')

    if platform.system() == 'Darwin':  # macOS
        os.system('afplay response.mp3')
    else:  # Linux
        os.system('mpg321 response.mp3 2>/dev/null || mpg123 response.mp3 2>/dev/null')

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("듣고 있습니다... 말씀하세요!")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio, language='ko-KR')
            print(f"You: {text}")
            return text
        except:
            return None

def chatbot_response(user_input):
    user_input = user_input.lower()
    if '안녕' in user_input:
        return "안녕하세요! 무엇을 도와드릴까요?"
    elif '시간' in user_input:
        now = datetime.now()
        return f"현재 시각은 {now.hour}시 {now.minute}분입니다."
    elif '날씨' in user_input:
        return "오늘 날씨는 맑습니다."
    elif '종료' in user_input or '끝' in user_input:
        return "안녕히 가세요!"
    else:
        return "다시 말씀해주세요."

def main():
    speak("음성 챗봇을 시작합니다.")
    while True:
        user_input = listen()
        if user_input is None:
            continue
        if '종료' in user_input or '끝' in user_input:
            speak("안녕히 가세요!")
            break
        response = chatbot_response(user_input)
        speak(response)

if __name__ == "__main__":
    main()
EOF

# 실행 스크립트 생성
cat > "$PROJECT_DIR/run_yolo.sh" << EOF
#!/bin/bash
cd "$PROJECT_DIR/yolo_detector"
python3 yolo_detector.py
EOF
chmod +x "$PROJECT_DIR/run_yolo.sh"

cat > "$PROJECT_DIR/run_face.sh" << EOF
#!/bin/bash
cd "$PROJECT_DIR/face_detector"
python3 face_detector.py
EOF
chmod +x "$PROJECT_DIR/run_face.sh"

cat > "$PROJECT_DIR/run_voice.sh" << EOF
#!/bin/bash
cd "$PROJECT_DIR/voice_chatbot"
python3 voice_chatbot.py
EOF
chmod +x "$PROJECT_DIR/run_voice.sh"

echo -e "${GREEN}✅ 프로젝트 파일 생성 완료${NC}"

# 완료 메시지
echo ""
echo -e "${YELLOW}[6/6]${NC} 설치 완료!"
echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                                                           ║${NC}"
echo -e "${CYAN}║     ✅ AI 실습 프로젝트 설치가 완료되었습니다!           ║${NC}"
echo -e "${CYAN}║                                                           ║${NC}"
echo -e "${CYAN}║     프로젝트 위치: ~/AIProjects                           ║${NC}"
echo -e "${CYAN}║                                                           ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# 메뉴
show_menu() {
    echo ""
    echo -e "${BLUE}┌───────────────────────────────────────────────────────────┐${NC}"
    echo -e "${BLUE}│                      실행 메뉴                            │${NC}"
    echo -e "${BLUE}├───────────────────────────────────────────────────────────┤${NC}"
    echo -e "${BLUE}│  [1] YOLO 객체 인식 실행                                  │${NC}"
    echo -e "${BLUE}│  [2] 얼굴 인식 실행                                       │${NC}"
    echo -e "${BLUE}│  [3] 음성 챗봇 실행                                       │${NC}"
    echo -e "${BLUE}│  [4] 프로젝트 폴더 열기                                   │${NC}"
    echo -e "${BLUE}│  [5] 종료                                                 │${NC}"
    echo -e "${BLUE}└───────────────────────────────────────────────────────────┘${NC}"
    echo ""
    read -p "선택 (1-5): " choice

    case $choice in
        1)
            echo ""
            echo "YOLO 객체 인식을 실행합니다..."
            cd "$PROJECT_DIR/yolo_detector"
            python3 yolo_detector.py
            show_menu
            ;;
        2)
            echo ""
            echo "얼굴 인식을 실행합니다..."
            cd "$PROJECT_DIR/face_detector"
            python3 face_detector.py
            show_menu
            ;;
        3)
            echo ""
            echo "음성 챗봇을 실행합니다..."
            cd "$PROJECT_DIR/voice_chatbot"
            python3 voice_chatbot.py
            show_menu
            ;;
        4)
            if [ "$MACHINE" == "Mac" ]; then
                open "$PROJECT_DIR"
            else
                xdg-open "$PROJECT_DIR" 2>/dev/null || nautilus "$PROJECT_DIR" 2>/dev/null
            fi
            show_menu
            ;;
        5)
            echo ""
            echo -e "${GREEN}프로그램을 종료합니다. 즐거운 AI 학습 되세요! 🚀${NC}"
            exit 0
            ;;
        *)
            echo "잘못된 선택입니다. 다시 선택해주세요."
            show_menu
            ;;
    esac
}

show_menu
