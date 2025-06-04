@echo off
echo 마케팅 플랫폼 백엔드 서버 시작
echo 종료하려면 Ctrl+C를 누르세요.
echo.

REM 필요한 패키지 확인
python -c "import google.generativeai" 2>nul
if %errorlevel% neq 0 (
    echo Google Generative AI 라이브러리를 설치합니다...
    pip install google-generativeai
)

echo 백엔드 서버 시작 중...
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
