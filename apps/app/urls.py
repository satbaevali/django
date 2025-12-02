from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, CinemaViewSet, ShowtimeViewSet, BookingViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'cinemas', CinemaViewSet)
router.register(r'showtimes', ShowtimeViewSet)
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('v1/', include(router.urls)),
]
