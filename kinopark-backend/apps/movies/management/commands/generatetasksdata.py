from typing import Any
from random import choice, choices, randint, uniform
from datetime import datetime, time
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.db.models import QuerySet

from apps.movies.models import (
    Genre,
    Cinema,
    Hall,
    Seat,
    Movie,
    Showtime,
    Booking
)
from apps.auths.models import CustomUser


class Command(BaseCommand):
    help = "Generate models"

    EMAIL_DOMAINS = ("gmail.com", "mail.ru")
    SOME_WORDS = ("lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit")
    GENRE_WORDS = ("Драма", "Комедия", "Фантастика", "Экшн", "Мелодрама", "Детектив")
    CINEMA_WORDS = (
        "Kinopark", "Chaplin", "Arman Cinema", "Kinoplexx", "Kinostar", "Saryarka Cinema",
        "Cinema Towers", "Silkway Cinema", "Cinema City", "Altyn Arna Cinema", "Nomad Cinema",
        "Qazaqfilm Hall", "Mega Cinema", "Premium Cinema",
    )
    CITY_WORDS = ("Алматы", "Астана", "Шымкент", "Қарағанды", "Атырау", "Ақтөбе", "Павлодар", "Өскемен", "Қостанай")
    HALL_WORDS = (
        "Hall 1", "Hall 2", "Hall 3", "Hall 4", "Hall 5", "VIP Hall", "Premium Hall", "IMAX Hall",
        "Dolby Atmos Hall", "LUXE Hall", "3D Hall", "4DX Hall", "Gold Hall", "Silver Hall",
        "Family Hall", "Comfort Hall",
    )
    MOVIE_WORDS = (
        "Томирис", "Бизнес по-казахски", "Келін", "Жаужүрек мың бала", "Махаббат. Жек көру",
        "Көксерек", "Анаға апарар жол", "Шал", "Қыз Жібек", "Елбасы жолы", "Зауал", "Бекзат", "Ана жүрегі",
    )
    SOME_DESCRIPTIONS = (
        "Фильм о смелости, любви и верности. Главный герой борется за свою мечту.",
        "Добрая и трогательная история о настоящей дружбе и человеческих ценностях.",
        "Захватывающая история, наполненная опасностями и неожиданными поворотами.",
        "Основано на реальных событиях. Фильм рассказывает о силе духа и преодолении трудностей.",
        "Эта история о любви, которая проходит через испытания и расстояние.",
        "Фильм о жизни в большом городе и сложных отношениях между людьми.",
        "Драма о выборе между честью и личным счастьем.",
        "Фантастическая история о будущем человечества и его судьбе."
    )

    def __generate_users(self, user_count=20) -> None:
        USER_PASSWORD = make_password("12345")
        created_users: list[CustomUser] = []
        user_before: int = CustomUser.objects.count()

        for i in range(user_count):
            full_name = f"user{i + 1}"
            email = f"user{i + 1}@{choice(self.EMAIL_DOMAINS)}"
            created_users.append(
                CustomUser(
                    full_name=full_name,
                    email=email,
                    password=USER_PASSWORD
                )
            )

        CustomUser.objects.bulk_create(created_users, ignore_conflicts=True)
        user_after: int = CustomUser.objects.count()

        self.stdout.write(self.style.SUCCESS(f"Created {user_after - user_before} users"))

    def __generate_genre(self, genre_count=20) -> None:
        created_genres: list[Genre] = []
        genre_before: int = Genre.objects.count()

        for _ in range(genre_count):
            name = choice(self.GENRE_WORDS)
            created_genres.append(Genre(name=name))

        Genre.objects.bulk_create(created_genres, ignore_conflicts=True)
        genre_after: int = Genre.objects.count()

        self.stdout.write(self.style.SUCCESS(f"Created {genre_after - genre_before} genres"))

    def __generate_cinema(self, cinema_count=20) -> None:
        created_cinemas: list[Cinema] = []
        cinema_before: int = Cinema.objects.count()

        for _ in range(cinema_count):
            name = choice(self.CINEMA_WORDS)
            address = " ".join(choices(self.SOME_WORDS, k=4)).capitalize()
            city = choice(self.CITY_WORDS)
            created_cinemas.append(Cinema(name=name, address=address, city=city))

        Cinema.objects.bulk_create(created_cinemas, ignore_conflicts=True)
        cinema_after: int = Cinema.objects.count()

        self.stdout.write(self.style.SUCCESS(f"Created {cinema_after - cinema_before} cinemas"))

    def __generate_hall(self, hall_count=20) -> None:
        created_halls: list[Hall] = []
        hall_before: int = Hall.objects.count()
        all_cinemas: QuerySet[Cinema] = Cinema.objects.all()

        for _ in range(hall_count):
            cinema = choice(all_cinemas)
            name = choice(self.HALL_WORDS)
            created_halls.append(Hall(cinema=cinema, name=name, total_seats=randint(35, 38)))

        Hall.objects.bulk_create(created_halls, ignore_conflicts=True)
        hall_after: int = Hall.objects.count()

        self.stdout.write(self.style.SUCCESS(f"Created {hall_after - hall_before} halls"))

    def __generate_seat(self, seat_count=20) -> None:
        created_seats: list[Seat] = []
        seat_before: int = Seat.objects.count()
        all_halls: QuerySet[Hall] = Hall.objects.all()

        for _ in range(seat_count):
            hall = choice(all_halls)
            created_seats.append(Seat(hall=hall, row=randint(1, 8), number=randint(1, 15)))

        Seat.objects.bulk_create(created_seats, ignore_conflicts=True)
        seat_after: int = Seat.objects.count()

        self.stdout.write(self.style.SUCCESS(f"Created {seat_after - seat_before} seats"))

    def __generate_movie(self, movie_count=20) -> None:
        created_movies: list[Movie] = []
        all_genres: QuerySet[Genre] = Genre.objects.all()
        movie_before: int = Movie.objects.count()
        LANGUAGE = ("KZ", "RU", "EN")

        for _ in range(movie_count):
            title = choice(self.MOVIE_WORDS)
            description = choice(self.SOME_DESCRIPTIONS)
            language = choice(LANGUAGE)
            rating = round(uniform(1.0, 5.0), 2)
            duration = randint(50, 150)
            created_movies.append(
                Movie(title=title, description=description, language=language, rating=rating, duration=duration)
            )

        Movie.objects.bulk_create(created_movies, ignore_conflicts=True)
        new_movies: QuerySet[Movie] = Movie.objects.all()[movie_before:]

        for movie in new_movies:
            genres_to_add = choices(all_genres, k=randint(1, 3))
            movie.genre.set(genres_to_add)

        movie_after: int = Movie.objects.count()
        self.stdout.write(self.style.SUCCESS(f"Created {movie_after - movie_before} movies and assigned genres"))

    def __generate_showtime(self, showtime_count=20) -> None:
        created_showtimes: list[Showtime] = []
        all_movies: QuerySet[Movie] = Movie.objects.all()
        all_halls: QuerySet[Hall] = Hall.objects.all()
        showtime_before: int = Showtime.objects.count()

        for _ in range(showtime_count):
            movie = choice(all_movies)
            hall = choice(all_halls)
            start_hour = randint(12, 23)
            start_minute = choice([0, 15, 30, 45])
            end_hour = start_hour + randint(1, 4)
            start_t = time(start_hour % 24, start_minute)
            end_t = time(end_hour % 24, 0)
            price = randint(2000, 5000)

            created_showtimes.append(Showtime(movie=movie, hall=hall, start_time=start_t, end_time=end_t, price=price))

        Showtime.objects.bulk_create(created_showtimes, ignore_conflicts=True)
        showtime_after: int = Showtime.objects.count()
        self.stdout.write(self.style.SUCCESS(f"Created {showtime_after - showtime_before} showtimes"))

    def __generate_booking(self, booking_count=20) -> None:
        created_bookings: list[Booking] = []
        all_users: QuerySet[CustomUser] = CustomUser.objects.all()
        all_showtimes: QuerySet[Showtime] = Showtime.objects.all()
        all_seats: QuerySet[Seat] = Seat.objects.all()
        booking_before: int = Booking.objects.count()
        STATUS = ('booked', 'canceled')

        for _ in range(booking_count):
            user = choice(all_users)
            showtime = choice(all_showtimes)
            seat = choice(all_seats)
            created_bookings.append(
                Booking(user=user, showtime=showtime, seat=seat, status=choice(STATUS))
            )

        Booking.objects.bulk_create(created_bookings, ignore_conflicts=True)
        booking_after: int = Booking.objects.count()
        self.stdout.write(self.style.SUCCESS(f"Created {booking_after - booking_before} bookings"))

    def handle(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
        start_time = datetime.now()

        # self.__generate_users(user_count=20)
        self.__generate_genre(genre_count=20)
        self.__generate_cinema(cinema_count=20)
        self.__generate_hall(hall_count=20)
        self.__generate_seat(seat_count=20)
        self.__generate_movie(movie_count=20)
        self.__generate_showtime(showtime_count=20)
        # self.__generate_booking(booking_count=20)

        self.stdout.write(
            f"The whole process to generate data took: {(datetime.now() - start_time).total_seconds()} seconds"
        )
