from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
import csv
from io import TextIOWrapper

app = FastAPI()

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, title, author, genre, cover):
        self.books.append({"title": title, "author": author, "genre": genre, "cover": cover})

library = Library()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "books": library.books})

@app.get("/add_book", response_class=HTMLResponse)
async def add_book(request: Request):
    return templates.TemplateResponse("add_book.html", {"request": request})

@app.post("/add_book", response_class=HTMLResponse)
async def add_book_post(request: Request, title: str = Form(...), author: str = Form(...), genre: str = Form(...), cover: str = Form(...)):
    library.add_book(title, author, genre, cover)
    return RedirectResponse(url="/", status_code=302)

@app.get("/remove_book/{index}", response_class=HTMLResponse)
async def remove_book(request: Request, index: int):
    if 0 <= index < len(library.books):
        library.books.pop(index)
    return RedirectResponse(url="/", status_code=302)

@app.get("/import_books", response_class=HTMLResponse)
async def import_books(request: Request):
    return templates.TemplateResponse("import_books.html", {"request": request})

@app.post("/import_books", response_class=HTMLResponse)
async def import_books_post(request: Request, file: UploadFile = File(...)):
    # Clear existing entries in the library
    library.books = []

    # Read data from the uploaded CSV file and add books to the library
    content = TextIOWrapper(await file.read(), encoding='utf-8')
    reader = csv.reader(content)
    next(reader)  # Skip header row
    for row in reader:
        title, author, genre, cover = row
        library.add_book(title, author, genre, cover)

    return RedirectResponse(url="/", status_code=302)
