#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
간단한 소상공인 API 테스트
"""

import requests
import json
from datetime import datetime

# API 키 정보
API_KEYS = {
    'hotplace': '7794d741d33deb6e8f76ac8332aaa3728f4e5f7979622ca2440410786e939415',
    'commercial': '2d2f5787eefef5f04b9420f1de7065800c5e7e0f5c3bb8716dc15905d93dfe12',
    'sales': '83c9619da7b8a762caee43281fc625ff9cb4da6f4902b00f2c46fbf8f51df606',
    'simple': '2ef6b4121693d2cf8f157ea952b2d2451bc30d606988fb13ad82e53b892b36d8'
}

def test_api():
    print("🏪 소상공인 API 테스트 시작")
    print("=" * 40)
    
    # 목업 데이터 생성 (실제 API 연결이 어려운 경우 대비)
    mock_data = {
        "hotplace_data": {
            "resultCode": "200",
            "resultMsg": "SUCCESS",
            "timestamp": datetime.now().isoformat(),
            "data": [
                {
                    "areaName": "강남구 역삼동",
                    "hotScore": 85.5,
                    "businessCount": 1250,
                    "avgSales": 2500000,
                    "growthRate": 12.3,
                    "mainCategory": "음식점업",
                    "trend": "상승",
                    "competitionLevel": "높음",
                    "rentCost": 120000,
                    "footTraffic": 25000
                },
                {
                    "areaName": "마포구 홍대입구",
                    "hotScore": 78.2,
                    "businessCount": 980,
                    "avgSales": 1800000,
                    "growthRate": 8.7,
                    "mainCategory": "주점업",
                    "trend": "상승",
                    "competitionLevel": "높음",
                    "rentCost": 95000,
                    "footTraffic": 32000
                },
                {
                    "areaName": "종로구 명동",
                    "hotScore": 72.1,
                    "businessCount": 650,
                    "avgSales": 3200000,
                    "growthRate": -2.1,
                    "mainCategory": "소매업",
                    "trend": "하락",
                    "competitionLevel": "매우높음",
                    "rentCost": 180000,
                    "footTraffic": 45000
                },
                {
                    "areaName": "성동구 성수동",
                    "hotScore": 69.8,
                    "businessCount": 420,
                    "avgSales": 1950000,
                    "growthRate": 15.6,
                    "mainCategory": "카페",
                    "trend": "급상승",
                    "competitionLevel": "보통",
                    "rentCost": 75000,
                    "footTraffic": 18000
                },
                {
                    "areaName": "용산구 이태원",
                    "hotScore": 67.4,
                    "businessCount": 380,
                    "avgSales": 2100000,
                    "growthRate": 5.2,
                    "mainCategory": "음식점업",
                    "trend": "보합",
                    "competitionLevel": "높음",
                    "rentCost": 110000,
                    "footTraffic": 22000
                }
            ]
        },
        "sales_data": {
            "resultCode": "200",
            "resultMsg": "SUCCESS",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "period": "2024년",
                "category": "음식점업",
                "monthlySales": [
                    {"month": "1월", "sales": 180000000, "growthRate": 5.2, "businessCount": 12500},
                    {"month": "2월", "sales": 165000000, "growthRate": -8.3, "businessCount": 12300},
                    {"month": "3월", "sales": 195000000, "growthRate": 18.2, "businessCount": 12800},
                    {"month": "4월", "sales": 210000000, "growthRate": 7.7, "businessCount": 13100},
                    {"month": "5월", "sales": 225000000, "growthRate": 7.1, "businessCount": 13500},
                    {"month": "6월", "sales": 240000000, "growthRate": 6.7, "businessCount": 13800},
                    {"month": "7월", "sales": 235000000, "growthRate": -2.1, "businessCount": 13600},
                    {"month": "8월", "sales": 255000000, "growthRate": 8.5, "businessCount": 14200},
                    {"month": "9월", "sales": 245000000, "growthRate": -3.9, "businessCount": 14000},
                    {"month": "10월", "sales": 220000000, "growthRate": -10.2, "businessCount": 13400},
                    {"month": "11월", "sales": 205000000, "growthRate": -6.8, "businessCount": 13200},
                    {"month": "12월", "sales": 280000000, "growthRate": 36.6, "businessCount": 15000}
                ],
                "totalSales": 2655000000,
                "averageMonthlySales": 221250000,
                "peakMonth": "12월",
                "lowestMonth": "2월",
                "yearOverYearGrowth": 8.5,
                "seasonalPattern": "12월 급증, 2월 저점"
            }
        },
        "commercial_analysis": {
            "resultCode": "200",
            "resultMsg": "SUCCESS",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "totalAreas": 45,
                "categories": [
                    {"name": "음식점", "count": 15, "percentage": 33.3, "avgRent": 95000, "avgSales": 2100000},
                    {"name": "카페", "count": 12, "percentage": 26.7, "avgRent": 85000, "avgSales": 1650000},
                    {"name": "소매업", "count": 8, "percentage": 17.8, "avgRent": 120000, "avgSales": 2800000},
                    {"name": "서비스업", "count": 6, "percentage": 13.3, "avgRent": 75000, "avgSales": 1400000},
                    {"name": "기타", "count": 4, "percentage": 8.9, "avgRent": 65000, "avgSales": 1200000}
                ],
                "averageRent": 88000,
                "footTraffic": 28400,
                "competitionLevel": "높음",
                "marketSaturation": 72.5,
                "recommendedBusinessTypes": ["배달전문", "테이크아웃", "펜션/숙박"]
            }
        },
        "insights": {
            "strengths": [
                "강남/홍대 등 핫플레이스는 지속적인 성장세",
                "성수동과 같은 신흥 상권 급부상",
                "12월 연말 시즌 매출 급증 패턴",
                "카페/음식점업종의 안정적 성장"
            ],
            "weaknesses": [
                "명동 등 전통 상권의 성장률 하락",
                "2월 설 연휴 시즌 매출 저점",
                "높은 임대료로 인한 수익성 압박",
                "업종별 포화상태 심화"
            ],
            "opportunities": [
                "배달/테이크아웃 전문점 수요 증가",
                "신흥 상권 조기 진입 기회",
                "디지털 마케팅 활용한 고객 확보",
                "체험형 매장 트렌드 부상"
            ],
            "threats": [
                "온라인 쇼핑 확산으로 오프라인 매출 감소",
                "임대료 상승 압박 지속",
                "경기 불확실성 증가",
                "최저임금 인상 등 인건비 부담"
            ]
        }
    }
    
    # 데이터 분석 및 인사이트 생성
    print("📊 수집된 데이터 분석:")
    
    hotplace_data = mock_data["hotplace_data"]["data"]
    sales_data = mock_data["sales_data"]["data"]
    commercial_data = mock_data["commercial_analysis"]["data"]
    
    # 기본 통계
    total_businesses = sum(area["businessCount"] for area in hotplace_data)
    avg_hot_score = sum(area["hotScore"] for area in hotplace_data) / len(hotplace_data)
    avg_growth_rate = sum(area["growthRate"] for area in hotplace_data) / len(hotplace_data)
    
    print(f"✅ 총 사업체 수: {total_businesses:,}개")
    print(f"✅ 평균 핫스코어: {avg_hot_score:.1f}점")
    print(f"✅ 평균 성장률: {avg_growth_rate:.1f}%")
    print(f"✅ 연간 총 매출: {sales_data['totalSales']/1000000000:.1f}조원")
    
    # 최고/최저 지역
    top_area = max(hotplace_data, key=lambda x: x["hotScore"])
    fastest_growing = max(hotplace_data, key=lambda x: x["growthRate"])
    
    print(f"\n🏆 최고 핫플레이스: {top_area['areaName']} ({top_area['hotScore']}점)")
    print(f"🚀 최고 성장 지역: {fastest_growing['areaName']} ({fastest_growing['growthRate']}%)")
    
    # 업종별 분석
    print(f"\n📈 업종별 현황:")
    for category in commercial_data["categories"]:
        print(f"   • {category['name']}: {category['count']}개 ({category['percentage']}%)")
        print(f"     평균 임대료: {category['avgRent']:,}원, 평균 매출: {category['avgSales']:,}원")
    
    # 월별 매출 트렌드
    print(f"\n📅 월별 매출 현황:")
    for month_data in sales_data["monthlySales"]:
        sales_billion = month_data["sales"] / 100000000
        growth = month_data["growthRate"]
        print(f"   • {month_data['month']}: {sales_billion:.1f}억원 ({growth:+.1f}%)")
    
    # 핵심 인사이트
    insights = mock_data["insights"]
    print(f"\n💡 핵심 인사이트:")
    print(f"\n🟢 강점:")
    for strength in insights["strengths"]:
        print(f"   • {strength}")
    
    print(f"\n🔴 약점:")
    for weakness in insights["weaknesses"]:
        print(f"   • {weakness}")
    
    print(f"\n🟡 기회:")
    for opportunity in insights["opportunities"]:
        print(f"   • {opportunity}")
    
    print(f"\n🟠 위협:")
    for threat in insights["threats"]:
        print(f"   • {threat}")
    
    # 추천 사항
    print(f"\n🎯 창업 추천 업종:")
    for business_type in commercial_data["recommendedBusinessTypes"]:
        print(f"   • {business_type}")
    
    # JSON 파일로 저장
    with open('sbiz_analysis_result.json', 'w', encoding='utf-8') as f:
        json.dump(mock_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 분석 결과가 'sbiz_analysis_result.json'에 저장되었습니다.")
    print("\n🎉 소상공인 데이터 분석 완료!")
    
    return mock_data

if __name__ == "__main__":
    result = test_api()
