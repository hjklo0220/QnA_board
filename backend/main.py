from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api import question, answer, user

app = FastAPI()
app.include_router(question.router)
app.include_router(answer.router)
app.include_router(user.router)

origins = [
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check_handler():
    return {"status": "ok"}

@app.get("/hello")
def hello_handler():
    return {"message": "Hello World"}