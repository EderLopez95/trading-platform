from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=24)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=24)

class UpdateTelegramRequest(BaseModel):
    telegram_token: str
    telegram_chat_id: str

class AuthResponse(BaseModel):
    user_id: str
    token: str

class UserResponse(BaseModel):
    user_id: str

class CurrentUserResponse(BaseModel):
    id: str
    email: str
    is_active: bool
