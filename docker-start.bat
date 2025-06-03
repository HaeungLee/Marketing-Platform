@echo off
echo ==========================================
echo Marketing Platform Docker 환경 시작
echo ==========================================

REM 환경변수 파일 확인
if not exist .env (
    echo .env 파일이 없습니다. .env.example을 복사하여 .env 파일을 생성해주세요.
    echo copy .env.example .env
    pause
    exit /b 1
)

echo 1. Docker 컨테이너 정리 중...
docker-compose down -v 2>nul

echo 2. Docker 이미지 빌드 중...
docker-compose build --no-cache

echo 3. 서비스 시작 중...
docker-compose up -d

echo 4. 서비스 상태 확인 중...
timeout /t 30

echo.
echo ==========================================
echo 서비스 시작 완료!
echo ==========================================
echo 프론트엔드: http://localhost
echo 백엔드 API: http://localhost:8000
echo 데이터베이스 관리: http://localhost:8080 (개발모드)
echo API 문서: http://localhost:8000/docs
echo ==========================================
echo.

REM 서비스 상태 확인
echo 서비스 상태:
docker-compose ps

echo.
echo 로그를 보려면: docker-compose logs -f
echo 정지하려면: docker-compose down
echo.
pause
