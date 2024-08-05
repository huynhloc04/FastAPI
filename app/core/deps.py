from datetime import datetime
from fastapi import Security, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from pydantic import ValidationError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


from app.core.config import settings
from app.db.session import get_session
from app.repository.base import BaseRepository
from app.models.user import User, TokenPayload


security_bearer = HTTPBearer()


async def get_current_user(
    token: HTTPAuthorizationCredentials = Security(security_bearer),
    session: AsyncSession = Depends(get_session),
) -> User:
    try:
        payload = jwt.decode(
            token.credentials, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    #   Get user from parsed token
    user = await BaseRepository(User).get_by_item(session=session, email=token_data.sub)
    return user
