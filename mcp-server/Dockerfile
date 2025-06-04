FROM node:18-alpine AS builder

WORKDIR /app

# 패키지 파일 복사
COPY package*.json ./
COPY tsconfig.json ./

# 의존성 설치
RUN npm ci

# 소스 코드 복사
COPY src/ ./src/

# TypeScript 빌드
RUN npm run build

# Production stage
FROM node:18-alpine

WORKDIR /app

# 프로덕션 의존성만 설치
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

# 빌드된 파일 복사
COPY --from=builder /app/dist ./dist

# 헬스체크 추가
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD node -e "console.log('Health check')" || exit 1

# 포트 노출
EXPOSE 3001

# 애플리케이션 시작
CMD ["npm", "start"]
