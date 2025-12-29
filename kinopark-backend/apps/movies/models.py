"""
Movie booking system models with city-based cinema structure.

This module contains all database models for the cinema booking system:
- Genre: Movie categories
- Cinema: Physical cinema locations with city information
- Hall: Screening rooms within cinemas
- Seat: Individual seats in halls
- Movie: Film information with genres
- Showtime: Movie screening sessions with pricing
- Booking: User ticket reservations
- Payment: Payment records for bookings
"""

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.abstracts.models import AbstractBaseModel


class Genre(models.Model):
    """
    Movie genre classification.
    
    Examples: Action, Comedy, Drama, Horror, Sci-Fi
    """
    
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Genre Name",
        help_text="Name of the movie genre"
    )
    
    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"
        ordering = ['name']
    
    def __str__(self) -> str:
        return self.name


class Cinema(AbstractBaseModel):
    """
    Physical cinema location with city-based organization.
    
    Each cinema belongs to a specific city and can have multiple halls.
    This allows filtering cinemas by city for better user experience.
    """
    
    name = models.CharField(
        max_length=200,
        verbose_name="Cinema Name",
        help_text="Name of the cinema (e.g., Kinopark Esentai)"
    )
    city = models.CharField(
        max_length=100,
        verbose_name="City",
        help_text="City where cinema is located",
        db_index=True
    )
    address = models.CharField(
        max_length=255,
        verbose_name="Address",
        help_text="Street address of the cinema"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description",
        help_text="Additional information about the cinema"
    )
    
    class Meta:
        verbose_name = "Cinema"
        verbose_name_plural = "Cinemas"
        ordering = ['city', 'name']
        unique_together = [['name', 'city']]
    
    def __str__(self) -> str:
        return f"{self.name} ({self.city})"
    
    @property
    def total_halls(self) -> int:
        """Return total number of halls in this cinema."""
        return self.halls.count()
    
    @property
    def total_capacity(self) -> int:
        """Return total seating capacity across all halls."""
        return sum(hall.total_seats for hall in self.halls.all())


class Hall(models.Model):
    """
    Screening room within a cinema.
    
    Each hall belongs to a specific cinema and contains multiple seats.
    Halls can have different capacities and features (e.g., IMAX, VIP).
    """
    
    cinema = models.ForeignKey(
        Cinema,
        on_delete=models.CASCADE,
        related_name='halls',
        verbose_name="Cinema"
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Hall Name",
        help_text="Name or number of the hall (e.g., IMAX Hall, Hall 1)"
    )
    total_seats = models.PositiveIntegerField(
        verbose_name="Total Seats",
        help_text="Total number of seats in this hall"
    )
    hall_type = models.CharField(
        max_length=50,
        choices=[
            ('standard', 'Standard'),
            ('vip', 'VIP'),
            ('imax', 'IMAX'),
            ('4dx', '4DX'),
        ],
        default='standard',
        verbose_name="Hall Type"
    )
    
    class Meta:
        verbose_name = "Hall"
        verbose_name_plural = "Halls"
        ordering = ['cinema', 'name']
        unique_together = [['cinema', 'name']]
    
    def __str__(self) -> str:
        return f"{self.name} - {self.cinema.name}"
    
    @property
    def available_seats(self) -> int:
        """Return number of seats in this hall."""
        return self.seats.count()


class Seat(models.Model):
    """
    Individual seat within a hall.
    
    Seats are organized by row and number for easy identification.
    Each seat can only be booked once per showtime.
    """
    
    hall = models.ForeignKey(
        Hall,
        on_delete=models.CASCADE,
        related_name='seats',
        verbose_name="Hall"
    )
    row = models.PositiveIntegerField(
        verbose_name="Row Number",
        validators=[MinValueValidator(1)]
    )
    number = models.PositiveIntegerField(
        verbose_name="Seat Number",
        validators=[MinValueValidator(1)]
    )
    seat_type = models.CharField(
        max_length=20,
        choices=[
            ('standard', 'Standard'),
            ('vip', 'VIP'),
            ('couple', 'Couple Seat'),
        ],
        default='standard',
        verbose_name="Seat Type"
    )
    
    class Meta:
        verbose_name = "Seat"
        verbose_name_plural = "Seats"
        ordering = ['hall', 'row', 'number']
        unique_together = [['hall', 'row', 'number']]
    
    def __str__(self) -> str:
        return f"Row {self.row}, Seat {self.number} ({self.hall.name})"


class Movie(AbstractBaseModel):
    """
    Movie information with genres and metadata.
    
    Movies can be shown at multiple cinemas and have multiple showtimes.
    """
    
    title = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Movie Title"
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='movies',
        verbose_name="Genres"
    )
    rating = models.FloatField(
        blank=True,
        null=True,
        verbose_name="Rating",
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        help_text="Movie rating from 0 to 10"
    )
    duration = models.PositiveIntegerField(
        verbose_name="Duration",
        help_text="Duration in minutes"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description",
        help_text="Movie plot summary"
    )
    language = models.CharField(
        max_length=50,
        verbose_name="Language",
        help_text="Original language of the movie"
    )
    poster = models.ImageField(
        upload_to='posters/%Y/%m/',
        null=True,
        blank=True,
        verbose_name="Poster Image"
    )
    release_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Release Date"
    )
    
    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"
        ordering = ['-created_at', 'title']
    
    def __str__(self) -> str:
        return self.title
    
    @property
    def genre_list(self) -> str:
        """Return comma-separated list of genres."""
        return ", ".join(g.name for g in self.genre.all())


class Showtime(models.Model):
    """
    Movie screening session with timing and pricing.
    
    Each showtime links a movie to a specific hall at a specific time.
    Pricing can vary based on hall type, time, and day of week.
    """
    
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='showtimes',
        verbose_name="Movie"
    )
    hall = models.ForeignKey(
        Hall,
        on_delete=models.CASCADE,
        related_name='showtimes',
        verbose_name="Hall"
    )
    start_time = models.DateTimeField(
        verbose_name="Start Time",
        db_index=True
    )
    end_time = models.DateTimeField(
        verbose_name="End Time"
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Base Price",
        help_text="Base ticket price in local currency"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Active",
        help_text="Whether this showtime is available for booking"
    )
    
    class Meta:
        verbose_name = "Showtime"
        verbose_name_plural = "Showtimes"
        ordering = ['start_time', 'hall']
        unique_together = [['hall', 'start_time']]
    
    def __str__(self) -> str:
        return f"{self.movie.title} - {self.start_time.strftime('%Y-%m-%d %H:%M')} ({self.hall.name})"
    
    @property
    def cinema(self):
        """Return cinema where this showtime takes place."""
        return self.hall.cinema
    
    @property
    def available_seats_count(self) -> int:
        """Return number of available seats for this showtime."""
        total = self.hall.total_seats
        booked = self.bookings.filter(status='booked').count()
        return total - booked


class Booking(models.Model):
    """
    User ticket reservation for a specific showtime and seat.
    
    Bookings are unique per showtime and seat combination.
    Status tracks whether booking is active, cancelled, or completed.
    """
    
    STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('booked', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name="User"
    )
    showtime = models.ForeignKey(
        Showtime,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name="Showtime"
    )
    seat = models.ForeignKey(
        Seat,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name="Seat"
    )
    booking_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Booking Time"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Booking Status"
    )
    
    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        ordering = ['-booking_time']
        unique_together = [['showtime', 'seat']]
    
    def __str__(self) -> str:
        return f"Booking #{self.id} - {self.user.email} - {self.showtime.movie.title}"
    
    def save(self, *args, **kwargs):
        """Validate seat belongs to showtime's hall before saving."""
        if self.seat.hall != self.showtime.hall:
            raise ValueError(
                f"Seat {self.seat} does not belong to hall {self.showtime.hall}"
            )
        super().save(*args, **kwargs)


class Payment(models.Model):
    """
    Payment record for a booking.
    
    Tracks payment status and automatically updates booking status.
    One-to-one relationship ensures one payment per booking.
    """
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name="User"
    )
    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name='payment',
        verbose_name="Booking"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Amount Paid"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Payment Status"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Payment Date"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Last Updated"
    )
    
    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ['-created_at']
    
    def __str__(self) -> str:
        return f"Payment #{self.id} - {self.amount} - {self.status}"