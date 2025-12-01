from django.shortcuts import render
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from apps.app.models import Movie, Cinema, Hall, Seat, Genre, Showtime
from apps.app.serializers import  SeatSerializer,  MovieSerializer, CinemaSerializer, HallSerializer, ShowtimeSerializer 

# Create your views here.
class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    # Optimize query to prefetch related genres
    queryset = Movie.objects.prefetch_related('genre').all()
    serializer_class = MovieSerializer

    # Filtering, searching
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['genre__name', 'language'] # genre name = 'Action', 'Comedy'
    search_fields = ['title', 'description'] # ?search = "some text"

class CinemaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cinema.objects.prefetch_related('halls').all()
    serializer_class = CinemaSerializer

class ShowtimeViewSet(viewsets.ReadOnlyModelViewSet):
    # Sorting by
    queryset = Showtime.objects.select_related('movie', 'hall').all().order_by('start_time')
    serializer_class = ShowtimeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['movie', 'hall', 'start_time'] # Filter by movie ID, hall ID, start time