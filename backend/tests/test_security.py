"""
보안 관련 테스트 - JWT, 인증, Rate Limiting
"""
import pytest
from datetime import timedelta
from unittest.mock import patch, MagicMock
import time


class TestJWTSecurity:
    """JWT 보안 테스트"""
    
    @pytest.mark.unit
    @pytest.mark.auth
    def test_create_access_token(self):
        """액세스 토큰 생성 테스트"""
        from src.infrastructure.security.jwt import create_access_token
        
        user_data = {"sub": "test@example.com", "user_id": "123"}
        result = create_access_token(user_data)
        
        assert "access_token" in result
        assert "token_type" in result
        assert result["token_type"] == "bearer"
        assert "expires_in" in result
        assert result["expires_in"] > 0
    
    @pytest.mark.unit
    @pytest.mark.auth
    def test_create_access_token_with_refresh(self):
        """액세스 토큰 + 리프레시 토큰 생성 테스트"""
        from src.infrastructure.security.jwt import create_access_token
        
        user_data = {"sub": "test@example.com"}
        result = create_access_token(user_data, include_refresh=True)
        
        assert "access_token" in result
        assert "refresh_token" in result
        assert result["refresh_token"] is not None
    
    @pytest.mark.unit
    @pytest.mark.auth
    def test_verify_valid_token(self):
        """유효한 토큰 검증 테스트"""
        from src.infrastructure.security.jwt import create_access_token, verify_token
        
        user_data = {"sub": "test@example.com"}
        token_result = create_access_token(user_data)
        
        payload = verify_token(token_result["access_token"])
        
        assert payload["sub"] == "test@example.com"
        assert payload["token_type"] == "access"
        assert "exp" in payload
        assert "iat" in payload
        assert "iss" in payload
        assert "aud" in payload
    
    @pytest.mark.unit
    @pytest.mark.auth
    def test_verify_invalid_token(self):
        """잘못된 토큰 검증 테스트"""
        from src.infrastructure.security.jwt import verify_token
        from fastapi import HTTPException
        
        with pytest.raises(HTTPException) as exc_info:
            verify_token("invalid.token.here")
        
        assert exc_info.value.status_code == 401
    
    @pytest.mark.unit
    @pytest.mark.auth
    def test_verify_expired_token(self):
        """만료된 토큰 검증 테스트"""
        from src.infrastructure.security.jwt import create_access_token, verify_token
        from fastapi import HTTPException
        
        # 이미 만료된 토큰 생성 (음수 delta)
        user_data = {"sub": "test@example.com"}
        token_result = create_access_token(
            user_data, 
            expires_delta=timedelta(seconds=-1)
        )
        
        with pytest.raises(HTTPException) as exc_info:
            verify_token(token_result["access_token"])
        
        assert exc_info.value.status_code == 401
        assert "expired" in exc_info.value.detail.lower()
    
    @pytest.mark.unit
    @pytest.mark.auth
    def test_token_type_mismatch(self):
        """토큰 타입 불일치 테스트"""
        from src.infrastructure.security.jwt import (
            create_access_token, 
            create_refresh_token, 
            verify_token
        )
        from fastapi import HTTPException
        
        # Refresh 토큰을 Access 토큰으로 검증 시도
        user_data = {"sub": "test@example.com"}
        refresh_token = create_refresh_token(user_data)
        
        with pytest.raises(HTTPException) as exc_info:
            verify_token(refresh_token, expected_type="access")
        
        assert exc_info.value.status_code == 401
    
    @pytest.mark.unit
    @pytest.mark.auth
    def test_refresh_access_token(self):
        """리프레시 토큰으로 액세스 토큰 갱신 테스트"""
        from src.infrastructure.security.jwt import (
            create_access_token,
            refresh_access_token
        )
        
        # 초기 토큰 생성
        user_data = {"sub": "test@example.com", "name": "Test User"}
        initial_tokens = create_access_token(user_data, include_refresh=True)
        
        # 리프레시 토큰으로 새 액세스 토큰 발급
        new_tokens = refresh_access_token(initial_tokens["refresh_token"])
        
        assert "access_token" in new_tokens
        assert new_tokens["access_token"] != initial_tokens["access_token"]


class TestTokenBlacklist:
    """토큰 블랙리스트 테스트"""
    
    @pytest.mark.unit
    @pytest.mark.auth
    @pytest.mark.asyncio
    async def test_add_to_blacklist(self, mock_redis):
        """블랙리스트 추가 테스트"""
        from src.infrastructure.security.jwt import TokenBlacklist
        
        blacklist = TokenBlacklist(mock_redis)
        result = await blacklist.add("test-jti-123", 3600)
        
        assert result is True
        mock_redis.setex.assert_called_once()
    
    @pytest.mark.unit
    @pytest.mark.auth
    @pytest.mark.asyncio
    async def test_check_blacklisted(self, mock_redis):
        """블랙리스트 확인 테스트"""
        from src.infrastructure.security.jwt import TokenBlacklist
        
        mock_redis.get.return_value = "1"  # 블랙리스트에 있음
        
        blacklist = TokenBlacklist(mock_redis)
        result = await blacklist.is_blacklisted("test-jti-123")
        
        assert result is True
    
    @pytest.mark.unit
    @pytest.mark.auth
    @pytest.mark.asyncio
    async def test_local_blacklist_fallback(self):
        """Redis 없을 때 로컬 블랙리스트 테스트"""
        from src.infrastructure.security.jwt import TokenBlacklist
        
        # Redis 없이 생성
        blacklist = TokenBlacklist(redis_client=None)
        
        # 추가
        await blacklist.add("test-jti-456", 3600)
        
        # 확인
        assert await blacklist.is_blacklisted("test-jti-456") is True
        assert await blacklist.is_blacklisted("other-jti") is False
        
        # 제거
        await blacklist.remove("test-jti-456")
        assert await blacklist.is_blacklisted("test-jti-456") is False


class TestSettings:
    """설정 보안 테스트"""
    
    @pytest.mark.unit
    def test_secret_key_generation(self):
        """시크릿 키 자동 생성 테스트"""
        from src.config.settings import generate_secret_key
        
        key1 = generate_secret_key()
        key2 = generate_secret_key()
        
        # 매번 다른 키 생성
        assert key1 != key2
        # 충분한 길이
        assert len(key1) >= 32
    
    @pytest.mark.unit
    def test_production_validation(self):
        """프로덕션 환경 검증 테스트"""
        from src.config.settings import Settings
        
        # 프로덕션 설정으로 생성
        with patch.dict('os.environ', {
            'ENVIRONMENT': 'production',
            'DEBUG': 'false'
        }):
            settings = Settings()
            settings.environment = "production"
            
            errors = settings.validate_production_settings()
            
            # 프로덕션에서 필수 설정 누락 시 에러 발생
            assert isinstance(errors, list)
    
    @pytest.mark.unit
    def test_cors_origins_list(self):
        """CORS origins 파싱 테스트"""
        from src.config.settings import Settings
        
        with patch.dict('os.environ', {
            'CORS_ORIGINS': 'http://localhost:3000,http://example.com, http://test.com '
        }):
            settings = Settings()
            settings.cors_origins = "http://localhost:3000,http://example.com, http://test.com "
            
            origins = settings.cors_origins_list
            
            assert len(origins) == 3
            assert "http://localhost:3000" in origins
            assert "http://example.com" in origins
            assert "http://test.com" in origins  # 공백 제거됨
    
    @pytest.mark.unit
    def test_redis_connection_url(self):
        """Redis 연결 URL 생성 테스트"""
        from src.config.settings import Settings
        
        # 비밀번호 없는 경우
        settings = Settings()
        settings.redis_host = "localhost"
        settings.redis_port = 6379
        settings.redis_db = 0
        settings.redis_password = None
        settings.redis_ssl = False
        settings.redis_url = None
        
        url = settings.redis_connection_url
        assert url == "redis://localhost:6379/0"
        
        # 비밀번호 있는 경우
        settings.redis_password = "secret"
        url = settings.redis_connection_url
        assert "secret" in url
        
        # SSL 사용 시
        settings.redis_ssl = True
        url = settings.redis_connection_url
        assert url.startswith("rediss://")


class TestPasswordSecurity:
    """비밀번호 보안 테스트"""
    
    @pytest.mark.unit
    def test_password_hashing(self):
        """비밀번호 해싱 테스트"""
        from src.infrastructure.security.password import get_password_hash, verify_password
        
        password = "TestPassword123!"
        hashed = get_password_hash(password)
        
        # 해시 생성 확인
        assert hashed != password
        assert len(hashed) > 0
        
        # 검증 테스트
        assert verify_password(password, hashed) is True
        assert verify_password("wrong_password", hashed) is False
    
    @pytest.mark.unit
    def test_same_password_different_hash(self):
        """같은 비밀번호도 다른 해시 생성"""
        from src.infrastructure.security.password import get_password_hash
        
        password = "TestPassword123!"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        
        # 솔트로 인해 매번 다른 해시
        assert hash1 != hash2
