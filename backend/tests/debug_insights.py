import asyncio
import asyncpg
from src.presentation.api.v1.insights import InsightsService

async def test_insights():
    service = InsightsService()
    
    print("=== 타겟 고객 분석 테스트 ===")
    try:
        result = await service.get_target_customer_analysis("카페", "강남")
        print("✅ 성공:", result)
    except Exception as e:
        print(f"❌ 오류: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n=== 입지 추천 테스트 ===")
    try:
        result = await service.get_optimal_location("음식점", 50000000, "30대")
        print("✅ 성공:", result)
    except Exception as e:
        print(f"❌ 오류: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_insights())
