from typing import Any
from random import choice,choices, randint
from datetime import datetime, time,timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db.models import QuerySet

from apps.app.models import Genre,Cinema,Hall,Seat,Movie,Show_time,Booking,Payment

class Command(BaseCommand):
    help = "Generate models"
    
    EMAIL_DOMAINS = (
        "gmail.com",
        "mail.ru"
    )
    SOME_WORDS = (
        "lorem",
        "ipsum",
        "dolor",
        "sit",
        "amet",
        "consectetur",
        "adipiscing",
        "elit",
        "sed",
        "do",
        "eiusmod",
        "tempor",
        "incididunt",
        "ut",
        "labore",
        "et",
        "dolore",
        "magna",
        "aliqua",
    )
    
    def __generate_users(self,user_count = 20)->None:
        USER_PASSWORD = make_password("12345")
        created_user:list[User] = []
        user_before : int = User.objects.count()
        
        i:int
        for i in range(user_count):
            username:str = f"user{i+1}"
            email: str = f"user{i+1}@{choice(self.EMAIL_DOMAINS)}"
            created_user.append(
                User(
                    username = username,
                    email = email,
                    password = USER_PASSWORD
                )
            )
        User.objects.bulk_create(created_user,ignore_conflicts=True)
        user_after:int = User.objects.count()
        
        self.stdout.write(
            self.style.SUCCESS(
                f"Created{user_after - user_before} users"
            )
        )
        
    def __generate_genre(self,genre_count = 20)->None:
        create_genre:list[Genre] = []
        genre_before: int = Genre.objects.count()
        
        a:int 
        for a in range(genre_count):
            name = " ".join(choices(self.SOME_WORDS, k=3)).capitalize()
            create_genre.append(
                Genre(
                    name = name
                )
            )
        Genre.objects.bulk_create(create_genre,ignore_conflicts=True)
        genre_after:int = Genre.objects.count()
        
        self.stdout.write(
            self.style.SUCCESS(
                f"Created {genre_after - genre_before} genre"
            )
        )
    
    def __generate_cinema(self,cinema_count = 20)->None:
        create_cinema:list[Cinema] = []
        cinema_before: int = Cinema.objects.count()
        
        i:int 
        for i in range(cinema_count):
            name = " ".join(choices(self.SOME_WORDS,k=3)).capitalize()
            address = " ".join(choices(self.SOME_WORDS, k=4)).capitalize()
            city = " ".join(choices(self.SOME_WORDS,k=3)).capitalize()
            create_cinema.append(
                Cinema(
                    name = name,
                    address = address,
                    city = city
                )
            )
        Cinema.objects.bulk_create(create_cinema,ignore_conflicts=True)
        cinema_after: int = Cinema.objects.count()
        
        self.stdout.write(
            self.style.SUCCESS(
                f"Created {cinema_after - cinema_before} cinema"
            )
        )
    
    
    def __generate_hall(self,hall_count=20):
        create_hall:list[Hall] = []
        hall_before:int = Hall.objects.count()
        exited_cinema : QuerySet[Cinema]= Cinema.objects.all()
        
        i:int
        for i in range(hall_count):
            cinema : Cinema = choice(exited_cinema)
            name = " ".join(choices(self.SOME_WORDS,k=3)).capitalize()
            create_hall.append(
                Hall(
                    cinema=cinema,
                    name = name,
                    total_seats = randint(35,38)
                )
            )
        Hall.objects.bulk_create(create_hall,ignore_conflicts=True)
        hall_after : int = Hall.objects.count()
        
        self.stdout.write(
            self.style.SUCCESS(
                f"Created {hall_after - hall_before } hall"
            )
        )
        
    def __generate_seat(self,seat_count = 20)->None:
        create_seat:list[Seat] = []
        seat_before:int = Seat.objects.count()
        exited_hall:QuerySet[Hall] = Hall.objects.all()
        
        for i in range(seat_count):
            hall:Hall = choice(exited_hall)
            create_seat.append(
                Seat(
                    hall = hall,
                    row = randint(1,8),
                    number = randint(1,15),
                )
            )
        Seat.objects.bulk_create(create_seat,ignore_conflicts=True)
        seat_after: int = Seat.objects.count()
        
        self.stdout.write(
            self.style.SUCCESS(
                f"Created {seat_after - seat_before } seat"
            )
        )
            
    
    def __generate_show_time(self,show_time_count = 20)->None:
        create_show_time:list[Show_time] = []
        exited_movie : QuerySet[Movie] = Movie.objects.all()
        exited_hall : QuerySet[Hall] = Hall.objects.all()
        show_before:int = Show_time.objects.count()
        
        if not exited_movie.exists():
            return
        
        
        for i in range(show_time_count):
            movie:Movie = choice(exited_movie)
            hall: Hall = choice(exited_hall)
            start_hour = randint(4,12)
            start_minute = choice([0,15,30,45])
            end_hour = randint(start_hour + 4 ,20)
            
            start_t = time(start_hour,start_minute)
            end_t = time(end_hour,0)
            
            create_show_time.append(
                Show_time(
                    movie = movie,
                    hall = hall,
                    start_time = start_t,
                    end_time = end_t ,
                    price = f"{randint(2000,5000)}tg"
                )
            )
        show_after:int = Show_time.objects.count()
        Show_time.objects.bulk_create(create_show_time,ignore_conflicts=True)
        self.stdout.write(
            self.style.SUCCESS(
                f"Created {show_after - show_before } show_time"
            )
        )
            
        
    
    def handle(self, *args:tuple [Any, ...],**kwargs: dict[str, Any])->None:
        start_time:datetime = datetime.now()
        
        self.__generate_users(user_count=20)
        self.__generate_genre(genre_count=20)
        self.__generate_cinema(cinema_count=20)
        self.__generate_hall(hall_count=20)
        self.__generate_seat(seat_count=20)
        self.__generate_show_time(show_time_count=20)
        self.stdout.write(
            "The whole process to generate data took: {} seconds".format(
                    (datetime.now() - start_time).total_seconds()
                )
            )