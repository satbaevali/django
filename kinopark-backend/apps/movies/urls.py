"""
URL routing for movie booking system.

All endpoints are prefixed with /api/v1/apps/

Main routes:
- /genres/ - Movie genres
- /cinemas/ - Cinema locations
- /movies/ - Movie catalog
- /showtimes/ - Screening sessions
- /bookings/ - User bookings
- /payments/ - Payment processing
- /seats/ - Seat information
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.movies.views import (
    GenreViewSet,
    CinemaViewSet,
    MovieViewSet,
    ShowtimeViewSet,
    SeatViewSet,
    BookingViewSet,
    PaymentViewSet,
)


# Initialize router
router = DefaultRouter()

# Register all viewsets
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'cinemas', CinemaViewSet, basename='cinema')
router.register(r'movies', MovieViewSet, basename='movie')
router.register(r'showtimes', ShowtimeViewSet, basename='showtime')
router.register(r'seats', SeatViewSet, basename='seat')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'payments', PaymentViewSet, basename='payment')

# URL patterns
urlpatterns = [
    path('', include(router.urls)),
]