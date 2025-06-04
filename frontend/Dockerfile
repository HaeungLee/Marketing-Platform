# 프론트엔드 Dockerfile - React + Vite + Nginx
# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

# 패키지 파일 복사
COPY package*.json ./

# 의존성 설치
RUN npm ci --only=production

# 소스 코드 복사
COPY . .

# 프로덕션 빌드
RUN npm run build

# Production stage
FROM nginx:alpine

# Nginx 설정 파일 복사
COPY nginx.conf /etc/nginx/nginx.conf

# 빌드된 정적 파일 복사
COPY --from=builder /app/dist /usr/share/nginx/html

# 포트 노출
EXPOSE 80

# Nginx 시작
CMD ["nginx", "-g", "daemon off;"]
