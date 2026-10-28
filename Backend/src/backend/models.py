from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import CheckConstraint, Enum as SAEnum, UniqueConstraint, text
from sqlmodel import Field, Relationship, SQLModel

class SeatType(str, Enum):
    PREMIUM = "premium"
    SUPER_PREMIUM = "super_premium"
    REGULAR = "regular"
    DOUBLE = "double"


class TicketType(str, Enum):
    REGULAR = "regular"
    STUDENT = "student"
    DISCOUNT = "discount"


class Genre(str, Enum):
    ANIMATION = "animation"
    ACTION = "action"
    COMEDY = "comedy"
    DRAMA = "drama"
    HORROR = "horror"
    SCIENCE_FICTION = "science_fiction"
    ROMANCE = "romance"
    THRILLER = "thriller"
    FANTASY = "fantasy"
    MYSTERY = "mystery"
    WESTERN = "western"
    DOCUMENTARY = "documentary"


def pg_enum(enum, name):
    return SAEnum(enum, name=name, values_callable=lambda e: [m.value for m in e])


class CinemaLocation(SQLModel, table=True):
    __tablename__ = "cinema_locations"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=255)
    address: str = Field(max_length=255)
    hall_count: int
    is_active: bool = Field(default=True, sa_column_kwargs={"server_default": text("true")})

    halls: list["CinemaHall"] = Relationship(back_populates="location")


class CinemaHall(SQLModel, table=True):
    __tablename__ = "cinema_halls"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=255)
    row_count: int
    seat_count: int

    location_id: int = Field(
        foreign_key="cinema_locations.id"
    )

    location: CinemaLocation = Relationship(
        back_populates="halls"
    )

    sessions: list["Session"] = Relationship(
        back_populates="hall"
    )


class Movie(SQLModel, table=True):
    __tablename__ = "movies"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=255)

    genres: list["MovieGenre"] = Relationship(
        back_populates="movie"
    )

    sessions: list["Session"] = Relationship(
        back_populates="movie"
    )

    reviews: list["Review"] = Relationship(
        back_populates="movie"
    )

class MovieGenre(SQLModel, table=True):
    __tablename__ = "movie_genres"

    movie_id: int = Field(
        foreign_key="movies.id",
        primary_key=True
    )

    genre: Genre = Field(sa_type=pg_enum(Genre, "genre"), primary_key=True)

    movie: Movie = Relationship(
        back_populates="genres"
    )

class Session(SQLModel, table=True):
    __tablename__ = "sessions"

    id: int | None = Field(default=None, primary_key=True)

    start_time: datetime

    movie_id: int = Field(
        foreign_key="movies.id"
    )

    hall_id: int = Field(
        foreign_key="cinema_halls.id"
    )

    movie: Movie = Relationship(
        back_populates="sessions"
    )

    hall: CinemaHall = Relationship(
        back_populates="sessions"
    )

    tickets: list["Ticket"] = Relationship(
        back_populates="session"
    )

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    first_name: str = Field(max_length=255)
    last_name: str = Field(max_length=255)
    email: str = Field(max_length=255, unique=True)
    phone: str = Field(max_length=20)

    tickets: list["Ticket"] = Relationship(
        back_populates="user"
    )

    reviews: list["Review"] = Relationship(
        back_populates="user"
    )

class Seat(SQLModel, table=True):
    __tablename__ = "seats"

    id: int | None = Field(default=None, primary_key=True)
    row: int
    number: int
    seat_type: SeatType = Field(sa_type=pg_enum(SeatType, "seat_type"))

    hall_id: int = Field(
        foreign_key="cinema_halls.id"
    )

    tickets: list["Ticket"] = Relationship(
        back_populates="seat"
    )

class Ticket(SQLModel, table=True):
    __tablename__ = "tickets"
    __table_args__ = (UniqueConstraint("session_id", "seat_id"),)

    id: int | None = Field(default=None, primary_key=True)

    ticket_type: TicketType = Field(sa_type=pg_enum(TicketType, "ticket_type"))

    session_id: int = Field(
        foreign_key="sessions.id"
    )

    user_id: int = Field(
        foreign_key="users.id"
    )

    seat_id: int = Field(
        foreign_key="seats.id"
    )

    session: Session = Relationship(
        back_populates="tickets"
    )

    user: User = Relationship(
        back_populates="tickets"
    )

    seat: Seat = Relationship(
        back_populates="tickets"
    )

class Review(SQLModel, table=True):
    __tablename__ = "reviews"
    __table_args__ = (CheckConstraint("stars >= 1 AND stars <= 5"),)

    id: int | None = Field(default=None, primary_key=True)

    comment: str | None = None
    stars: int | None = Field(default=None, ge=1, le=5)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": text("now()")},
    )

    user_id: int = Field(
        foreign_key="users.id"
    )

    movie_id: int = Field(
        foreign_key="movies.id"
    )

    user: User = Relationship(
        back_populates="reviews"
    )

    movie: Movie = Relationship(
        back_populates="reviews"
    )