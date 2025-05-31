from pydantic import BaseModel, EmailStr, constr

class LoginRequest(BaseModel):
    user_id: str  # Changed from username to user_id for ID-based login
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    user_type: str

class RegisterPersonalRequest(BaseModel):
    username: constr(min_length=4, max_length=50)
    email: EmailStr
    password: constr(min_length=8)

class RegisterBusinessRequest(BaseModel):
    username: constr(min_length=4, max_length=50)
    email: EmailStr
    password: constr(min_length=8)

class RegisterResponse(BaseModel):
    id: str
    username: str
    email: str
    user_type: str