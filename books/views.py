from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import Optional, Union
from utils import safe_convert
from utils.base_view import APIModelView
from .schemas import BookBase, BookUpdate
from .models import Book
from ProjectMain.database import get_db


class BookModelView(APIModelView):
    """
    CRUD for Books
    """

    @classmethod
    async def get(
        cls,
        id: Optional[int] = None,
        db: Session = Depends(get_db),
        limit: Union[int, str, None] = None,
        offset: Union[int, str, None] = None,
    ):
        # Only devs will mess with types so no point providing specific error handling
        limit = safe_convert(limit, to_type=int, default=10)  
        offset = safe_convert(offset, to_type=int, default=0)

        if isinstance(id, int):
            book = db.query(Book).filter(Book.id == id).first()
            if not book:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
                )
            return {
                "data": book,
                "message": "Book retrieved successfully",
            }
        books = db.query(Book).offset(offset).limit(limit).all()
        return {
            "data": books,
            "message": "Books retrieved successfully",
            "metadata": {"limit": limit, "offset": offset},
        }

    @classmethod
    async def post(cls, book: BookBase, db: Session = Depends(get_db)):
        db_book = Book(**book.model_dump())
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return {"data": db_book, "message": "Book created successfully"}

    @classmethod
    async def put(cls, id: int, book: BookBase, db: Session = Depends(get_db)):
        db_book = db.query(Book).filter(Book.id == id).first()
        if not db_book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
            )
        # Replace all fields
        for key, value in book.model_dump().items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
        return {"data": db_book, "message": "Book updated successfully"}

    @classmethod
    async def patch(cls, id: int, book: BookUpdate, db: Session = Depends(get_db)):
        db_book = db.query(Book).filter(Book.id == id).first()
        if not db_book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
            )
        # Update only provided fields
        update_data = book.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided for update",
            )
        for key, value in update_data.items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
        return {"data": db_book, "message": "Book partially updated successfully"}

    @classmethod
    async def delete(cls, id: int, db: Session = Depends(get_db)):
        db_book = db.query(Book).filter(Book.id == id).first()
        if not db_book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
            )
        db.delete(db_book)
        db.commit()
        return {"message": "Book deleted successfully"}
