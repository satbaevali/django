from typing import Any
from random import choice,choices, randint, uniform
from datetime import datetime, time,timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.db.models import QuerySet


from apps.app.models import Genre,Cinema,Hall,Seat,Movie,Show_time,Booking
from apps.auths.models import CustomUser

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
    )
    GENRE_WORDS = (
        "Драма",
        "Комедия",
        "Фантастика",
        "Экшн",
        "Мелодрама",
        "Детектив",
    )
    CINEMA_WORDS =(
        "Kinopark",
        "Chaplin",
        "Arman Cinema",
        "Kinoplexx",
        "Kinostar",
        "Saryarka Cinema",
        "Cinema Towers",
        "Silkway Cinema",
        "Cinema City",
        "Altyn Arna Cinema",
        "Nomad Cinema",
        "Qazaqfilm Hall",
        "Mega Cinema",
        "Premium Cinema",
    )
    CITY_WORDS = (
        "Алматы",
        "Астана",
        "Шымкент",
        "Қарағанды",
        "Атырау",
        "Ақтөбе",
        "Павлодар",
        "Өскемен",
        "Қостанай"
    )
    HALL_WORDS = (
        "Hall 1",
        "Hall 2",
        "Hall 3",
        "Hall 4",
        "Hall 5",
        "VIP Hall",
        "Premium Hall",
        "IMAX Hall",
        "Dolby Atmos Hall",
        "LUXE Hall",
        "3D Hall",
        "4DX Hall",
        "Gold Hall",
        "Silver Hall",
        "Family Hall",
        "Comfort Hall",
    )
    MOVIE_WORDS = (
        "Томирис",
        "Бизнес по-казахски",
        "Келін",
        "Жаужүрек мың бала",
        "Махаббат. Жек көру",
        "Көксерек",
        "Анаға апарар жол",
        "Шал",
        "Қыз Жібек",
        "Елбасы жолы",
        "Зауал",
        "Бекзат",
        "Ана жүрегі",
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
    
    def __generate_users(self,user_count = 20)->None:
        USER_PASSWORD = make_password("12345")
        created_user:list[CustomUser] = []
        user_before : int = CustomUser.objects.count()
        
        i:int
        for i in range(user_count):
            full_name:str = f"user{i+1}"
            email: str = f"user{i+1}@{choice(self.EMAIL_DOMAINS)}"
            created_user.append(
                CustomUser(
                    full_name = full_name,
                    email = email,
                    password = USER_PASSWORD
                )
            )
        CustomUser.objects.bulk_create(created_user,ignore_conflicts=True)
        user_after:int = CustomUser.objects.count()
        
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
            name = " ".join(choices(self.GENRE_WORDS, k=1)).capitalize()
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
            name = " ".join(choices(self.CINEMA_WORDS,k=1)).capitalize()
            address = " ".join(choices(self.SOME_WORDS, k=4)).capitalize()
            city = " ".join(choices(self.CITY_WORDS,k=1)).capitalize()
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
            name = " ".join(choices(self.HALL_WORDS,k=1)).capitalize()
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
    def __generate_movie(self,movie_count = 20)->None:
        create_movie:list[Movie] = []
        exited_genre:QuerySet[Genre] = Genre.objects.all()
        movie_before:int = Movie.objects.count()
        LANGUAGE = ("KZ","RU","EN")
        duration = randint(50,150)
        
        i:int
        for i in range(movie_count):
            title = " ".join(choices(self.MOVIE_WORDS, k=1)).capitalize()    
            description =" ".join(choices(self.SOME_DESCRIPTIONS)).capitalize()
            language = choice(LANGUAGE)
            rating = round(uniform(1.0,5.0),2)
            create_movie.append(
                Movie(
                    title = title,
                    description =description,
                    duration = duration,
                    language = language,
                    rating = rating,
                )
            )
             
        
        Movie.objects.bulk_create(create_movie,ignore_conflicts=True)
        all_movies:QuerySet[Movie] = Movie.objects.all()[movie_before:]
        
        for movie in all_movies:
            genres_to_add = choices(exited_genre, k=randint(1, 3)) 
            movie.genre.set(genres_to_add)
        
        movie_after:int = Movie.objects.count()
        
        self.stdout.write(self.style.SUCCESS(f"Created {movie_after - movie_before} movies and assigned genres."))     
    
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
            start_hour = randint(12,23)
            start_minute = choice([0,15,30,45])
            
            if start_hour >= 22:
                end_hour = randint(0, 2)
            else:
                end_hour = randint(start_hour + 1, min(start_hour + 4, 23))

            start_t = time(start_hour % 24, start_minute)
            end_t = time(end_hour % 24, 0)
                        
            create_show_time.append(
                Show_time(
                    movie = movie,
                    hall = hall,
                    start_time = start_t,
                    end_time = end_t ,
                    price = randint(2000,5000)
                )
            )
        
        Show_time.objects.bulk_create(create_show_time,ignore_conflicts=True)
        show_after:int = Show_time.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f"Created {show_after - show_before } show_time"
            )
        )
    
    def __generate_booking(self,book_count = 20)->None:
        create_booking :list[Booking] = []
        
        exited_user_id:QuerySet[CustomUser] = CustomUser.objects.all()
        exited_show_time:QuerySet[Show_time] = Show_time.objects.all()
        exited_seat:QuerySet[Seat] = Seat.objects.all()
        booking_before : int=Booking.objects.count()
        
        i:int
        for i in range(book_count):
            user_id:CustomUser=choice(exited_user_id)
            show_time:Show_time=choice(exited_show_time)
            seats:Seat = choice(exited_seat)
            start_h = randint(4,12)
            start_m = choice([0,15,30,45])
            booking_time = time(start_h,start_m)
            status = ('pending','confirmed','canceled')
            create_booking.append(
                Booking(
                    user_id=user_id,
                    show_time = show_time,
                    seats = seats,
                    booking_time = booking_time,
                    status = choice(status)
                )
            )         
        Booking.objects.bulk_create(create_booking,ignore_conflicts=True)
        booking_after : int=Booking.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f"Created {booking_after - booking_before } booking"
            )
        )
            
        
    
    def handle(self, *args:tuple [Any, ...],**kwargs: dict[str, Any])->None:
        start_time:datetime = datetime.now()
        
        #self.__generate_users(user_count=20)
        self.__generate_genre(genre_count=20)
        self.__generate_cinema(cinema_count=20)
        self.__generate_hall(hall_count=20)
        self.__generate_seat(seat_count=20)
        self.__generate_show_time(show_time_count=20)
        self.__generate_movie(movie_count=20)
        #self.__generate_booking(book_count=20)
        self.stdout.write(
            "The whole process to generate data took: {} seconds".format(
                    (datetime.now() - start_time).total_seconds()
                )
            )