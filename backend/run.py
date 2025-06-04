#!/usr/bin/env python3
"""
Backend server startup script
"""
import uvicorn
import sys
import os

# Add both backend and src directories to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'src'))

if __name__ == "__main__":
    uvicorn.run(
        "src.main:create_app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["src"],
        factory=True
    )
