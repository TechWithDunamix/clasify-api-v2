from pydantic import BaseModel, EmailStr
class CreateUser(BaseModel):
    full_name: str
    username: str
    email: EmailStr
    password: str


class LoginUser(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str


class UserSession(BaseModel):
    user_id: str
    profile_image: str
    full_name: str
    username: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str