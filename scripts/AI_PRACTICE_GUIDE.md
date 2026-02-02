# AI 실습 프로젝트 자동 설치 가이드

## 포함된 파일

1. **setup_ai_projects.bat** - Windows용 설치 스크립트
2. **setup_ai_projects.sh** - Mac/Linux용 설치 스크립트
3. **AI_PRACTICE_GUIDE.md** - 이 문서

---

## Windows 사용자

### 설치 방법

1. **setup_ai_projects.bat** 파일을 다운로드
2. 파일에 마우스 우클릭 → **"관리자 권한으로 실행"** 선택
3. 자동으로 설치 진행 (약 5-10분 소요)
4. 설치 완료 후 실행 메뉴 선택

### 실행 메뉴

설치가 완료되면 다음 메뉴가 표시됩니다:

```
[1] YOLO 객체 인식 실행
[2] 얼굴 인식 실행
[3] 음성 챗봇 실행
[4] 프로젝트 폴더 열기
[5] 종료
```

### 수동 실행 방법

프로젝트 폴더: `C:\Users\[사용자명]\AIProjects\`

```cmd
cd %USERPROFILE%\AIProjects

# YOLO 실행
run_yolo.bat

# 얼굴 인식 실행
run_face.bat

# 음성 챗봇 실행
run_voice.bat
```

---

## Mac 사용자

### 설치 방법

1. **setup_ai_projects.sh** 파일을 다운로드
2. 터미널 열기 (Cmd + Space → "터미널" 검색)
3. 다운로드 폴더로 이동:
   ```bash
   cd ~/Downloads
   ```
4. 실행 권한 부여:
   ```bash
   chmod +x setup_ai_projects.sh
   ```
5. 스크립트 실행:
   ```bash
   ./setup_ai_projects.sh
   ```

### 실행 메뉴

설치 완료 후 메뉴에서 선택하거나, 수동으로 실행:

```bash
cd ~/AIProjects

# YOLO 실행
./run_yolo.sh

# 얼굴 인식 실행
./run_face.sh

# 음성 챗봇 실행
./run_voice.sh
```

---

## Linux 사용자

### 설치 방법

```bash
# 1. 스크립트 다운로드 후
cd ~/Downloads

# 2. 실행 권한 부여
chmod +x setup_ai_projects.sh

# 3. 스크립트 실행
./setup_ai_projects.sh
```

### 의존성 설치 (Ubuntu/Debian)

```bash
# Python 설치
sudo apt update
sudo apt install python3 python3-pip python3-venv

# OpenCV 의존성
sudo apt install python3-opencv

# 음성 재생 도구 (선택사항)
sudo apt install mpg321
```

---

## 설치되는 내용

### 1. YOLO 객체 인식 프로젝트

**경로**: `AIProjects/yolo_detector/`

**파일**:
- `yolo_detector.py` - 메인 실행 파일
- `yolov8n.pt` - YOLO 모델 (자동 다운로드)

**기능**:
- 웹캠으로 실시간 객체 탐지
- 80+ 종류의 객체 인식 (사람, 자동차, 동물 등)
- 프레임 카운터 표시

**종료**: `q` 키

---

### 2. 얼굴 인식 프로젝트

**경로**: `AIProjects/face_detector/`

**파일**:
- `face_detector.py` - 메인 실행 파일

**기능**:
- 웹캠으로 실시간 얼굴 탐지
- 여러 명의 얼굴 동시 인식
- OpenCV 또는 face_recognition 라이브러리 자동 선택

**종료**: `q` 키

---

### 3. 음성 챗봇 프로젝트

**경로**: `AIProjects/voice_chatbot/`

**파일**:
- `voice_chatbot.py` - 메인 실행 파일
- `response.mp3` - 음성 응답 파일 (자동 생성)

**기능**:
- 음성 명령 인식 (한국어)
- AI 음성 응답
- 간단한 대화 기능 (인사, 시간, 날씨 등)

**명령어**:
- "안녕" - 인사
- "시간" - 현재 시간 확인
- "날씨" - 날씨 정보
- "종료" 또는 "끝" - 프로그램 종료

---

## 시스템 요구사항

### 최소 사양

| 항목 | 요구사항 |
|------|---------|
| **OS** | Windows 10/11, macOS 10.14+, Ubuntu 20.04+ |
| **Python** | 3.8 이상 |
| **RAM** | 4GB 이상 (8GB 권장) |
| **저장공간** | 2GB 이상 |
| **웹캠** | 필수 (YOLO, 얼굴 인식) |
| **마이크** | 필수 (음성 챗봇) |

### 권장 사양

- **RAM**: 8GB 이상
- **GPU**: NVIDIA GPU (CUDA 지원) - 속도 향상
- **웹캠**: 720p 이상

---

## 문제 해결

### 1. "Python을 찾을 수 없습니다"

**Windows**:
- https://www.python.org/downloads/ 에서 최신 Python 다운로드
- 설치 시 "Add Python to PATH" 체크 필수

**Mac**:
```bash
brew install python3
```

**Linux**:
```bash
sudo apt install python3 python3-pip
```

---

### 2. 웹캠이 작동하지 않습니다

**확인사항**:
- 다른 프로그램(Zoom, Teams 등)에서 웹캠 사용 중인지 확인
- 웹캠 권한 확인 (Mac: 시스템 환경설정 → 보안 및 개인 정보 보호)
- 웹캠이 제대로 연결되어 있는지 확인

**테스트**:
```python
import cv2
cap = cv2.VideoCapture(0)
print(cap.isOpened())  # True가 나와야 정상
```

---

### 3. 패키지 설치 실패

**Windows - pyaudio 오류**:
```cmd
pip install pipwin
pipwin install pyaudio
```

**Mac - face_recognition 오류**:
```bash
brew install cmake
pip3 install dlib
pip3 install face-recognition
```

**Linux - OpenCV 오류**:
```bash
sudo apt install python3-opencv libopencv-dev
```

---

### 4. YOLO 모델 다운로드 실패

**수동 다운로드**:
1. https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
2. 다운로드한 파일을 `AIProjects/yolo_detector/` 폴더에 복사

---

### 5. 음성 인식이 작동하지 않습니다

**확인사항**:
- 마이크 권한 확인
- 인터넷 연결 확인 (Google API 사용)
- 조용한 환경에서 테스트

**대안 (키보드 입력)**:
```python
user_input = input("입력: ")
```

---

### 6. 음성이 재생되지 않습니다

**Windows**:
- 기본 미디어 플레이어 확인
- `response.mp3` 파일 수동 재생 테스트

**Mac**:
```bash
brew install mpg321
# 또는
brew install mpg123
```

**Linux**:
```bash
sudo apt install mpg321 mpg123
```

---

## 성능 최적화

### GPU 가속 (NVIDIA GPU)

```bash
# CUDA 버전 확인
nvidia-smi

# PyTorch CUDA 버전 설치
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

---

### 속도 개선 팁

1. **낮은 해상도 사용**:
```python
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
```

2. **프레임 건너뛰기**:
```python
frame_count = 0
if frame_count % 2 == 0:  # 2프레임마다 한 번 처리
    results = model(frame)
```

3. **더 가벼운 YOLO 모델**:
```python
model = YOLO('yolov8n.pt')  # Nano (가장 빠름)
# yolov8s.pt - Small
# yolov8m.pt - Medium
# yolov8l.pt - Large
# yolov8x.pt - Extra Large (가장 정확)
```

---

## 학습 가이드

### 초보자 추천 순서

| 순서 | 프로젝트 | 예상 시간 | 난이도 |
|------|---------|----------|-------|
| 1 | 얼굴 인식 | 20분 | 초급 |
| 2 | YOLO 객체 인식 | 30분 | 중급 |
| 3 | 음성 챗봇 | 40분 | 중급 |

---

### 심화 학습 과제

#### Level 1 (초급)

**얼굴 인식**:
- [ ] 탐지된 얼굴 수 화면에 표시
- [ ] 얼굴에 모자이크 처리
- [ ] 웃는 얼굴 감지

**YOLO**:
- [ ] 특정 객체만 필터링 (예: 사람만)
- [ ] 객체별 카운트 표시
- [ ] 탐지 결과 로그 저장

**음성 챗봇**:
- [ ] 더 많은 대화 패턴 추가
- [ ] 계산기 기능 추가
- [ ] 대화 히스토리 저장

---

#### Level 2 (중급)

**얼굴 인식**:
- [ ] 특정 인물 등록 및 이름 인식
- [ ] 감정 분석 (행복/슬픔/화남)
- [ ] 출석 체크 시스템

**YOLO**:
- [ ] 객체 추적 (동일 객체 ID 부여)
- [ ] 침입 감지 알림
- [ ] 비디오 파일 분석

**음성 챗봇**:
- [ ] OpenAI GPT API 연동
- [ ] 날씨 API 실시간 연동
- [ ] 일정 관리 기능

---

#### Level 3 (고급)

**통합 프로젝트**:
- [ ] AI 보안 시스템 (얼굴 인식 + 침입 탐지)
- [ ] 스마트 홈 컨트롤러 (음성 + 객체 인식)
- [ ] AI 비서 (음성 챗봇 + 스케줄 관리)

---

## 추가 리소스

### 공식 문서

| 라이브러리 | URL |
|-----------|-----|
| YOLO | https://docs.ultralytics.com/ |
| OpenCV | https://docs.opencv.org/ |
| face_recognition | https://face-recognition.readthedocs.io/ |
| SpeechRecognition | https://pypi.org/project/SpeechRecognition/ |

### 튜토리얼

- **YOLO 한글 가이드**: https://github.com/ultralytics/ultralytics
- **OpenCV 기초**: https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html
- **Python 음성 인식**: https://realpython.com/python-speech-recognition/

---

## 라이선스

이 프로젝트는 교육 목적으로 제작되었습니다.

**사용된 오픈소스**:
- Ultralytics YOLO (AGPL-3.0)
- OpenCV (Apache 2.0)
- face_recognition (MIT)
- SpeechRecognition (BSD)

---

## 축하합니다!

AI 실습 환경 설정을 완료했습니다!

이제 직접 코드를 실행하고 수정하며 AI 기술을 배워보세요.

**Happy Coding!**
