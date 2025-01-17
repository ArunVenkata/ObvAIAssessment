# middleware.py

from fastapi import Request, status
from jose import JWTError, jwt
from ProjectMain import settings
from utils.base_response import json_error_response

async def auth_middleware(request: Request, call_next):
    if request.url.path in ["/auth/register", "/auth/login", "/docs", "/openapi.json"]:
        return await call_next(request)
    
    token = request.headers.get("Authorization")
    if token is None:
        return json_error_response(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    try:
        token = token.split(" ")[1]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.AUTH_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return json_error_response(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )
    except JWTError:
        return json_error_response(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    request.state.user = username
    response = await call_next(request)
    return response