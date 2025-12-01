from django.db import models
from typing import Optional
from apps.abstracts.models import AbstractBaseModel
from django.contrib.auth import get_user_model  
from django.conf import settings


# Movie genre (e.g., Action, Comedy)
class Genre(models.Model):
    """
    Model representing a movie genre (e.g., Action, Comedy).
    """
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def __str__(self) -> str:
        return self.name

# Cinema with name, address, and city
class Cinema(AbstractBaseModel):
    """
    Model representing a physical cinema location
    """
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        return self.name

# Hall in a cinema with total seats
class Hall(models.Model):
    """
    Model representing a hall inside a cinema.
    """
    cinema = models.ForeignKey(
        Cinema, 
        on_delete=models.CASCADE, 
        related_name='halls'
    )
    name = models.CharField(max_length=100, blank=True)
    total_seats = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.name} - {self.cinema.name}"

# Seat in a hall
class Seat(models.Model):
    """
    Model representing a specific seat in a hall.
    """
    hall = models.ForeignKey(
        Hall, 
        on_delete=models.CASCADE, 
        related_name='seats'
    )
    row = models.PositiveIntegerField()
    number = models.PositiveIntegerField()

    class Meta:
        unique_together = ('hall', 'row', 'number')
        verbose_name = 'Seat'
        verbose_name_plural = 'Seats'

    def __str__(self) -> str:
        return f"Row {self.row}, Seat {self.number} - {self.hall.name}"

# Movie with genre, duration, language, and rating
class Movie(AbstractBaseModel):
    """
    Model representing a movie entity.
    """
    title = models.CharField(max_length=100, unique=True)
    genre = models.ManyToManyField(Genre, related_name='movies')
    rating = models.FloatField(blank=True, null=True)
    duration = models.IntegerField(help_text="Duration in minutes")
    description = models.TextField(blank=True)
    language = models.CharField(max_length=50, blank=True)
    poster = models.ImageField(upload_to='posters/', null=True, blank=True)
    
    def __str__(self) -> str:
        return self.title
    
# Show time for a movie in a hall with price
class Showtime(models.Model):
    """
    Model representing a specific movie screening
    """
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE, 
        related_name='showtimes'
    )
    hall = models.ForeignKey(
        Hall, 
        on_delete=models.CASCADE, 
        related_name='showtimes'
    )
    start_time = models.DateField()
    end_time = models.DateField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.movie.title} at {self.start_time.strftime('%Y-%m-%d')} in {self.hall.name}"

class Booking(models.Model):
    """
    Model representing a booking made by a user for a specific showtime and seat.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    showtime = models.ForeignKey(
        Showtime,
        on_delete=models.CASCADE, 
        related_name='bookings'
    )
    seat = models.ForeignKey(
        Seat, 
        on_delete=models.CASCADE, 
        related_name='bookings'
    )
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
    
    def save(self, *args, **kwargs):
        if not self.pk:
            if Booking.objects.filter(showtime=self.showtime, seat=self.seat).exists():
                raise ValueError("This seat is already booked for the selected showtime.")
        super().save(*args, **kwargs)    
    
    def __str__(self) -> str:
        return f"{self.user} — {self.showtime} — seat {self.seat}"
    
class Payment(models.Model):
    """
    Model representing a payment for a booking.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='payments'
    )
    booking = models.OneToOneField(
        Booking, 
        on_delete=models.CASCADE, 
        related_name='payment'
    )
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Payment #{self.id} — {self.status} — {self.booking}"