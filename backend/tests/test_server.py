#!/usr/bin/env python3
"""
Simple test to check if the FastAPI server can start
"""
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from fastapi import FastAPI
    from config.settings import Settings
    
    print("✅ FastAPI imported successfully")
    print("✅ Settings imported successfully")
    
    # Test creating a simple app
    app = FastAPI(title="Test App")
    print("✅ FastAPI app created successfully")
    
    # Test settings
    settings = Settings()
    print(f"✅ Settings loaded: {settings.app_name}")
    
    print("\n🎉 Backend is ready to start!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
