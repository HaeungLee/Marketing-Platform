from datetime import datetime, timedelta
from typing import Optional, Tuple
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from ..models.user import User, UserType
from ..repositories.user_repository import UserRepository
from ..exceptions.auth_exception import (
    AuthenticationError,
    InvalidCredentialsError,
    UserNotFoundError,
)

# JWT 설정
SECRET_KEY = "your-secret-key"  # 실제 운영 환경에서는 환경 변수로 관리
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def create_access_token(self, user: User, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = {
            "sub": user.id,
            "user_type": user.user_type.value
        }
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def authenticate_user(self, user_id: str, password: str) -> Tuple[User, str]:
        print(f"Attempting to authenticate user with ID: {user_id}")  # 디버깅용 로그
        user = self.user_repository.get_by_id(user_id)
        if not user:
            print(f"User not found with ID: {user_id}")  # 디버깅용 로그
            raise UserNotFoundError("사용자를 찾을 수 없습니다.")
        if not self.verify_password(password, user.hashed_password):
            print(f"Invalid password for ID: {user_id}")  # 디버깅용 로그
            raise InvalidCredentialsError("아이디 또는 비밀번호가 올바르지 않습니다.")
        print(f"User authenticated successfully with ID: {user_id}")  # 디버깅용 로그
        access_token = self.create_access_token(user)
        return user, access_token

    def register_personal_user(self, username: str, email: str, password: str) -> User:
        # 이메일 중복 확인
        if self.user_repository.get_by_email(email):
            raise AuthenticationError("이미 등록된 이메일입니다.")
        
        # 아이디 중복 확인
        if self.user_repository.get_by_username(username):
            raise AuthenticationError("이미 사용 중인 아이디입니다.")

        hashed_password = self.get_password_hash(password)
        user = User(
            username=username,
            email=email,
            password_hash=hashed_password,
            user_type=UserType.PERSONAL
        )
        return self.user_repository.create(user)

    def register_business_user(self, username: str, email: str, password: str) -> User:
        # 이메일 중복 확인
        if self.user_repository.get_by_email(email):
            raise AuthenticationError("이미 등록된 이메일입니다.")
        
        # 아이디 중복 확인
        if self.user_repository.get_by_username(username):
            raise AuthenticationError("이미 사용 중인 아이디입니다.")

        hashed_password = self.get_password_hash(password)
        user = User(
            username=username,
            email=email,
            password_hash=hashed_password,
            user_type=UserType.BUSINESS
        )
        return self.user_repository.create(user)