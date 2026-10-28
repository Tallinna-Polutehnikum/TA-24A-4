from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.database import engine
from backend.models import Genre, Movie
from sqlalchemy.orm import selectinload
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

class MovieResponse(BaseModel):
    id: int
    name: str
    genres: list[Genre]


@app.get("/movies", response_model=list[MovieResponse])
def get_movies() -> list[MovieResponse]:
    with Session(engine) as session:
        statement = select(Movie).options(selectinload(Movie.genres))
        movies = session.exec(statement).all()

        return [to_movie_response(movie) for movie in movies]


@app.get("/movies/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int) -> MovieResponse:
    with Session(engine) as session:
        movie = session.get(Movie, movie_id)

        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")

        return to_movie_response(movie)


def to_movie_response(movie: Movie) -> MovieResponse:
    return MovieResponse(
        id=movie.id,
        name=movie.name,
        genres=[movie_genre.genre for movie_genre in movie.genres],
    )