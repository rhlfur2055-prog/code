export interface AIDemo {
  slug: string;
  name: string;
  description: string;
  embedUrl: string;
  difficulty: '입문' | '초급' | '중급';
  category: string;
  tags: string[];
  codeExample?: string;
}

export const aiDemos: AIDemo[] = [
  {
    slug: "object-detection",
    name: "객체 탐지 (YOLO)",
    description: "이미지에서 사물을 자동으로 인식하고 위치를 표시합니다",
    embedUrl: "https://kadirnar-yolov10.hf.space",
    difficulty: "입문",
    category: "컴퓨터 비전",
    tags: ["YOLO", "객체탐지", "이미지분석"],
    codeExample: `from ultralytics import YOLO

# 모델 로드
model = YOLO('yolov8n.pt')

# 이미지 추론
results = model('image.jpg')

# 결과 표시
results[0].show()`
  },
  {
    slug: "background-removal",
    name: "배경 제거",
    description: "이미지에서 배경을 자동으로 제거하고 투명 PNG로 저장",
    embedUrl: "https://eccv2022-dis-background-removal.hf.space",
    difficulty: "입문",
    category: "이미지 편집",
    tags: ["배경제거", "이미지편집", "PNG"],
    codeExample: `from rembg import remove
from PIL import Image

# 이미지 로드
input_img = Image.open('photo.jpg')

# 배경 제거
output = remove(input_img)

# 저장
output.save('result.png')`
  },
  {
    slug: "image-upscale",
    name: "이미지 업스케일",
    description: "저화질 이미지를 AI로 고화질로 변환 (2x, 4x)",
    embedUrl: "https://finegrain-finegrain-image-enhancer.hf.space",
    difficulty: "입문",
    category: "이미지 편집",
    tags: ["업스케일", "화질개선", "슈퍼해상도"],
    codeExample: `from PIL import Image
import torch
from realesrgan import RealESRGAN

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = RealESRGAN(device, scale=4)
model.load_weights('weights/RealESRGAN_x4.pth')

image = Image.open('low_res.jpg')
sr_image = model.predict(image)
sr_image.save('high_res.png')`
  },
  {
    slug: "image-caption",
    name: "이미지 설명 (BLIP)",
    description: "AI가 이미지 내용을 자연어로 설명합니다",
    embedUrl: "https://salesforce-blip.hf.space",
    difficulty: "입문",
    category: "멀티모달",
    tags: ["이미지캡션", "BLIP", "비전언어"],
    codeExample: `from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

image = Image.open('photo.jpg')
inputs = processor(image, return_tensors="pt")
output = model.generate(**inputs)

caption = processor.decode(output[0], skip_special_tokens=True)
print(caption)`
  },
  {
    slug: "face-restoration",
    name: "얼굴 복원 (GFPGAN)",
    description: "흐릿하거나 손상된 얼굴 사진을 선명하게 복원",
    embedUrl: "https://xintao-gfpgan.hf.space",
    difficulty: "입문",
    category: "이미지 복원",
    tags: ["얼굴복원", "GFPGAN", "화질개선"],
    codeExample: `import cv2
from gfpgan import GFPGANer

# 복원 모델 로드
restorer = GFPGANer(
    model_path='GFPGANv1.4.pth',
    upscale=2,
    arch='clean'
)

# 이미지 로드 및 복원
img = cv2.imread('blurry_face.jpg')
_, _, output = restorer.enhance(img)

cv2.imwrite('restored_face.jpg', output)`
  },
  {
    slug: "depth-estimation",
    name: "깊이 추정 (Depth Anything)",
    description: "2D 이미지에서 3D 깊이 정보를 분석",
    embedUrl: "https://depth-anything-depth-anything-v2.hf.space",
    difficulty: "초급",
    category: "3D 비전",
    tags: ["깊이추정", "3D", "DepthAnything"],
    codeExample: `from transformers import pipeline
from PIL import Image

# 깊이 추정 파이프라인
pipe = pipeline(task="depth-estimation", model="LiheYoung/depth-anything-large-hf")

# 이미지 로드
image = Image.open('scene.jpg')

# 깊이 추정
depth = pipe(image)
depth_map = depth["depth"]
depth_map.save("depth_map.png")`
  },
  {
    slug: "image-segmentation",
    name: "이미지 분할 (SAM 2)",
    description: "이미지에서 객체 영역을 정밀하게 분리",
    embedUrl: "https://facebook-sam2-point-tracking.hf.space",
    difficulty: "초급",
    category: "컴퓨터 비전",
    tags: ["SAM", "세그멘테이션", "Meta"],
    codeExample: `from segment_anything import sam_model_registry, SamPredictor
import cv2

# SAM 모델 로드
sam = sam_model_registry["vit_h"](checkpoint="sam_vit_h.pth")
predictor = SamPredictor(sam)

# 이미지 설정
image = cv2.imread("image.jpg")
predictor.set_image(image)

# 포인트로 마스크 생성
masks, _, _ = predictor.predict(
    point_coords=[[500, 375]],
    point_labels=[1]
)`
  },
  {
    slug: "ocr",
    name: "OCR (문자 인식)",
    description: "이미지에서 한글/영문 텍스트를 추출",
    embedUrl: "https://tomofi-easyocr.hf.space",
    difficulty: "입문",
    category: "문서 처리",
    tags: ["OCR", "텍스트추출", "EasyOCR"],
    codeExample: `import easyocr

# Reader 생성 (한국어 + 영어)
reader = easyocr.Reader(['ko', 'en'])

# OCR 실행
result = reader.readtext('document.png')

# 결과 출력
for (bbox, text, prob) in result:
    print(f'{text} (신뢰도: {prob:.2f})')`
  },
  {
    slug: "music-generation",
    name: "음악 생성 (MusicGen)",
    description: "텍스트 설명으로 음악을 자동 생성",
    embedUrl: "https://facebook-musicgen.hf.space",
    difficulty: "입문",
    category: "오디오",
    tags: ["음악생성", "MusicGen", "Meta"],
    codeExample: `from audiocraft.models import MusicGen
import scipy

# 모델 로드
model = MusicGen.get_pretrained('facebook/musicgen-small')
model.set_generation_params(duration=8)

# 텍스트로 음악 생성
wav = model.generate(['happy acoustic guitar melody'])

# 저장
scipy.io.wavfile.write('music.wav', rate=32000, data=wav[0].cpu().numpy())`
  },
  {
    slug: "speech-recognition",
    name: "음성 인식 (Whisper)",
    description: "음성 파일을 텍스트로 정확하게 변환",
    embedUrl: "https://openai-whisper.hf.space",
    difficulty: "입문",
    category: "오디오",
    tags: ["음성인식", "Whisper", "STT"],
    codeExample: `import whisper

# 모델 로드
model = whisper.load_model("base")

# 음성 인식
result = model.transcribe("audio.mp3")

# 결과 출력
print(result["text"])

# 타임스탬프 포함
for segment in result["segments"]:
    print(f'[{segment["start"]:.2f}s] {segment["text"]}')`
  }
];

export const getDemoBySlug = (slug: string): AIDemo | undefined => {
  return aiDemos.find(demo => demo.slug === slug);
};

export const getDemosByCategory = (category: string): AIDemo[] => {
  return aiDemos.filter(demo => demo.category === category);
};

export const getCategories = (): string[] => {
  return Array.from(new Set(aiDemos.map(demo => demo.category)));
};
