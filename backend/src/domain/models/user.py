from sqlalchemy import Column, String, DateTime, Enum, Boolean
from sqlalchemy.sql import func
from ..database import Base
import enum

class UserType(str, enum.Enum):
    PERSONAL = "PERSONAL"
    BUSINESS = "BUSINESS"

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=True)
    password_hash = Column(String(100), nullable=False)
    user_type = Column(Enum(UserType), nullable=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 