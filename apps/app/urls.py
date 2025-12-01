from django.urls import path, include
from rest_framework.routers import DefaultRouter
# Импортируем наши ViewSets
from .views import MovieViewSet, CinemaViewSet, ShowtimeViewSet

router = DefaultRouter()
# Регистрируем маршруты (Endpoints)
router.register(r'movies', MovieViewSet)
router.register(r'cinemas', CinemaViewSet)
router.register(r'showtimes', ShowtimeViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]