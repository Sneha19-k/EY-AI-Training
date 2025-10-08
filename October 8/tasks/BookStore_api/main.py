from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Create FastAPI instance
app = FastAPI()

# Pydantic model for Book
class Book(BaseModel):
    id: int
    title: str
    author: str
    price: float
    in_stock: bool

# Separate model for update (price and stock only)
class BookUpdate(BaseModel):
    price: float = None
    in_stock: bool = None

# In-memory "database"
books = [
    {"id": 1, "title": "Deep Learning", "author": "Ian Goodfellow", "price": 1200.0, "in_stock": True},
    {"id": 2, "title": "Clean Code", "author": "Robert C. Martin", "price": 450.0, "in_stock": True},
    {"id": 3, "title": "The Pragmatic Programmer", "author": "Andrew Hunt", "price": 550.0, "in_stock": False},
    {"id": 4, "title": "Introduction to Algorithms", "author": "CLRS", "price": 999.0, "in_stock": True},
]

# ---------------- GET: All Books ----------------
@app.get("/books")
def get_all_books():
    return {"books": books}

# ---------------- GET: Book by ID ----------------
@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

# ---------------- POST: Add a New Book ----------------
@app.post("/books", status_code=201)
def add_book(book: Book):
    for b in books:
        if b["id"] == book.id:
            raise HTTPException(status_code=400, detail=f"Book with ID {book.id} already exists.")
    books.append(book.dict())
    return {"message": "Book added successfully", "books": books}

# ---------------- PUT: Update Book ----------------
@app.put("/books/{book_id}")
def update_book(book_id: int, update: BookUpdate):
    for i, book in enumerate(books):
        if book["id"] == book_id:
            if update.price is not None:
                books[i]["price"] = update.price
            if update.in_stock is not None:
                books[i]["in_stock"] = update.in_stock
            return {"message": "Book updated successfully", "book": books[i]}
    raise HTTPException(status_code=404, detail="Book not found")

# ---------------- DELETE: Delete Book ----------------
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for i, book in enumerate(books):
        if book["id"] == book_id:
            deleted = books.pop(i)
            return {"message": "Book deleted successfully", "book": deleted}
    raise HTTPException(status_code=404, detail="Book not found")
