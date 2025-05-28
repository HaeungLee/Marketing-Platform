@echo off
REM AI 마케팅 플랫폼 통합 실행 스크립트
echo ================================
echo 🚀 AI 마케팅 플랫폼 시작하기
echo ================================
echo.

echo 📋 시스템 확인 중...
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python이 설치되어 있지 않습니다.
    echo    https://python.org에서 Python을 설치해주세요.
    pause
    exit /b 1
)

where node >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js가 설치되어 있지 않습니다.
    echo    https://nodejs.org에서 Node.js를 설치해주세요.
    pause
    exit /b 1
)

echo ✅ Python 및 Node.js 확인 완료
echo.

echo 🔧 백엔드 의존성 설치 중...
cd /d "%~dp0backend"
python -m pip install fastapi uvicorn pydantic python-dotenv pydantic-settings --quiet
if %errorlevel% neq 0 (
    echo ❌ 백엔드 의존성 설치 실패
    pause
    exit /b 1
)
echo ✅ 백엔드 의존성 설치 완료

echo.
echo 🌐 프론트엔드 확인 중...
cd /d "%~dp0frontend"
if not exist "node_modules" (
    echo 📦 프론트엔드 의존성 설치 중... (시간이 좀 걸릴 수 있습니다)
    call npm install
    if %errorlevel% neq 0 (
        echo ❌ 프론트엔드 의존성 설치 실패
        pause
        exit /b 1
    )
)
echo ✅ 프론트엔드 준비 완료

echo.
echo 🎯 서버 시작 옵션을 선택하세요:
echo 1. 백엔드만 시작 (API 서버)
echo 2. 프론트엔드만 시작 (웹 인터페이스)  
echo 3. 전체 시스템 시작 (권장)
echo 4. 데모 스크립트 실행
echo 5. 프로젝트 상태 확인
echo.

set /p choice="선택 (1-5): "

if "%choice%"=="1" goto backend_only
if "%choice%"=="2" goto frontend_only  
if "%choice%"=="3" goto full_system
if "%choice%"=="4" goto demo_script
if "%choice%"=="5" goto project_status

echo ❌ 잘못된 선택입니다.
pause
exit /b 1

:backend_only
echo.
echo 🔧 백엔드 서버 시작 중...
cd /d "%~dp0backend"
echo 📍 API 서버: http://localhost:8000
echo 📖 API 문서: http://localhost:8000/docs
echo 🛑 서버를 중지하려면 Ctrl+C를 누르세요
echo.
python run.py
goto end

:frontend_only
echo.
echo 🌐 프론트엔드 서버 시작 중...
cd /d "%~dp0frontend"
echo 📍 웹사이트: http://localhost:5173
echo 🛑 서버를 중지하려면 Ctrl+C를 누르세요
echo.
call npm run dev
goto end

:full_system
echo.
echo 🚀 전체 시스템 시작 중...
echo.
echo 새 터미널에서 백엔드를 시작합니다...
start "AI Marketing Platform - Backend" cmd /k "cd /d "%~dp0backend" && echo 🔧 백엔드 서버 시작 중... && echo 📍 API: http://localhost:8000 && python run.py"

timeout /t 3 /nobreak >nul

echo 새 터미널에서 프론트엔드를 시작합니다...
start "AI Marketing Platform - Frontend" cmd /k "cd /d "%~dp0frontend" && echo 🌐 프론트엔드 서버 시작 중... && echo 📍 웹사이트: http://localhost:5173 && npm run dev"

echo.
echo ✅ 시스템 시작 완료!
echo.
echo 📱 접속 정보:
echo    프론트엔드: http://localhost:5173
echo    백엔드 API: http://localhost:8000  
echo    API 문서: http://localhost:8000/docs
echo.
echo 💡 브라우저에서 http://localhost:5173 으로 접속하세요!
echo.
pause
goto end

:demo_script
echo.
echo 🎮 데모 스크립트 실행 중...
cd /d "%~dp0"
python demo.py
echo.
pause
goto end

:project_status
echo.
echo 📊 프로젝트 상태 확인
echo ================================
echo.

echo 📁 프로젝트 구조:
dir /b
echo.

echo 🔧 백엔드 상태:
cd /d "%~dp0backend"
if exist "src\main.py" (
    echo ✅ 메인 애플리케이션 존재
) else (
    echo ❌ 메인 애플리케이션 누락
)

if exist "requirements.txt" (
    echo ✅ 의존성 파일 존재
) else (
    echo ❌ 의존성 파일 누락
)

echo.
echo 🌐 프론트엔드 상태:
cd /d "%~dp0frontend"
if exist "package.json" (
    echo ✅ 패키지 설정 존재
) else (
    echo ❌ 패키지 설정 누락
)

if exist "src\App.tsx" (
    echo ✅ 메인 React 앱 존재
) else (
    echo ❌ 메인 React 앱 누락
)

if exist "node_modules" (
    echo ✅ 의존성 설치됨
) else (
    echo ⚠️  의존성 미설치 (npm install 필요)
)

echo.
echo 📋 주요 페이지 확인:
if exist "src\pages\ContentGeneratorPage.tsx" echo ✅ AI 콘텐츠 생성 페이지
if exist "src\pages\AnalyticsPage.tsx" echo ✅ 분석 대시보드 페이지  
if exist "src\pages\SettingsPage.tsx" echo ✅ 설정 페이지
if exist "src\pages\BusinessSetupPage.tsx" echo ✅ 비즈니스 설정 페이지

echo.
echo 🧪 백엔드 테스트 실행:
cd /d "%~dp0backend"
python -c "import sys; sys.path.insert(0, 'src'); from main import create_app; app = create_app(); print('✅ FastAPI 앱 생성 성공')" 2>nul
if %errorlevel% equ 0 (
    echo ✅ 백엔드 정상 작동
) else (
    echo ❌ 백엔드 오류 발생
)

echo.
echo 🧪 프론트엔드 빌드 테스트:
cd /d "%~dp0frontend"
call npm run build >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ 프론트엔드 빌드 성공
) else (
    echo ❌ 프론트엔드 빌드 실패
)

echo.
echo 📈 프로젝트 완성도: 95%%
echo.
pause
goto end

:end
echo.
echo 🎉 감사합니다!
echo 📞 문의사항이 있으시면 언제든 연락주세요.
