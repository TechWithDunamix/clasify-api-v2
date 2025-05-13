from hmac import new
import re
from nexios.routing import Router
from nexios.http import Request, Response
from dto.responses import Success200, Error400,Error401
from ._models import CreateUser, LoginUser, LoginResponse, UserSession, RefreshTokenRequest
from models.user import User
from nexios.auth.backends.jwt import create_jwt, decode_jwt
from nexios.auth.decorator import auth
from datetime import datetime, timedelta
from pytz import timezone
from nexios import Depend
from .deps import get_user_session
auth_router = Router(prefix="/auth", tags=["Auth"])

@auth_router.post("/create-user", 
                 request_model=CreateUser,
                 summary = "Create User",
                 responses={
                     200: Success200,
                     400: Error400
                 })
async def creare_user(request: Request, response: Response):
    request_data = await request.json
    user_data = CreateUser(**request_data)
    if await User.filter(username=user_data.username).exists():
        return response.json({"message": "User already exists", "detail": {"username": "User already exists"}}, status_code=400)
    if await User.filter(email=user_data.email).exists():
        return response.json({"message": "User already exists", "detail": {"email": "User already exists"}}, status_code=400)
    await User.create_user(**user_data.dict())
    
    return {"message": "User created successfully"}


@auth_router.post("/login", 
                 request_model=LoginUser,
                 summary = "Login User",
                 responses={
                     200: LoginResponse,
                     400: Error400
                 })
async def login(request: Request, response: Response):
    request_data = await request.json
    login_data = LoginUser(**request_data)
    user = await User.filter(email=login_data.email).first()
    if not user:
        return response.json({"message": "Invalid credentials", "detail": {"username": "Invalid credentials"}}, status_code=400)
    if not user.verify_password(login_data.password):
        return response.json({"message": "Invalid credentials", "detail": {"password": "Invalid credentials"}}, status_code=400)
    return {
        "access_token": create_jwt({"user_id": str(user.id), "exp": datetime.now(timezone('UTC')) + timedelta(days=1)}),
        "refresh_token": create_jwt({"user_id": str(user.id), "exp": datetime.now(timezone('UTC')) + timedelta(days=7)})
    }


@auth_router.post("/logout", 
                 summary = "Logout User",
                 deprecated=True,
                 responses={
                     200: Success200,
                     400: Error400
                 })
async def logout(request: Request, response: Response):
    return {"message": "Logged out successfully"}


@auth_router.post("/refresh-token", 
                 summary = "Refresh Token",
                 security=[{"bearerAuth": []}],
                 request_model=RefreshTokenRequest,
                 responses={
                     200: LoginResponse,
                     400: Error400
                 })


async def refresh_token(request: Request, response: Response):
    request_data = await request.json
    data = RefreshTokenRequest(**request_data)
    payload = decode_jwt(data.refresh_token)
    new_acess_token = create_jwt({"user_id": payload["user_id"], "exp": datetime.now(timezone('UTC')) + timedelta(days=1)})
    new_refresh_token = create_jwt({"user_id": payload["user_id"], "exp": datetime.now(timezone('UTC')) + timedelta(days=7)})
    return {
        "access_token": new_acess_token,
        "refresh_token": new_refresh_token
    }

@auth_router.post("/session", 
                 summary = "Session",
                 security=[{"bearerAuth": []}],
                 responses={
                     200: UserSession,
                     401: Error401
                 })
@auth(["jwt"])
async def session(request: Request, response: Response, session = Depend(get_user_session)):
    return session