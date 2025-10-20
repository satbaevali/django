from django.db import models
from apps.abstracts.models import AbstractBaseModel
# User model for app users with contact info
class User(models.Model):
    name = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, unique=True, blank=True)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=12, unique=True, blank=True)

    def __str__(self):
        return self.name

# Movie genre (e.g., Action, Comedy)
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Cinema with name, address, and city
class Cinema(AbstractBaseModel):
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

# Hall in a cinema with total seats
class Hall(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name='halls')
    name = models.CharField(max_length=100, blank=True)
    total_seats = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.cinema.name}"

# Seat in a hall
class Seat(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='seats')
    row = models.PositiveIntegerField()
    number = models.PositiveIntegerField()

    def __str__(self):
        return f"Row {self.row}, Seat {self.number} - {self.hall.name}"

# Movie with genre, duration, language, and rating
class Movie(AbstractBaseModel):
    title = models.CharField(max_length=100, unique=True)
    genre = models.ManyToManyField(Genre, related_name='movies')
    description = models.TextField(blank=True)
    duration = models.IntegerField(help_text="Duration in minutes")
    language = models.CharField(max_length=50, blank=True)
    rating = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.title

# Show time for a movie in a hall with price
class Show_time(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='show_times')
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='show_times')
    start_time = models.TimeField()
    end_time = models.TimeField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.movie.title} at {self.start_time} in {self.hall.name}"

# Booking of a show time by a user for a seat
class Booking(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    show_time = models.ForeignKey(Show_time, on_delete=models.CASCADE, related_name='bookings')
    seats = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name='bookings')
    booking_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
    ], default='pending')

    def __str__(self):
        return f"Booking by {self.user_id.name} for {self.show_time.movie.title} at {self.show_time.start_time}"

