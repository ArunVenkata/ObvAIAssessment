from fastapi import APIRouter, Depends
from typing import Generic, List, Optional, TypeVar
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ProjectMain.database import get_db

T = TypeVar("T", bound=BaseModel)


class APIModelView:
    """
    Custom Implementation for class based views in fastapi
    """

    router: Optional[APIRouter] = None

    http_methods = ["get", "put", "post", "delete", "patch"]
    __item_level_methods = ["get", "put", "delete", "patch"]

    @classmethod
    def as_view(cls, prefix: str, tags: List[str] = None):
        """
        Registers all HTTP methods defined in the class with FastAPI's router.
        """
        if cls.router is None:
            cls.router = APIRouter(prefix=prefix, tags=tags or [])
        for method in cls.http_methods:
            handler = getattr(cls, method, None)
            if handler:
                cls.router.add_api_route(
                    path="",
                    endpoint=handler,
                    methods=[method.upper()],
                )
                if method in cls.__item_level_methods:
                    cls.router.add_api_route(
                        path="/{id}",
                        endpoint=handler,
                        methods=[method.upper()],
                    )
        return cls.router



    

class APIView(Generic[T]):
    router: Optional[APIRouter] = None

    http_methods = ["get", "put", "post", "delete", "patch"]
    __item_level_methods = ["get", "put", "delete", "patch"]

    @classmethod
    def as_view(cls, prefix: str, tags: List[str] = None):
        if cls.router is None:
            cls.router = APIRouter(prefix=prefix, tags=tags or [])
        for method in cls.http_methods:
            handler = getattr(cls, method, None)
            if handler:
                cls.router.add_api_route(
                    path="",
                    endpoint=handler,
                    methods=[method.upper()],
                )
                if method in cls.__item_level_methods:
                    cls.router.add_api_route(
                        path="/{id}",
                        endpoint=handler,
                        methods=[method.upper()],
                    )
        return cls.router

    @classmethod
    async def get(cls, id: Optional[int] = None, db: Session = Depends(get_db)):
        raise NotImplementedError

    @classmethod
    async def post(cls, item: T, db: Session = Depends(get_db)):
        raise NotImplementedError

    @classmethod
    async def put(cls, id: int, item: T, db: Session = Depends(get_db)):
        raise NotImplementedError

    @classmethod
    async def patch(cls, id: int, item: T, db: Session = Depends(get_db)):
        raise NotImplementedError

    @classmethod
    async def delete(cls, id: int, db: Session = Depends(get_db)):
        raise NotImplementedError
