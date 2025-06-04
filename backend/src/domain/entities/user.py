"""
사용자 엔티티
"""
from sqlalchemy import Column, String, Boolean, DateTime, Enum as SQLAlchemyEnum, ForeignKey, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from config.database import Base
from domain.entities.user_type import UserType

class User(Base):
    __tablename__ = "users"

    uuid = Column(Integer, primary_key=True, autoincrement=True)  # SERIAL PRIMARY KEY
    id = Column(String(36), unique=True, nullable=False)          # UUID, UNIQUE, NOT NULL
    email = Column(String, unique=True, nullable=False, index=True)
    username = Column(String(50), nullable=False)
    hashed_password = Column(String, nullable=False)
    user_type = Column(SQLAlchemyEnum(UserType), nullable=False)
    phone = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # OAuth 관련 필드
    social_provider = Column(String, nullable=True)
    social_id = Column(String, nullable=True)

    # 관계 설정
    business_profile = relationship("BusinessProfile", back_populates="user", uselist=False)

class BusinessProfile(Base):
    __tablename__ = "business_profiles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    users_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    business_name = Column(String(100), nullable=False)
    business_registration_number = Column(String(20), nullable=False, unique=True)
    business_type = Column(String(50), nullable=False)  # 업종
    business_category = Column(String(50), nullable=False)  # 업태
    address = Column(String(200), nullable=False)
    representative_name = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계 설정
    user = relationship("User", back_populates="business_profile")

class EmailVerification(Base):
    __tablename__ = "email_verifications"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, nullable=False, index=True)
    code = Column(String, nullable=False)
    verified = Column(Boolean, default=False)
    verified_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class PasswordReset(Base):
    __tablename__ = "password_resets"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    users_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    token = Column(String, nullable=False, unique=True)
    used = Column(Boolean, default=False)
    used_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 관계 설정
    user = relationship("User", backref="password_resets")
