from fastapi import Body,FastAPI

app = FastAPI() #this is going to be a fastapi application

BOOKS = [
    {'title':'TITLE1', 'author':'author1', 'category':'science'},
    {'title':'TITLE2', 'author':'author2', 'category':'science'},
    {'title':'TITLE3', 'author':'author3', 'category':'fiction'},
    {'title':'TITLE4', 'author':'author4', 'category':'math'},
    {'title':'TITLE6', 'author':'author2', 'category':'math'}
]
@app.get("")
async def read_all_books():
    return BOOKS

@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book
@app.get("/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

#for making new entities
@app.post("/books/create_book")
async def create_book(new_book = Body()):
    BOOKS.append(new_book)

#for editing entities that already exist
@app.put("/books/update_book")
async def update_book(updated_book = Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book

@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break
@app.get("/books/byauthor/{author}")
async def read_author_by_query(author: str):
    books = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books.append(book)
    return books

