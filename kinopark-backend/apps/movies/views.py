from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q, Prefetch
from django.utils import timezone
from apps.movies.models import (
    Genre,
    Cinema,
    Hall,
    Seat,
    Movie,
    Showtime,
    Booking,
    Payment
)
from apps.movies.serializers import (
    GenreSerializer,
    CinemaListSerializer,
    CinemaDetailSerializer,
    HallSerializer,
    SeatSerializer,
    MovieSimpleSerializer,
    MovieDetailSerializer,
    ShowtimeListSerializer,
    ShowtimeDetailSerializer,
    ShowtimeCreateSerializer,
    BookingListSerializer,
    BookingCreateSerializer,
    PaymentSerializer,
    PaymentCreateSerializer,
)


#Genre ViewSet
class GenreViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def list(self, request):
        queryset = Genre.objects.all()
        serializer = GenreSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        genre = Genre.objects.get(pk=pk)
        serializer = GenreSerializer(genre)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def movies(self, request, pk=None):
        genre = Genre.objects.get(pk=pk)
        movies = genre.movies.filter(
            showtimes__is_active=True,
            showtimes__start_time__gte=timezone.now()
        ).distinct()
        serializer = MovieSimpleSerializer(movies, many=True)
        return Response(serializer.data)


#Cinema ViewSet
class CinemaViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Cinema.objects.prefetch_related('halls').annotate(
            total_halls=Count('halls')
        )

    def list(self, request):
        queryset = self.get_queryset()

        city = request.query_params.get('city')
        if city:
            queryset = queryset.filter(city__iexact=city)

        serializer = CinemaListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        cinema = self.get_queryset().get(pk=pk)
        serializer = CinemaDetailSerializer(cinema)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def cities(self, request):
        cities = Cinema.objects.values('city').annotate(
            cinema_count=Count('id')
        ).order_by('city')

        return Response({
            'count': cities.count(),
            'results': list(cities)
        })

    @action(detail=False, methods=['get'], url_path='by-city/(?P<city>[^/.]+)')
    def by_city(self, request, city=None):
        cinemas = self.get_queryset().filter(city__iexact=city)

        if not cinemas.exists():
            return Response(
                {'error': f'No cinemas found in {city}'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CinemaListSerializer(cinemas, many=True)
        return Response({
            'city': city,
            'count': cinemas.count(),
            'results': serializer.data
        })

    @action(detail=True, methods=['get'])
    def current_movies(self, request, pk=None):
        cinema = self.get_queryset().get(pk=pk)
        now = timezone.now()

        movies = Movie.objects.filter(
            showtimes__hall__cinema=cinema,
            showtimes__start_time__gte=now,
            showtimes__is_active=True
        ).distinct()

        serializer = MovieSimpleSerializer(movies, many=True)
        return Response({
            'cinema': cinema.name,
            'city': cinema.city,
            'movie_count': movies.count(),
            'movies': serializer.data
        })


#Movie ViewSet
class MovieViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Movie.objects.prefetch_related('genre')

    def list(self, request):
        movies = self.get_queryset()

        city = request.query_params.get('city')
        if city:
            movies = movies.filter(
                showtimes__hall__cinema__city__iexact=city,
                showtimes__is_active=True,
                showtimes__start_time__gte=timezone.now()
            ).distinct()

        serializer = MovieSimpleSerializer(movies, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        movie = self.get_queryset().get(pk=pk)
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='now-showing')
    def now_showing(self, request):
        now = timezone.now()
        movies = self.get_queryset().filter(
            showtimes__start_time__gte=now,
            showtimes__is_active=True
        ).distinct()

        serializer = MovieSimpleSerializer(movies, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def showtimes(self, request, pk=None):
        movie = self.get_queryset().get(pk=pk)
        now = timezone.now()

        showtimes = Showtime.objects.filter(
            movie=movie,
            start_time__gte=now,
            is_active=True
        )

        city = request.query_params.get('city')
        if city:
            showtimes = showtimes.filter(hall__cinema__city__iexact=city)

        serializer = ShowtimeListSerializer(showtimes, many=True)
        return Response({
            'movie': movie.title,
            'count': showtimes.count(),
            'showtimes': serializer.data
        })

    @action(detail=True, methods=['get'], url_path='available-cities')
    def available_cities(self, request, pk=None):
        movie = self.get_queryset().get(pk=pk)
        now = timezone.now()

        cities = Cinema.objects.filter(
            halls__showtimes__movie=movie,
            halls__showtimes__start_time__gte=now,
            halls__showtimes__is_active=True
        ).values('city').annotate(
            cinema_count=Count('id', distinct=True),
            showtime_count=Count('halls__showtimes', distinct=True)
        )

        return Response({
            'movie': movie.title,
            'cities': list(cities)
        })


#Booking ViewSet
class BookingViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self, request):
        return Booking.objects.filter(user=request.user).select_related(
            'showtime__movie',
            'showtime__hall__cinema',
            'seat'
        )

    def list(self, request):
        serializer = BookingListSerializer(
            self.get_queryset(request), many=True
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        booking = self.get_queryset(request).get(pk=pk)
        serializer = BookingListSerializer(booking)
        return Response(serializer.data)

    def create(self, request):
        serializer = BookingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        booking = self.get_queryset(request).get(pk=pk)

        if booking.showtime.start_time <= timezone.now():
            return Response(
                {'error': 'Cannot cancel booking for past or ongoing showtime.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.status = 'cancelled'
        booking.save()

        return Response({'message': 'Booking cancelled successfully.'})


#Payment ViewSet
class PaymentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self, request):
        return Payment.objects.filter(user=request.user).select_related(
            'booking__showtime__movie',
            'booking__showtime__hall__cinema',
            'booking__seat'
        )

    def list(self, request):
        serializer = PaymentSerializer(
            self.get_queryset(request), many=True
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        payment = self.get_queryset(request).get(pk=pk)
        serializer = PaymentSerializer(payment)
        return Response(serializer.data)

    def create(self, request):
        serializer = PaymentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payment = serializer.save(
            user=request.user,
            status='paid'
        )

        booking = payment.booking
        booking.status = 'booked'
        booking.save()

        return Response({
            'message': 'Payment successful! Your ticket is booked.',
            'payment': PaymentSerializer(payment).data
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        payments = self.get_queryset(request)

        return Response({
            'total_spent': str(sum(p.amount for p in payments if p.status == 'paid')),
            'payment_count': payments.count(),
            'successful_payments': payments.filter(status='paid').count(),
            'pending_payments': payments.filter(status='pending').count(),
        })


#Showtime ViewSet
class ShowtimeViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def get_queryset(self):
        now = timezone.now()
        return Showtime.objects.select_related(
            'movie', 'hall__cinema'
        ).filter(
            is_active=True,
            start_time__gte=now
        )

    def list(self, request):
        queryset = self.get_queryset()

        movie = request.query_params.get('movie')
        if movie:
            queryset = queryset.filter(movie_id=movie)

        hall = request.query_params.get('hall')
        if hall:
            queryset = queryset.filter(hall_id=hall)

        city = request.query_params.get('hall__cinema__city')
        if city:
            queryset = queryset.filter(hall__cinema__city__iexact=city)

        serializer = ShowtimeListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        showtime = self.get_queryset().get(pk=pk)
        serializer = ShowtimeDetailSerializer(showtime)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def today(self, request):
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start.replace(hour=23, minute=59, second=59)

        showtimes = self.get_queryset().filter(
            start_time__gte=today_start,
            start_time__lte=today_end
        )

        city = request.query_params.get('city')
        if city:
            showtimes = showtimes.filter(hall__cinema__city__iexact=city)

        serializer = ShowtimeListSerializer(showtimes, many=True)
        return Response({
            'date': today_start.date(),
            'count': showtimes.count(),
            'showtimes': serializer.data
        })

    @action(detail=True, methods=['get'], url_path='available-seats')
    def available_seats(self, request, pk=None):
        showtime = self.get_queryset().get(pk=pk)

        total_seats = showtime.hall.total_seats
        booked_seats = Booking.objects.filter(
            showtime=showtime,
            status='booked'
        ).count()

        available = total_seats - booked_seats

        return Response({
            'showtime_id': showtime.id,
            'movie': showtime.movie.title,
            'hall': showtime.hall.name,
            'total_seats': total_seats,
            'booked_seats': booked_seats,
            'available_seats': available,
            'is_full': available == 0
        })


#Seat ViewSet
class SeatViewSet(viewsets.ViewSet):
    """
    ViewSet for browsing seats.

    Mainly used internally by booking system.
    """

    permission_classes = [AllowAny]

    def get_queryset(self):
        return Seat.objects.select_related('hall__cinema')

    def list(self, request):
        queryset = self.get_queryset()

        hall = request.query_params.get('hall')
        if hall:
            queryset = queryset.filter(hall_id=hall)

        row = request.query_params.get('row')
        if row:
            queryset = queryset.filter(row=row)

        seat_type = request.query_params.get('seat_type')
        if seat_type:
            queryset = queryset.filter(seat_type=seat_type)

        serializer = SeatSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        seat = self.get_queryset().get(pk=pk)
        serializer = SeatSerializer(seat)
        return Response(serializer.data)
