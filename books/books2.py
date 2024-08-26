
from typing import Optional

from fastapi import FastAPI, Body,Path,Query,HTTPException
from pydantic import BaseModel, Field
from starlette import status
from pydantic.v1.types import OptionalInt

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published: int

    def __init__(self, id, title, author, description, rating, published):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published = published


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create",default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0,lt=6)
    published: int = Field(gt=1990,lt=2025)

    model_config = {
        "json_schema_extra":{
            "example":{
                "title":"A new book",
                "author":"<NAME>",
                "description":"A new description of a book",
                "rating":4,
                "published":2000

            }
        }
    }


BOOKS = [
    Book(1,'Computer Science','codingwithBunte','a very nice book',5,2000),
    Book(2,'Be Fast with FastAPI','codingwithBunte','a great book',5,2001),
    Book(3,'Master Endpoints','codingwithBunte','an Awesome book',5,2002),
    Book(4 ,'HP1','Author 1','Book Description',5,2003),
    Book(5,'HP2','Author 2','Book Description',5,2020),
    Book(6,'HP3','Author 3','Book Description',5,2001)
]



@app.get("", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404,detail="Book not found")
@app.get("/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0,lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return
@app.post("/create-book",status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest): #ova ni treba za validacija dali sme gi dobile tocnite indormacii
    #the code below this comment allows us to take the model and return all the variables from the book model in a dictionary format **book_request.model_dump()
    new_book = Book(**book_request.model_dump()) #converting the request into a Book object
    BOOKS.append(find_book_id(new_book))



def find_book_id(book: Book):

    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    # if len(BOOKS) > 0:
    #     book.id = BOOKS[-1].id +1 #book od tip Book da dobie id edno pogolemo od posledniot element od BOOKS[] listata
    # else:
    #     book.id = 1

    return book

@app.put("/books/update_book",status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404,detail="Book not found")

@app.delete("/books/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)): #za da prima samo nad 0
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            book_changed = True
            BOOKS.pop(i)
            break
    if not book_changed:
        raise HTTPException(status_code=404,detail="Book not found")
@app.get("/books/published/", status_code=status.HTTP_200_OK)
async def read_books_by_published_date(published: int = Query(gt=1990,lt=2025)):
    books_to_return = []
    for i in range(len(BOOKS)):
        if BOOKS[i].published == published:
            books_to_return.append(BOOKS[i])
    return books_to_return

