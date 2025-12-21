from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import(
    MovieViewSet,
    CinemaViewSet,
    SeatViewSet,
    ShowtimeViewSet,
    BookingViewSet,
    PaymentViewSet
)

"""Router setup for app viewsets"""
router = DefaultRouter()

"""Movie, Cinema, Showtime, Booking, Payment, Seat viewsets registration"""
router.register(r'movies', MovieViewSet,basename='movie')
router.register(r'cinemas', CinemaViewSet, basename='cinema')
router.register(r'showtimes', ShowtimeViewSet,basename='showtime')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'seats', SeatViewSet,basename='seat') # Added SeatViewSet


urlpatterns = [
    path('', include(router.urls)),
]