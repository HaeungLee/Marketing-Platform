#!/usr/bin/env python3
import asyncio
import aiohttp
import json
import time

BASE_URL = 'http://localhost:8000'

async def test_api():
    async with aiohttp.ClientSession() as session:
        print('🌟 API 통합 테스트 시작\n')
        
        # 1. 서버 상태 확인
        print('1️⃣ 서버 상태 확인')
        try:
            async with session.get(f'{BASE_URL}/') as resp:
                if resp.status == 200:
                    print('✅ 서버가 정상적으로 실행중입니다')
                else:
                    print(f'⚠️ 서버 응답 상태: {resp.status}')
        except Exception as e:
            print(f'❌ 서버 연결 실패: {e}')
            return
        
        print()
        
        # 2. Business Stores API 테스트
        print('2️⃣ Business Stores API 테스트')
        
        # 2-1. 전체 상가 조회
        print('📋 전체 상가 조회')
        try:
            async with session.get(f'{BASE_URL}/api/v1/business-stores') as resp:
                if resp.status == 200:
                    data = await resp.json()
                    print(f'✅ 총 {len(data)}개 상가 조회 성공')
                    if data:
                        print(f'   첫 번째 상가: {data[0]["store_name"]}')
                else:
                    print(f'❌ 조회 실패: {resp.status}')
                    text = await resp.text()
                    print(f'   응답: {text[:200]}...')
        except Exception as e:
            print(f'❌ 요청 실패: {e}')
        
        print()
        
        # 2-2. 지역별 상가 조회 (강남구)
        print('🏢 지역별 상가 조회 (강남구)')
        try:
            params = {'sigungu_name': '강남구'}
            async with session.get(f'{BASE_URL}/api/v1/business-stores', params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    print(f'✅ 강남구 상가 {len(data)}개 조회 성공')
                    for store in data[:3]:  # 처음 3개만 출력
                        print(f'   - {store["store_name"]} ({store["business_name"]})')
                else:
                    print(f'❌ 조회 실패: {resp.status}')
        except Exception as e:
            print(f'❌ 요청 실패: {e}')
        
        print()
        
        # 2-3. 업종별 상가 조회 (카페)
        print('☕ 업종별 상가 조회 (카페)')
        try:
            params = {'business_name': '카페'}
            async with session.get(f'{BASE_URL}/api/v1/business-stores', params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    print(f'✅ 카페 {len(data)}개 조회 성공')
                    for store in data:
                        print(f'   - {store["store_name"]} ({store["sigungu_name"]} {store["dong_name"]})')
                else:
                    print(f'❌ 조회 실패: {resp.status}')
        except Exception as e:
            print(f'❌ 요청 실패: {e}')
        
        print()
        
        # 2-4. 위치 기반 상가 조회 (강남역 근처)
        print('📍 위치 기반 상가 조회 (강남역 근처 500m)')
        try:
            params = {
                'latitude': 37.4979,
                'longitude': 127.0276,
                'radius': 500
            }
            async with session.get(f'{BASE_URL}/api/v1/business-stores/nearby', params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    print(f'✅ 강남역 근처 상가 {len(data)}개 조회 성공')
                    for store in data:
                        distance = store.get('distance', 'N/A')
                        print(f'   - {store["store_name"]} (거리: {distance}m)')
                else:
                    print(f'❌ 조회 실패: {resp.status}')
                    text = await resp.text()
                    print(f'   응답: {text[:200]}...')
        except Exception as e:
            print(f'❌ 요청 실패: {e}')
        
        print()
        
        # 3. 상가 통계 조회
        print('3️⃣ 상가 통계 조회')
        try:
            async with session.get(f'{BASE_URL}/api/v1/business-stores/stats') as resp:
                if resp.status == 200:
                    data = await resp.json()
                    print('✅ 통계 조회 성공')
                    print(f'   총 상가 수: {data.get("total_stores", "N/A")}')
                    
                    if 'by_business_type' in data:
                        print('   업종별 분포:')
                        for item in data['by_business_type'][:5]:
                            print(f'     - {item["business_name"]}: {item["count"]}개')
                    
                    if 'by_region' in data:
                        print('   지역별 분포:')
                        for item in data['by_region'][:5]:
                            print(f'     - {item["sigungu_name"]}: {item["count"]}개')
                else:
                    print(f'❌ 통계 조회 실패: {resp.status}')
        except Exception as e:
            print(f'❌ 요청 실패: {e}')
        
        print()
        
        # 4. 상권 분석 API 테스트
        print('4️⃣ 상권 분석 API 테스트')
        try:
            analysis_data = {
                'latitude': 37.4979,
                'longitude': 127.0276,
                'radius': 1000,
                'business_type': '카페'
            }
            async with session.post(f'{BASE_URL}/api/v1/business-stores/analyze', 
                                   json=analysis_data) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    print('✅ 상권 분석 성공')
                    print(f'   분석 지역: {data.get("location", "N/A")}')
                    print(f'   반경: {data.get("radius", "N/A")}m')
                    print(f'   분석 업종: {data.get("business_type", "N/A")}')
                    print(f'   경쟁업체 수: {data.get("competitor_count", "N/A")}개')
                    
                    if 'insights' in data:
                        print('   인사이트:')
                        for insight in data['insights'][:3]:
                            print(f'     - {insight}')
                else:
                    print(f'❌ 상권 분석 실패: {resp.status}')
                    text = await resp.text()
                    print(f'   응답: {text[:200]}...')
        except Exception as e:
            print(f'❌ 요청 실패: {e}')
        
        print()
        print('🎉 API 테스트 완료!')

if __name__ == "__main__":
    asyncio.run(test_api()) 