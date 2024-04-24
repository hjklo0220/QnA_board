from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from api import question, answer, user

app = FastAPI()
app.include_router(question.router)
app.include_router(answer.router)
app.include_router(user.router)
app.mount("/assets", StaticFiles(directory="frontend/dist/assets"))

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
def index():
    return FileResponse("frontend/dist/index.html")