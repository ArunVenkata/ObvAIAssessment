from fastapi import Depends, HTTPException, status

from datetime import timedelta
from sqlalchemy.orm import Session
from ProjectMain.database import get_db
from auth.utils import authenticate_user, create_access_token, get_password_hash
from utils.base_view import APIView
from ProjectMain import settings
from auth.schemas import LoginRequest, UserModel
from auth.models import User


class AuthRegisterView(APIView):

    @classmethod
    async def post(cls, user: UserModel, db: Session = Depends(get_db)):
        print(user, "USER")
        db_user = db.query(User).filter(User.username == user.username).first()
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered",
            )
        hashed_password = get_password_hash(user.password)
        db_user = User(
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            hashed_password=hashed_password,
            disabled=False,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"message": "User created successfully"}
    

class AuthLoginView(APIView):
    
    
    @classmethod
    async def post(cls, login_request: LoginRequest, db: Session = Depends(get_db)):
        user = authenticate_user(db, login_request.username, login_request.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return {"access_token": access_token, "token_type": "bearer"}
