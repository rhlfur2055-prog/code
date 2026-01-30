@echo off
chcp 65001 > nul
echo 🚀 CodeMaster 190개 빈 페이지 자동 작성 시작...
echo.

cd /d C:\tools\codemaster-next-main\codemaster-next-main\codemaster-next-main

claude "VIBE_CODING_PROMPT.md와 INCIDENT_DRIVEN_LEARNING_PROMPT_v3.md를 참고하여 src/data/contents/ 폴더의 다음 파일들의 빈 페이지를 모두 채워줘:

1. javascript.json (42개 빈칸)
2. ai.json (40개 빈칸)
3. html-css.json (34개 빈칸)
4. cleancode.json (31개 빈칸)
5. python.json (23개 빈칸)
6. ai-roadmap.json (20개 빈칸)

각 페이지마다 7-8개 섹션 필수: concept, code, use-case, best-practice, common-mistake, tip, practice

바이브 코딩 스타일:
✅ 이모지 많이 🎯💡📊
✅ 편한 말투 (~예요)
✅ 실무 예시 (네이버/카카오/쿠팡)
✅ 2024-2025 실제 사고 사례
✅ Good vs Bad 비교
✅ 성능 숫자 (1000배 빠름)
❌ ... 생략 금지
❌ 영어 주석 금지

지금 바로 190개 전부 작성 시작!"

echo.
echo ✅ 완료! http://localhost:3000 에서 확인하세요.
pause
