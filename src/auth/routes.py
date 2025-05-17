from fastapi import APIRouter, HTTPException, status

from src.auth.schemas import Login, Refresh, Token
from src.auth.security.passwords import verify_password
from src.auth.security.schemas import TokenPayload
from src.auth.security.token import (
    create_tokens,
    verify_refresh_token,
)
from src.users.dependencies import UserServiceDep

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/token", response_model=Token)
async def login(request: Login, user_service: UserServiceDep):
    user = await user_service.get_one_or_none(username=request.username)

    if not user or not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    payload = TokenPayload(id=user.id, role=user.role)
    access_token, refresh_token = create_tokens(payload)
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


@router.post("/refresh", response_model=Token)
async def refresh(request: Refresh) -> Token:
    payload = verify_refresh_token(request.refresh_token)
    access_token, refresh_token = create_tokens(payload)
    return Token(access_token=access_token, refresh_token=refresh_token)
