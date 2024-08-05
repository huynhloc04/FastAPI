from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status

from app.db.session import get_session
from app.models.user import User, UserInput, UserResponse, TokenSchema
from app.crud.user import create_user, get_user_by_email, get_user
from app.core.deps import get_current_user
from app.core.security import (
    get_hashed_password,
    verify_password,
    create_access_token,
    create_refresh_token,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/signup", response_model=UserResponse, summary="Create a new user.")
async def signup(
    data: UserInput, session: AsyncSession = Depends(get_session)
) -> UserResponse:
    #   Querying database to check user already exist
    user = await get_user_by_email(session=session, email=data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist",
        )
    data.password = get_hashed_password(data.password)
    return await create_user(session=session, user=data)


@router.post(
    "/login",
    response_model=TokenSchema,
    summary="Create access and refresh tokens for user",
)
async def login(
    data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
) -> TokenSchema:
    user = await get_user_by_email(session=session, email=data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    #   Verify user with password
    if not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    return TokenSchema(
        access_token=create_access_token(user.email),
        refresh_token=create_refresh_token(user.email),
    )


@router.get("/me", response_model=User, summary="Get current user.")
async def get_me(user: User = Depends(get_current_user)):
    return user


@router.get(
    "/{id}",
    summary="Get a user.",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
)
async def get_user_route(id: UUID, db: AsyncSession = Depends(get_session)):
    return await get_user(session=db, id=id)
