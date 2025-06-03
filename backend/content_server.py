#!/usr/bin/env python3
"""
Content API만을 위한 단순한 FastAPI 서버
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

# Content router import
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from content_simple import router as content_router

app = FastAPI(title="Marketing Platform - Content API", version="1.0.0")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 서빙 (이미지)
os.makedirs("static/images", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Content API 라우터 등록
app.include_router(content_router, prefix="/api/v1/content", tags=["content"])

@app.get("/")
async def root():
    return {"message": "Marketing Platform Content API Server"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("content_server:app", host="0.0.0.0", port=8000, reload=True)
