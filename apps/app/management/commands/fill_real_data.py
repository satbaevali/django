import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.app.models import Cinema, Hall, Seat, Genre, Movie, Showtime, Booking, Payment

class Command(BaseCommand):
    help = 'Fill the database with real Kinopark data (Kazakhstan)'
    

    def handle(self, *args, **kwargs):
        self.stdout.write("🎬 Начинаем заполнение базы реальными данными...")

        # 1. ОЧИСТКА (Удаляем старый контент, но НЕ пользователей)
        self.stdout.write("   Очистка старых данных (Booking, Showtime, Movie, Cinema)...")
        Payment.objects.all().delete()
        Booking.objects.all().delete()
        Showtime.objects.all().delete()
        Seat.objects.all().delete()
        Hall.objects.all().delete()
        Movie.objects.all().delete()
        Cinema.objects.all().delete()
        Genre.objects.all().delete()

        # 2. ЖАНРЫ
        self.stdout.write("   Создание жанров...")
        genres_data = ['Action', 'Sci-Fi', 'Drama', 'Horror', 'Comedy', 'Animation', 'Adventure', 'Musical']
        genres = {name: Genre.objects.create(name=name) for name in genres_data}

        # 3. ФИЛЬМЫ (Реальные премьеры 2024-2025)
        self.stdout.write("   Создание фильмов...")
        movies_list = [
            {
                "title": "Mufasa: The Lion King",
                "duration": 118,
                "rating": 7.8,
                "description": "Simba, having become king of the Pride Lands, is determined for his cub to follow in his paw prints.",
                "language": "English",
                "poster": "https://m.media-amazon.com/images/M/MV5BN2MyY2IyYmEtYzQyOC00Mjk5LThmNzMtMjFkYWJmMTY5ZTY2XkEyXkFqcGc@._V1_.jpg",
                "genres": ["Animation", "Adventure", "Drama"]
            },
            {
                "title": "Kraven the Hunter",
                "duration": 127,
                "rating": 6.5,
                "description": "Kraven's complex relationship with his ruthless father starts him down a path of vengeance with brutal consequences.",
                "language": "English",
                "poster": "https://m.media-amazon.com/images/M/MV5BMGUzYjM4ODYtNmM1ZC00NzUzLTg0NTEtYjFkNzgyYjRiYzU0XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
                "genres": ["Action", "Sci-Fi"]
            },
            {
                "title": "Sonic the Hedgehog 3",
                "duration": 109,
                "rating": 8.1,
                "description": "Sonic, Knuckles, and Tails reunite against a powerful new adversary, Shadow, a mysterious villain with powers unlike anything they have faced before.",
                "language": "English",
                "poster": "https://m.media-amazon.com/images/M/MV5BMjA5ZTE5NzgtM2VlNS00MzY2LTg4YTAtMzY5OTJmNWMzYzBjXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
                "genres": ["Action", "Animation", "Comedy"]
            },
            {
                "title": "Nosferatu",
                "duration": 132,
                "rating": 7.9,
                "description": "A gothic tale of obsession between a haunted young woman and the terrifying vampire infatuated with her, causing untold horror in its wake.",
                "language": "English",
                "poster": "https://m.media-amazon.com/images/M/MV5BHjEyYzJjMWEtOTQ2Yy00ZDY2LWJlNmEtMzFhNjA3MzFjNmYwXkEyXkFqcGc@._V1_.jpg",
                "genres": ["Horror", "Drama"]
            },
            {
                "title": "Dastur",
                "duration": 90,
                "rating": 7.5,
                "description": "A local Kazakh horror movie about traditions gone wrong.",
                "language": "Kazakh",
                "poster": "https://m.media-amazon.com/images/M/MV5BM2UzNTdkYjMtZVk5ZS00N2E2LWIyM2MtZjVjZjQwNjI5OTJlXkEyXkFqcGc@._V1_.jpg",
                "genres": ["Horror", "Drama"]
            },
            {
                "title": "Wicked",
                "duration": 160,
                "rating": 8.2,
                "description": "Elphaba, a misunderstood young woman because of her green skin, and Glinda, a popular girl, become friends at Shiz University.",
                "language": "English",
                "poster": "https://m.media-amazon.com/images/M/MV5BMjMwYTA0ZGQtMGM2MC00MjE2LWIzMWEtOGY2YzA3NzVmMWQ5XkEyXkFqcGc@._V1_.jpg",
                "genres": ["Musical", "Drama"]
            }
        ]

        created_movies = []
        for m_data in movies_list:
            movie = Movie.objects.create(
                title=m_data['title'],
                duration=m_data['duration'],
                rating=m_data['rating'],
                description=m_data['description'],
                language=m_data['language'],
                poster=m_data['poster'] # Сохраняем URL как строку или путь, Django обработает
            )
            for g_name in m_data['genres']:
                movie.genre.add(genres[g_name])
            created_movies.append(movie)

        # 4. КИНОТЕАТРЫ (Реальные Kinopark)
        self.stdout.write("   Создание кинотеатров...")
        cinemas_list = [
            {"name": "Kinopark 11 IMAX Esentai", "city": "Almaty", "address": "pr. Al-Farabi, 77/8"},
            {"name": "Kinopark 16 Forum", "city": "Almaty", "address": "pr. Seifullina, 617"},
            {"name": "Kinopark 7 IMAX Keruen", "city": "Astana", "address": "ul. Dostyk, 9"},
            {"name": "Kinopark 8 Saryarka", "city": "Astana", "address": "pr. Turan, 24"}
        ]

        created_halls = []
        for c_data in cinemas_list:
            cinema = Cinema.objects.create(**c_data)
            
            # В каждом кинотеатре создаем разные залы
            hall_configs = [
                {"name": "IMAX Laser", "seats": 100},
                {"name": "Dolby Atmos 1", "seats": 80},
                {"name": "Comfort Hall", "seats": 50},
                {"name": "VIP Hall", "seats": 20},
            ]

            for h_config in hall_configs:
                hall = Hall.objects.create(
                    cinema=cinema,
                    name=h_config["name"],
                    total_seats=h_config["seats"]
                )
                created_halls.append(hall)

                # Генерация мест (Bulk Create для скорости)
                seats_batch = []
                rows = 5
                seats_per_row = h_config["seats"] // rows
                
                for row in range(1, rows + 1):
                    for num in range(1, seats_per_row + 1):
                        seats_batch.append(Seat(hall=hall, row=row, number=num))
                
                Seat.objects.bulk_create(seats_batch)

        # 5. СЕАНСЫ (На сегодня, завтра и послезавтра)
        self.stdout.write("   Создание расписания сеансов...")
        
        now = timezone.now()
        today = now.replace(hour=10, minute=0, second=0, microsecond=0)
        
        # Генерируем сеансы на ближайшие 3 дня
        for day_offset in range(3):
            current_date = today + timedelta(days=day_offset)
            
            for hall in created_halls:
                # В каждом зале показываем 3-4 случайных фильма в день
                daily_movies = random.sample(created_movies, k=3)
                start_hour = 12 # Начинаем сеансы с 12:00

                for movie in daily_movies:
                    # Время начала
                    start_time = current_date.replace(hour=start_hour, minute=0)
                    end_time = start_time + timedelta(minutes=movie.duration)
                    
                    # Цена зависит от времени (вечер дороже) и зала (IMAX дороже)
                    price = 2500
                    if "IMAX" in hall.name: price += 1500
                    if "VIP" in hall.name: price += 3000
                    if start_hour >= 18: price += 500

                    Showtime.objects.create(
                        movie=movie,
                        hall=hall,
                        start_time=start_time,
                        end_time=end_time,
                        price=price
                    )
                    
                    # Следующий сеанс через 3 часа
                    start_hour += 3
                    if start_hour > 23: break

        self.stdout.write(self.style.SUCCESS(f"✅ УСПЕШНО! Создано фильмов: {len(created_movies)}, Залов: {len(created_halls)}. Данные реальные!"))