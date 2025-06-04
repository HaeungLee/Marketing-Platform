@echo off
echo ==========================================
echo Marketing Platform Docker 환경 정리
echo ==========================================

echo 1. 모든 컨테이너 정지 중...
docker-compose down

echo 2. 데이터 볼륨 제거 중... (데이터가 삭제됩니다!)
set /p confirm="데이터베이스 데이터를 모두 삭제하시겠습니까? (y/N): "
if /i "%confirm%"=="y" (
    docker-compose down -v
    docker volume prune -f
    echo 데이터 볼륨이 제거되었습니다.
) else (
    echo 데이터 볼륨은 유지됩니다.
)

echo 3. 사용하지 않는 이미지 정리 중...
docker image prune -f

echo 4. 네트워크 정리 중...
docker network prune -f

echo.
echo ==========================================
echo 정리 완료!
echo ==========================================
echo.

REM 남은 리소스 확인
echo 남은 컨테이너:
docker ps -a

echo.
echo 남은 이미지:
docker images

echo.
echo 남은 볼륨:
docker volume ls

pause
