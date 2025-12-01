from django.db import models

from apps.abstracts.models import AbstractBaseModel
from django.contrib.auth import get_user_model  
User = get_user_model()


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
    class Meta:
        unique_together = ('hall', 'row', 'number')

    def __str__(self):
        return f"Row {self.row}, Seat {self.number} - {self.hall.name}"

# Movie with genre, duration, language, and rating
class Movie(AbstractBaseModel):
    title = models.CharField(max_length=100, unique=True)
    genre = models.ManyToManyField(Genre, related_name='movies')
    rating = models.FloatField(blank=True, null=True)
    duration = models.IntegerField(help_text="Duration in minutes")
    description = models.TextField(blank=True)
    
    language = models.CharField(max_length=50, blank=True)
    poster = models.ImageField(upload_to='posters/', null=True, blank=True)
    

    def __str__(self):
        return self.title
    
# Show time for a movie in a hall with price
class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='show_times')
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='show_times')
    start_time = models.DateField()
    end_time = models.DateField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.movie.title} at {self.start_time.strftime('%Y-%m-%d')} in {self.hall.name}"




class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name='bookings')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name='bookings')

    booking_time = models.DateTimeField(auto_now_add=True)
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('booked', 'Booked'),
            ('canceled', 'Canceled'),
        ],
        default='booked'
    )

    class Meta:
        unique_together = ('showtime', 'seat') 
    def __str__(self):
        return f"{self.user} — {self.showtime} — seat {self.seat}"
class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment #{self.id} — {self.status} — {self.booking}"