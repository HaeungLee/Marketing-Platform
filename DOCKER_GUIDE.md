# Docker 환경 사용 가이드

## 🐳 Docker로 전체 서비스 실행

### 1. 환경 설정

```bash
# 환경변수 파일 생성
copy .env.example .env

# .env 파일에서 Google API 키 설정
GOOGLE_API_KEY=your_actual_google_api_key_here
```

### 2. 운영환경 실행

```bash
# 전체 서비스 시작
docker-start.bat

# 또는 수동 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 서비스 정지
docker-compose down
```

### 3. 개발환경 실행

```bash
# 개발환경 시작 (핫 리로드 지원)
docker-compose -f docker-compose.dev.yml up -d

# 백엔드만 재시작
docker-compose -f docker-compose.dev.yml restart backend-dev
```

## 📊 서비스 접속 정보

### 운영환경
- **프론트엔드**: http://localhost
- **백엔드 API**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs
- **DB 관리**: http://localhost:8080 (adminer)

### 개발환경
- **백엔드 API**: http://localhost:8001
- **DB 관리**: http://localhost:8081 (adminer)
- **PostgreSQL**: localhost:5433
- **Redis**: localhost:6380

## 🔧 유용한 Docker 명령어

```bash
# 컨테이너 상태 확인
docker-compose ps

# 특정 서비스 로그 확인
docker-compose logs -f backend

# 컨테이너 내부 접속
docker-compose exec backend bash
docker-compose exec postgres psql -U postgres -d marketing_platform

# 데이터베이스 백업
docker-compose exec postgres pg_dump -U postgres marketing_platform > backup.sql

# 데이터베이스 복원
docker-compose exec -T postgres psql -U postgres marketing_platform < backup.sql

# 캐시 정리
docker-compose exec redis redis-cli FLUSHALL

# 볼륨 데이터 완전 삭제
docker-compose down -v
```

## 🚀 배포 준비

### 1. 환경변수 설정
```bash
# 프로덕션 환경변수 설정
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=강력한-시크릿-키-변경필요
ALLOWED_ORIGINS=https://yourdomain.com
```

### 2. SSL/HTTPS 설정
```bash
# Nginx SSL 설정 추가
# frontend/nginx.conf 파일 수정
```

### 3. 클라우드 배포
```bash
# Docker Hub에 이미지 푸시
docker-compose build
docker tag marketing-platform_backend your-repo/marketing-platform-backend
docker push your-repo/marketing-platform-backend
```

## 🛠️ 트러블슈팅

### PostgreSQL 연결 오류
```bash
# 컨테이너 상태 확인
docker-compose ps

# PostgreSQL 로그 확인
docker-compose logs postgres

# 네트워크 확인
docker network ls
```

### 포트 충돌 해결
```bash
# 다른 포트 사용
docker-compose -f docker-compose.dev.yml up -d
```

### 데이터 초기화
```bash
# 모든 데이터 삭제 후 재시작
docker-clean.bat
docker-start.bat
```
