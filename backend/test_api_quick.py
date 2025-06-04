#!/usr/bin/env python3
"""
Simple test script to verify the API fixes are working
"""

import requests
import json
import sys

def test_api_endpoint(url, description):
    """Test a single API endpoint"""
    try:
        print(f"\n🧪 Testing: {description}")
        print(f"URL: {url}")
        
        response = requests.get(url, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ SUCCESS - API returned 200")
            
            # Print key information
            if 'error' in data:
                print(f"⚠️  API includes error message: {data['error']}")
            else:
                print("✅ No error message in response")
                
            # Show first few keys of response
            if isinstance(data, dict):
                keys = list(data.keys())[:5]
                print(f"Response keys: {keys}")
                
        else:
            print(f"❌ FAILED - Status: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            
    except requests.exceptions.ConnectionError:
        print("❌ FAILED - Cannot connect to server (is it running?)")
        return False
    except Exception as e:
        print(f"❌ FAILED - Error: {e}")
        return False
        
    return response.status_code == 200

def main():
    """Test all the insights APIs"""
    
    base_url = "http://localhost:8000/api/v1/insights"
    
    # Test endpoints
    tests = [
        (f"{base_url}/marketing-timing?target_age=30대&business_type=카페", "Marketing Timing API"),
        (f"{base_url}/target-customer?business_type=카페&region=강남", "Target Customer Analysis API"),
        (f"{base_url}/optimal-location?business_type=카페&budget=50000000&target_age=30대", "Optimal Location API"),
    ]
    
    print("🚀 Starting API Tests...")
    print("=" * 60)
    
    success_count = 0
    total_count = len(tests)
    
    for url, description in tests:
        if test_api_endpoint(url, description):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {success_count}/{total_count} APIs working")
    
    if success_count == total_count:
        print("🎉 All APIs are working correctly!")
    else:
        print("⚠️  Some APIs need attention")
        
    return success_count == total_count

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
