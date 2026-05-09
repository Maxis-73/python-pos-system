from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.core.database import get_db
from app.core.security import hash_password, create_access_token, verify_password
from .schemas import LoginRequest, RegisterRequest, LoginResponse
from .model import User
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=LoginResponse)
async def register(data: RegisterRequest, db=Depends(get_db)):
    try:
        # 1. Verify email exists
        user_exists = db.query(User).filter(User.email == data.email).first()
        if user_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        
        # 2. Verify password
        if data.password != data.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The passwords do not match",
            )
        
        # 3. Hash password
        password_hash = hash_password(data.password)

        # 4. Save user
        user_db = User(
            email = data.email,
            hashed_password = password_hash,
            full_name = data.full_name
        )
        db.add(user_db)
        db.commit()
        db.refresh(user_db)

        return LoginResponse(message="User registered successfully")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while trying to register a user",
        )


@router.post("/login", response_model=LoginResponse)
async def login(credentials: LoginRequest, response: Response, db=Depends(get_db)):
    try:
        # 1. Verify email exists
        user_exists = db.query(User).filter(User.email == credentials.email).first()
        if not user_exists:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="This email is not registered"
            )

        # 2. Verify password
        if not verify_password(credentials.password, user_exists.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="The password is not correct, please verify it"
            )

        # 3. Create and save access token
        access_token = create_access_token({"sub": str(user_exists.id)})
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True
        )

        # 4. Response
        return LoginResponse(message="User Login Successfully")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while trying to login",
        )