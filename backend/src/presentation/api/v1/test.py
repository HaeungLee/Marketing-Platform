from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/test-error")
async def test_error():
    """모니터링 테스트를 위한 의도적 에러 발생"""
    raise HTTPException(
        status_code=500,
        detail="This is a test error for monitoring!"
    )
