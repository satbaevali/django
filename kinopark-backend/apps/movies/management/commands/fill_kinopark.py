
import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.movies.models import (
    Cinema, Hall, Seat,
    Genre, Movie, Showtime,
    Booking, Payment
)


class Command(BaseCommand):
    help = 'Fill the database with real Kinopark data (Kazakhstan)'

    def handle(self, *args, **kwargs):
        self.stdout.write("🎬 Заполнение базы Kinopark...")

        # 1. ОЧИСТКА
        Payment.objects.all().delete()
        Booking.objects.all().delete()
        Showtime.objects.all().delete()
        Seat.objects.all().delete()
        Hall.objects.all().delete()
        Movie.objects.all().delete()
        Cinema.objects.all().delete()
        Genre.objects.all().delete()

        # 2. ЖАНРЫ
        genres_data = [
            'Action', 'Sci-Fi', 'Drama',
            'Horror', 'Comedy',
            'Animation', 'Adventure', 'Musical'
        ]
        genres = {
            name: Genre.objects.create(name=name)
            for name in genres_data
        }

        # 3. ФИЛЬМЫ
        movies_list = [
            {
                "title": "Mufasa: The Lion King",
                "duration": 118,
                "rating": 7.8,
                "description": "Simba becomes king of the Pride Lands.",
                "language": "English",
                "genres": ["Animation", "Adventure", "Drama"]
            },
            {
                "title": "Kraven the Hunter",
                "duration": 127,
                "rating": 6.5,
                "description": "A brutal path of vengeance.",
                "language": "English",
                "genres": ["Action", "Sci-Fi"]
            },
            {
                "title": "Sonic the Hedgehog 3",
                "duration": 109,
                "rating": 8.1,
                "description": "Sonic faces Shadow.",
                "language": "English",
                "genres": ["Action", "Animation", "Comedy"]
            },
            {
                "title": "Nosferatu",
                "duration": 132,
                "rating": 7.9,
                "description": "A gothic horror tale.",
                "language": "English",
                "genres": ["Horror", "Drama"]
            },
            {
                "title": "Dastur",
                "duration": 90,
                "rating": 7.5,
                "description": "Kazakh horror movie.",
                "language": "Kazakh",
                "genres": ["Horror", "Drama"]
            },
            {
                "title": "Wicked",
                "duration": 160,
                "rating": 8.2,
                "description": "Musical fantasy story.",
                "language": "English",
                "genres": ["Musical", "Drama"]
            },
        ]

        created_movies = []
        for data in movies_list:
            movie = Movie.objects.create(
                title=data["title"],
                duration=data["duration"],
                rating=data["rating"],
                description=data["description"],
                language=data["language"],
                poster=None  # ❗ ImageField
            )
            for g in data["genres"]:
                movie.genre.add(genres[g])
            created_movies.append(movie)

        # 4. КИНОТЕАТРЫ
        cinemas_list = [
            {"name": "Kinopark 11 IMAX Esentai", "city": "Almaty", "address": "Al-Farabi 77/8"},
            {"name": "Kinopark 16 Forum", "city": "Almaty", "address": "Seifullina 617"},
            {"name": "Kinopark 7 IMAX Keruen", "city": "Astana", "address": "Dostyk 9"},
            {"name": "Kinopark 8 Saryarka", "city": "Astana", "address": "Turan 24"},
        ]

        created_halls = []

        for c in cinemas_list:
            cinema = Cinema.objects.create(**c)

            hall_configs = [
                {"name": "IMAX Laser", "seats": 100, "type": "imax"},
                {"name": "Dolby Atmos", "seats": 80, "type": "standard"},
                {"name": "Comfort Hall", "seats": 50, "type": "standard"},
                {"name": "VIP Hall", "seats": 20, "type": "vip"},
            ]

            for h in hall_configs:
                hall = Hall.objects.create(
                    cinema=cinema,
                    name=h["name"],
                    total_seats=h["seats"],
                    hall_type=h["type"]
                )
                created_halls.append(hall)

                # СИДЕНИЯ
                rows = 5
                seats_per_row = h["seats"] // rows
                seats = []

                for r in range(1, rows + 1):
                    for n in range(1, seats_per_row + 1):
                        seats.append(
                            Seat(
                                hall=hall,
                                row=r,
                                number=n,
                                seat_type="vip" if h["type"] == "vip" else "standard"
                            )
                        )

                Seat.objects.bulk_create(seats)

        # 5. СЕАНСЫ (3 ДНЯ)
        now = timezone.now()
        base_day = now.replace(hour=12, minute=0, second=0, microsecond=0)

        for day in range(3):
            date = base_day + timedelta(days=day)

            for hall in created_halls:
                movies_today = random.sample(created_movies, k=3)
                hour = 12

                for movie in movies_today:
                    start = date.replace(hour=hour)
                    end = start + timedelta(minutes=movie.duration)

                    price = 2500
                    if hall.hall_type == "imax":
                        price += 1500
                    if hall.hall_type == "vip":
                        price += 3000
                    if hour >= 18:
                        price += 500

                    Showtime.objects.create(
                        movie=movie,
                        hall=hall,
                        start_time=start,
                        end_time=end,
                        price=price,
                        is_active=True
                    )

                    hour += 3
                    if hour > 23:
                        break

        self.stdout.write(self.style.SUCCESS(
            f"✅ ГОТОВО: Фильмы={len(created_movies)}, Залы={len(created_halls)}"
        ))
