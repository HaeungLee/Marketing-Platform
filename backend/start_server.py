#!/usr/bin/env python3
"""
FastAPI 서버 시작 스크립트
"""
import uvicorn
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def start_server():
    try:
        print("🚀 Starting FastAPI server...")
        print("📁 Python path configured")
        
        # Import main app
        from main import app
        print("✅ FastAPI app imported successfully")
        
        # Start server
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            reload=False,  # Disable reload for testing
        )
        
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    start_server()
