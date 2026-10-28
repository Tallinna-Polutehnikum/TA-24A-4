import random
from datetime import datetime, timedelta, timezone

from faker import Faker
from sqlmodel import Session, select

from backend.database import engine
from backend.models import (
    CinemaHall,
    CinemaLocation,
    Genre,
    Movie,
    MovieGenre,
    Review,
    Seat,
    SeatType,
    Session as CinemaSession,
    Ticket,
    TicketType,
    User,
)


fake = Faker("et_EE")

def seed_database():
    with Session(engine) as db:
        existing_movie = db.exec(select(Movie)).first()

        if existing_movie:
            print("Database already contains data. Seeder stopped.")
            return

        print("Seeding database...")


        # CINEMA LOCATIONS

        locations = []

        for i in range(3):
            location = CinemaLocation(
                name=f"Kino {i + 1}",
                address=fake.address().replace("\n", ", "),
                hall_count=2,
                is_active=True,
            )

            db.add(location)
            locations.append(location)

        db.commit()

        for location in locations:
            db.refresh(location)


        # CINEMA HALLS

        halls = []

        for location in locations:
            for hall_number in range(1, 3):
                hall = CinemaHall(
                    name=f"{location.name} - Saal {hall_number}",
                    row_count=5,
                    seat_count=50,
                    location_id=location.id,
                )

                db.add(hall)
                halls.append(hall)

        db.commit()

        for hall in halls:
            db.refresh(hall)


        # SEATS

        seats_by_hall = {}

        seat_types = list(SeatType)

        for hall in halls:
            hall_seats = []

            for row in range(1, 6):
                for number in range(1, 11):
                    seat = Seat(
                        row=row,
                        number=number,
                        seat_type=random.choice(seat_types),
                        hall_id=hall.id,
                    )

                    db.add(seat)
                    hall_seats.append(seat)

            seats_by_hall[hall.id] = hall_seats

        db.commit()

        for hall_seats in seats_by_hall.values():
            for seat in hall_seats:
                db.refresh(seat)


        # MOVIES

        movie_names = [
            "Shadow Protocol",
            "Last Train Home",
            "Silent Orbit",
            "Midnight Signal",
            "Glass Horizon",
            "Northern Lights",
            "Final Sequence",
            "Lost Frequency",
            "Red Valley",
            "Beyond Tomorrow",
            "Dark Water",
            "Second Chance",
            "Frozen City",
            "Unknown Caller",
            "The Last Door",
        ]

        movies = []

        genres = list(Genre)

        for name in movie_names:
            movie = Movie(
                name=name,
            )

            db.add(movie)
            movies.append(movie)

        db.commit()

        for movie in movies:
            db.refresh(movie)


        # MOVIE GENRES - 1 to 3 per movie

        for movie in movies:
            for genre in random.sample(genres, random.randint(1, 3)):
                db.add(MovieGenre(movie_id=movie.id, genre=genre))

        db.commit()


        # USERS

        users = []

        for _ in range(30):
            user = User(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.unique.email(),
                phone=fake.phone_number()[:20],
            )

            db.add(user)
            users.append(user)

        db.commit()

        for user in users:
            db.refresh(user)


        # SESSIONS - 120 rows

        cinema_sessions = []

        start_date = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)

        # Fixed 3-hour slots, each (hall, day, hour) used once, so screenings cannot overlap
        slots = random.sample(
            [(hall, day, hour) for hall in halls for day in range(31) for hour in (10, 13, 16, 19, 22)],
            120,
        )

        for hall, day, hour in slots:
            movie = random.choice(movies)

            cinema_session = CinemaSession(
                start_time=start_date + timedelta(days=day, hours=hour),
                movie_id=movie.id,
                hall_id=hall.id,
            )

            db.add(cinema_session)
            cinema_sessions.append(cinema_session)

        db.commit()

        for cinema_session in cinema_sessions:
            db.refresh(cinema_session)


        # TICKETS - 300 rows

        used_seats = set()
        ticket_types = list(TicketType)

        tickets_created = 0

        while tickets_created < 300:
            cinema_session = random.choice(cinema_sessions)

            available_seats = seats_by_hall[cinema_session.hall_id]

            seat = random.choice(available_seats)

            reservation_key = (
                cinema_session.id,
                seat.id,
            )

            if reservation_key in used_seats:
                continue

            used_seats.add(reservation_key)

            ticket = Ticket(
                ticket_type=random.choice(ticket_types),
                session_id=cinema_session.id,
                user_id=random.choice(users).id,
                seat_id=seat.id,
            )

            db.add(ticket)
            tickets_created += 1

        db.commit()


        # REVIEWS

        for _ in range(50):
            review = Review(
                comment=fake.sentence(),
                stars=random.randint(1, 5),
                user_id=random.choice(users).id,
                movie_id=random.choice(movies).id,
            )

            db.add(review)

        db.commit()

        print("Database seeded successfully.")

if __name__ == "__main__":
    seed_database()