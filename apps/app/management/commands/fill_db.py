import random
from django.core.management.base import BaseCommand
from faker import Faker
from apps.app.models import Cinema, Hall, Seat, Genre, Movie
# If models are just in models.py, then from apps.cinema.models import ...

class Command(BaseCommand):
    help = 'Fills the database with dummy data for Endterm'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        self.stdout.write("Clearing old data...")
        # Deleting in the correct order to avoid breaking ForeignKeys
        Seat.objects.all().delete()
        Hall.objects.all().delete()
        Cinema.objects.all().delete()
        Movie.objects.all().delete()
        Genre.objects.all().delete()

        self.stdout.write("Creating Genres and Movies...")
        genres_list = ['Action', 'Comedy', 'Drama', 'Horror', 'Sci-Fi', 'Romance', 'Documentary']
        genres_objs = [Genre.objects.create(name=g) for g in genres_list]

        for _ in range(15): # 15 фильмов
            movie = Movie.objects.create(
                title=fake.catch_phrase(),
                description=fake.text(),
                duration=random.randint(90, 180),
                rating=round(random.uniform(5.0, 10.0), 1),
                language=random.choice(['English', 'Russian', 'Kazakh'])
            )
            # Добавляем рандомные жанры (от 1 до 3 штук)
            movie.genre.set(random.sample(genres_objs, k=random.randint(1, 3)))

        self.stdout.write("Creating Cinemas, Halls, and Seats...")
        for i in range(3): # 3 Cinemas
            cinema = Cinema.objects.create(
                name=f"KinoPark {fake.city()} Mall",
                city=fake.city(),
                address=fake.street_address()
            )
            
            # Each cinema has 3 halls
            for j in range(1, 4):
                hall = Hall.objects.create(
                    cinema=cinema,
                    name=f"Hall {j} ({'VIP' if j==3 else 'Standard'})",
                    total_seats=0
                )

                # SEAT GENERATION (Logic)
                # 5 rows of 8 seats = 40 seats
                seats = []
                for row in range(1, 6):
                    for num in range(1, 9):
                        seats.append(Seat(hall=hall, row=row, number=num))
                
                Seat.objects.bulk_create(seats) # Fast creation
                
                hall.total_seats = len(seats)
                hall.save()

        self.stdout.write(self.style.SUCCESS('Success! Database filled. 🚀'))