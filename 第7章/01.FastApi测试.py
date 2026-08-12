import uvicorn
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/books/{book_id}")
def read_book(book_id: int):
    return {"book_id": book_id}

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)