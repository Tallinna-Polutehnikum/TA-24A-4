from fastapi import FastAPI
from pydantic import BaseModel

from backend.database import engine
from backend.models import Movie
from sqlmodel import Session, select
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Kino API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HealthResponse(BaseModel):
    status: str


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")

@app.get("/movies")
def get_movies():
    with Session(engine) as session:
        statement = select(Movie)
        movies = session.exec(statement).all()

        return movies