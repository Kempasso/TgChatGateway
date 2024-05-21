from fastapi import APIRouter, Depends
from fastapi.routing import JSONResponse
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.authentication.models import User
from src.apps.authentication.repositories import UserRepository
from src.apps.authentication.services import UserService, check_jwt_token
from src.core import redis_service
from src.core.database import get_session
from fastapi.security import OAuth2PasswordRequestForm
from src.apps.authentication.serializers import UserCreate, Token, TokenData

auth_router = APIRouter()


def get_password_hash(password):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)


@auth_router.post("/register/")
async def register_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    user_repo = UserRepository(session=session)
    if exist_user := await user_repo.first_instance_by_values(username=user.username):
        return JSONResponse(content="User already exists", status_code=400)
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, password=hashed_password)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return JSONResponse(content={"username": new_user.username, "id": new_user.id}, status_code=201)


@auth_router.post("/token", response_model=Token)
async def get_token(form_data: OAuth2PasswordRequestForm = Depends(),
                    session: AsyncSession = Depends(get_session)):
    user_service = UserService(session=session)
    user = await user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        return JSONResponse("Auth credentials are invalid or expired", status_code=401)
    access_token = await user_service.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}



