from django.shortcuts import render
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from apps.app.models import Booking, Movie, Cinema, Hall, Payment, Seat, Genre, Showtime
from apps.app.serializers import  PaymentSerializer, SeatSerializer,  MovieSerializer, CinemaSerializer, HallSerializer, ShowtimeSerializer, BookingSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.
class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
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
    permission_classes = [permissions.AllowAny]
    # Sorting by
    queryset = Showtime.objects.select_related('movie', 'hall').all().order_by('start_time')
    serializer_class = ShowtimeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['movie', 'hall', 'start_time'] # Filter by movie ID, hall ID, start time



class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # add filtering
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['showtime', 'user']

    def get_queryset(self):
        if self.request.query_params.get('showtime'):
            return Booking.objects.select_related('showtime', 'seat').all()
        if self.request.user.is_authenticated:
            return Booking.objects.filter(user=self.request.user).select_related('showtime', 'seat')
        return Booking.objects.none()
        
        #return Booking.objects.filter(user=self.request.user).select_related('showtime', 'seat')

    def create(self, request, *args, **kwargs):
        """Override create to return a list of all created bookings"""
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bookings = serializer.save()
        out_serializer = BookingSerializer(bookings, many=True)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)
    
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = serializer.save()
        
        # Update booking status after payment
        payment.status = 'paid'
        payment.save()
        payment.booking.status = 'booked'
        payment.booking.save()
        
        return Response({'message': 'You successfully purchased a ticket!'}, status=status.HTTP_201_CREATED)
    
# view for Seat with filtering by hall    
class SeatViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['hall']