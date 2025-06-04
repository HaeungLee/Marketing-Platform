"""
데이터베이스 초기화 스크립트
"""
from config.database import Base, engine
from domain.entities.user import User, BusinessProfile, EmailVerification, PasswordReset

def init_db():
    """데이터베이스 테이블 생성"""
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    print("Creating database tables...")
    init_db()
    print("Database tables created successfully!") 