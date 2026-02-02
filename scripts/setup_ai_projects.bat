@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

:: ============================================
:: AI 실습 프로젝트 자동 설치 스크립트 (Windows)
:: CodeMaster Next - AI Practice Setup
:: ============================================

title AI 실습 프로젝트 설치

:: 색상 설정
color 0A

echo.
echo  ╔═══════════════════════════════════════════════════════════╗
echo  ║                                                           ║
echo  ║     🤖 AI 실습 프로젝트 자동 설치 스크립트 v1.0          ║
echo  ║                                                           ║
echo  ║     포함 프로젝트:                                        ║
echo  ║     1. YOLO 객체 인식                                     ║
echo  ║     2. 얼굴 인식 시스템                                   ║
echo  ║     3. 음성 챗봇                                          ║
echo  ║                                                           ║
echo  ╚═══════════════════════════════════════════════════════════╝
echo.

:: Python 확인
echo [1/6] Python 확인 중...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ Python이 설치되어 있지 않습니다!
    echo.
    echo 설치 방법:
    echo 1. https://www.python.org/downloads/ 접속
    echo 2. 최신 Python 다운로드
    echo 3. 설치 시 "Add Python to PATH" 체크 필수!
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% 확인됨

:: pip 업그레이드
echo.
echo [2/6] pip 업그레이드 중...
python -m pip install --upgrade pip --quiet

:: 프로젝트 디렉토리 생성
set PROJECT_DIR=%USERPROFILE%\AIProjects
echo.
echo [3/6] 프로젝트 폴더 생성 중: %PROJECT_DIR%

if not exist "%PROJECT_DIR%" mkdir "%PROJECT_DIR%"
if not exist "%PROJECT_DIR%\yolo_detector" mkdir "%PROJECT_DIR%\yolo_detector"
if not exist "%PROJECT_DIR%\face_detector" mkdir "%PROJECT_DIR%\face_detector"
if not exist "%PROJECT_DIR%\voice_chatbot" mkdir "%PROJECT_DIR%\voice_chatbot"

echo ✅ 폴더 생성 완료

:: 패키지 설치
echo.
echo [4/6] 필수 패키지 설치 중... (약 2-5분 소요)
echo.

:: 공통 패키지
echo     📦 OpenCV 설치 중...
pip install opencv-python --quiet

echo     📦 NumPy 설치 중...
pip install numpy --quiet

:: YOLO 패키지
echo     📦 Ultralytics (YOLO) 설치 중...
pip install ultralytics --quiet

:: 얼굴 인식 패키지
echo     📦 face-recognition 설치 중...
pip install face-recognition --quiet 2>nul
if errorlevel 1 (
    echo     ⚠️ face-recognition 설치 실패, dlib 먼저 설치 시도...
    pip install cmake --quiet
    pip install dlib --quiet
    pip install face-recognition --quiet
)

:: 음성 인식 패키지
echo     📦 SpeechRecognition 설치 중...
pip install SpeechRecognition --quiet

echo     📦 gTTS 설치 중...
pip install gtts --quiet

echo     📦 PyAudio 설치 중...
pip install pyaudio --quiet 2>nul
if errorlevel 1 (
    echo     ⚠️ PyAudio 설치 실패, pipwin으로 재시도...
    pip install pipwin --quiet
    pipwin install pyaudio --quiet 2>nul
)

echo.
echo ✅ 패키지 설치 완료

:: Python 파일 생성
echo.
echo [5/6] 프로젝트 파일 생성 중...

:: YOLO 프로젝트
(
echo from ultralytics import YOLO
echo import cv2
echo.
echo # YOLO 모델 로드
echo model = YOLO^('yolov8n.pt'^)
echo.
echo # 웹캠 초기화
echo cap = cv2.VideoCapture^(0^)
echo.
echo print^("YOLO 객체 인식 시작! 종료하려면 'q'를 누르세요."^)
echo.
echo while True:
echo     ret, frame = cap.read^(^)
echo     if not ret:
echo         print^("웹캠을 열 수 없습니다."^)
echo         break
echo.
echo     # YOLO로 객체 탐지
echo     results = model^(frame, verbose=False^)
echo     annotated_frame = results[0].plot^(^)
echo.
echo     # 화면에 표시
echo     cv2.imshow^('YOLO Object Detection', annotated_frame^)
echo.
echo     if cv2.waitKey^(1^) ^& 0xFF == ord^('q'^):
echo         break
echo.
echo cap.release^(^)
echo cv2.destroyAllWindows^(^)
echo print^("프로그램 종료"^)
) > "%PROJECT_DIR%\yolo_detector\yolo_detector.py"

:: 얼굴 인식 프로젝트
(
echo import cv2
echo.
echo # Haar Cascade 분류기 로드
echo face_cascade = cv2.CascadeClassifier^(
echo     cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
echo ^)
echo.
echo cap = cv2.VideoCapture^(0^)
echo.
echo print^("얼굴 인식 시작! 종료하려면 'q'를 누르세요."^)
echo.
echo while True:
echo     ret, frame = cap.read^(^)
echo     if not ret:
echo         break
echo.
echo     gray = cv2.cvtColor^(frame, cv2.COLOR_BGR2GRAY^)
echo.
echo     faces = face_cascade.detectMultiScale^(
echo         gray, scaleFactor=1.1, minNeighbors=5, minSize=^(30, 30^)
echo     ^)
echo.
echo     for ^(x, y, w, h^) in faces:
echo         cv2.rectangle^(frame, ^(x, y^), ^(x+w, y+h^), ^(0, 255, 0^), 2^)
echo         cv2.putText^(frame, 'Face', ^(x, y-10^), cv2.FONT_HERSHEY_SIMPLEX, 0.9, ^(0, 255, 0^), 2^)
echo.
echo     cv2.putText^(frame, f'Faces: {len^(faces^)}', ^(10, 30^), cv2.FONT_HERSHEY_SIMPLEX, 1, ^(255, 255, 255^), 2^)
echo     cv2.imshow^('Face Detection', frame^)
echo.
echo     if cv2.waitKey^(1^) ^& 0xFF == ord^('q'^):
echo         break
echo.
echo cap.release^(^)
echo cv2.destroyAllWindows^(^)
) > "%PROJECT_DIR%\face_detector\face_detector.py"

:: 음성 챗봇 프로젝트
(
echo import speech_recognition as sr
echo from gtts import gTTS
echo import os
echo from datetime import datetime
echo.
echo def speak^(text^):
echo     print^(f"AI: {text}"^)
echo     tts = gTTS^(text=text, lang='ko'^)
echo     tts.save^('response.mp3'^)
echo     os.system^('start response.mp3'^)
echo.
echo def listen^(^):
echo     recognizer = sr.Recognizer^(^)
echo     with sr.Microphone^(^) as source:
echo         print^("듣고 있습니다... 말씀하세요!"^)
echo         recognizer.adjust_for_ambient_noise^(source, duration=1^)
echo         try:
echo             audio = recognizer.listen^(source, timeout=5^)
echo             text = recognizer.recognize_google^(audio, language='ko-KR'^)
echo             print^(f"You: {text}"^)
echo             return text
echo         except:
echo             return None
echo.
echo def chatbot_response^(user_input^):
echo     user_input = user_input.lower^(^)
echo     if '안녕' in user_input:
echo         return "안녕하세요! 무엇을 도와드릴까요?"
echo     elif '시간' in user_input:
echo         now = datetime.now^(^)
echo         return f"현재 시각은 {now.hour}시 {now.minute}분입니다."
echo     elif '날씨' in user_input:
echo         return "오늘 날씨는 맑습니다."
echo     elif '종료' in user_input or '끝' in user_input:
echo         return "안녕히 가세요!"
echo     else:
echo         return "다시 말씀해주세요."
echo.
echo def main^(^):
echo     speak^("음성 챗봇을 시작합니다."^)
echo     while True:
echo         user_input = listen^(^)
echo         if user_input is None:
echo             continue
echo         if '종료' in user_input or '끝' in user_input:
echo             speak^("안녕히 가세요!"^)
echo             break
echo         response = chatbot_response^(user_input^)
echo         speak^(response^)
echo.
echo if __name__ == "__main__":
echo     main^(^)
) > "%PROJECT_DIR%\voice_chatbot\voice_chatbot.py"

:: 실행 스크립트 생성
echo @echo off > "%PROJECT_DIR%\run_yolo.bat"
echo cd /d "%PROJECT_DIR%\yolo_detector" >> "%PROJECT_DIR%\run_yolo.bat"
echo python yolo_detector.py >> "%PROJECT_DIR%\run_yolo.bat"
echo pause >> "%PROJECT_DIR%\run_yolo.bat"

echo @echo off > "%PROJECT_DIR%\run_face.bat"
echo cd /d "%PROJECT_DIR%\face_detector" >> "%PROJECT_DIR%\run_face.bat"
echo python face_detector.py >> "%PROJECT_DIR%\run_face.bat"
echo pause >> "%PROJECT_DIR%\run_face.bat"

echo @echo off > "%PROJECT_DIR%\run_voice.bat"
echo cd /d "%PROJECT_DIR%\voice_chatbot" >> "%PROJECT_DIR%\run_voice.bat"
echo python voice_chatbot.py >> "%PROJECT_DIR%\run_voice.bat"
echo pause >> "%PROJECT_DIR%\run_voice.bat"

echo ✅ 프로젝트 파일 생성 완료

:: 완료 메시지
echo.
echo [6/6] 설치 완료!
echo.
echo  ╔═══════════════════════════════════════════════════════════╗
echo  ║                                                           ║
echo  ║     ✅ AI 실습 프로젝트 설치가 완료되었습니다!           ║
echo  ║                                                           ║
echo  ║     프로젝트 위치: %PROJECT_DIR%                         ║
echo  ║                                                           ║
echo  ╚═══════════════════════════════════════════════════════════╝
echo.

:menu
echo  ┌───────────────────────────────────────────────────────────┐
echo  │                      실행 메뉴                            │
echo  ├───────────────────────────────────────────────────────────┤
echo  │  [1] YOLO 객체 인식 실행                                  │
echo  │  [2] 얼굴 인식 실행                                       │
echo  │  [3] 음성 챗봇 실행                                       │
echo  │  [4] 프로젝트 폴더 열기                                   │
echo  │  [5] 종료                                                 │
echo  └───────────────────────────────────────────────────────────┘
echo.
set /p choice="선택 (1-5): "

if "%choice%"=="1" (
    echo.
    echo YOLO 객체 인식을 실행합니다...
    cd /d "%PROJECT_DIR%\yolo_detector"
    python yolo_detector.py
    goto menu
)
if "%choice%"=="2" (
    echo.
    echo 얼굴 인식을 실행합니다...
    cd /d "%PROJECT_DIR%\face_detector"
    python face_detector.py
    goto menu
)
if "%choice%"=="3" (
    echo.
    echo 음성 챗봇을 실행합니다...
    cd /d "%PROJECT_DIR%\voice_chatbot"
    python voice_chatbot.py
    goto menu
)
if "%choice%"=="4" (
    explorer "%PROJECT_DIR%"
    goto menu
)
if "%choice%"=="5" (
    echo.
    echo 프로그램을 종료합니다. 즐거운 AI 학습 되세요! 🚀
    pause
    exit /b 0
)

echo 잘못된 선택입니다. 다시 선택해주세요.
goto menu
