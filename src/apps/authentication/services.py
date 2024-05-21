from src.apps.authentication.repositories import UserRepository
from passlib.context import CryptContext
from fastapi import Depends
import jwt as pyjwt

from src.apps.authentication.serializers import TokenData
from src.core.settings import oauth2_scheme


class UserService:
    def __init__(self, session):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.session = session
        self.user_repo = UserRepository(self.session)

    async def verify_password(self, password, hashed_password):
        return self.pwd_context.verify(password, hashed_password)

    async def get_user(self, username: str):
        user = await self.user_repo.first_instance_by_values(username=username)
        return user

    async def authenticate_user(self, username: str, password: str):
        user = await self.get_user(username)
        if not user or not await self.verify_password(password, user.password):
            return False
        return user

    async def create_access_token(self, data: dict):
        to_encode = data.copy()
        encoded_jwt = pyjwt.encode(to_encode, '12345', algorithm='HS256')
        return encoded_jwt


async def check_jwt_token(token: str = Depends(oauth2_scheme)):
    payload = pyjwt.decode(token, '12345', algorithms=['HS256'])
    username: str = payload.get("sub")
    if username is None:
        return None
    token_data = TokenData(username=username)
    return token_data
