# Drf-spectacular modules (НОВОЕ)
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiExample,
    OpenApiResponse,
    OpenApiTypes
)
# Django REST Framework modules
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status

#Project modules
from apps.movies.models import (
    Booking,
    Movie,
    Cinema,
    Payment,
    Seat,
    Showtime
)
from apps.movies.serializers import (
    PaymentSerializer,
    SeatSerializer,
    MovieSerializer,
    CinemaSerializer,
    ShowtimeSerializer,
    BookingSerializer
)

# MovieViewSet with documentation
@extend_schema_view(
    list=extend_schema(
        summary="List of movies",
        description="Get a list of all movies by genre.",
        tags=['Movies'],
        responses={
            HTTP_200_OK: MovieSerializer(many=True),
        }
    ),
    retrieve=extend_schema(
        summary="Detailed information about a movie",
        description="Get detailed information about a specific movie by ID.",
        tags=['Movies'],
        responses={
            HTTP_200_OK: MovieSerializer,
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Movie not found")
        }
    ),
    create=extend_schema(
        summary="Create a movie",
        description="Add a new movie to the database.",
        tags=['Movies'],
        request=MovieSerializer,
        responses={
            HTTP_201_CREATED: MovieSerializer,
            HTTP_400_BAD_REQUEST: OpenApiResponse(description="Validation error")
        },
        examples=[
            OpenApiExample(
                'Example of creating a movie',
                value={
                    'title': 'Inception',
                    'description': 'A thief who steals corporate secrets...',
                    'duration': 148,
                    'language': 'English',
                    'rating': 8.8,
                    'genre_ids': [1, 2]
                },
                request_only=True
            )
        ]
    )
)
class MovieViewSet(ViewSet):
    """
    ViewSet for managing Movie entities.
    
    Provides actions to list all movies, retrieve details of a specific movie,
    and create new movies.
    """
    permission_classes = [AllowAny]
    
    def list(self, request):
        """List all movies with prefetching genres to optimize queries."""
        
        queryset = Movie.objects.prefetch_related('genre').all()
        serializer = MovieSerializer(queryset, many=True)
        return Response(
            serializer.data,
            status=HTTP_200_OK
        )
    
    
    def retrieve(self, request, pk=None):
        """Retrieve a specific movie by its ID with prefetching genres."""
        
        queryset = Movie.objects.prefetch_related('genre').all()
        movie = queryset.get(pk=pk)
        serializer = MovieSerializer(movie)
        return Response(serializer.data,status=HTTP_200_OK)
    
    
    def create(self, request):
        """Create a new movie instance."""
        
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
# ---------------------------------------------------------------------
# CinemaViewSet with documentation
# ---------------------------------------------------------------------
@extend_schema_view(
    list=extend_schema(
        summary="List of cinemas",
        tags=['Cinemas'],
        responses={200: CinemaSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Details of a cinema",
        tags=['Cinemas'],
        responses={200: CinemaSerializer}
    ),
    create=extend_schema(
        summary="Add a cinema",
        tags=['Cinemas'],
        request=CinemaSerializer,
        responses={201: CinemaSerializer}
    )
)
class CinemaViewSet(ViewSet):
    """
    ViewSet for managing Cinema entities.
    
    Allows viewing all cinemas, getting details of a specific cinema,
    and creating new cinema locations.
    """
    permission_classes = [AllowAny]

    def list(self, request):
        """List all cinemas with prefetching halls to optimize queries."""
        queryset = Cinema.objects.prefetch_related('halls').all()
        serializer = CinemaSerializer(queryset, many=True)
        return Response(serializer.data,status=HTTP_200_OK)


    def retrieve(self, request, pk=None):
        """Retrieve a specific cinema by its ID with prefetching halls."""
        queryset = Cinema.objects.prefetch_related('halls').all()
        cinema = queryset.get(pk=pk)
        serializer = CinemaSerializer(cinema)
        return Response(serializer.data, status=HTTP_200_OK)
    
    
    def create(self, request):
        """Create a new cinema instance."""
        serializer = CinemaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
# ShowtimeViewSet with documentation 
@extend_schema_view(
    list=extend_schema(
        summary="Schedule of sessions",
        description="Get a list of sessions. You can filter by film, theatre, or date.",
        tags=['Showtimes'],
        parameters=[
            OpenApiParameter(name='movie', description='ID movie', required=False, type=int),
            OpenApiParameter(name='hall', description='ID hall', required=False, type=int),
            OpenApiParameter(name='start_time', description='Date (YYYY-MM-DD)', required=False, type=OpenApiTypes.DATE),
        ],
        responses={200: ShowtimeSerializer(many=True)}
    ),
    create=extend_schema(
        summary="Create a showtime",
        tags=['Showtimes'],
        request=ShowtimeSerializer,
        responses={201: ShowtimeSerializer}
    ),
    retrieve=extend_schema(
        summary="Details of a showtime",
        tags=['Showtimes'],
        responses={200: ShowtimeSerializer}
    )
)
class ShowtimeViewSet(ViewSet):
    """
    ViewSet for managing Movie Showtimes.
    
    Provides filtering capabilities to find showtimes by movie, hall, or date.
    """
    permission_classes = [AllowAny]
    
    def list(self, request):
        """
        List all showtimes with optional filtering.
        
        Query Parameters:
        - movie: ID of the movie
        - hall: ID of the hall
        - start_time: Date string (YYYY-MM-DD)
        """
        queryset = Showtime.objects.select_related('movie', 'hall').all().order_by('start_time')
        
        # Apply filters based on query parameters
        movie_id = request.query_params.get('movie')
        hall_id = request.query_params.get('hall')
        start_time = request.query_params.get('start_time')
        
        if movie_id:
            queryset = queryset.filter(movie__id=movie_id)
        if hall_id:
            queryset = queryset.filter(hall__id=hall_id)
        if start_time:
            queryset = queryset.filter(start_time__date=start_time)
        
        serializer = ShowtimeSerializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


    def retrieve(self, request, pk=None):
        """Retrieve a specific showtime by its ID."""
        queryset = Showtime.objects.select_related('movie', 'hall').all()
        showtime = queryset.get(pk=pk)
        serializer = ShowtimeSerializer(showtime)
        return Response(serializer.data,status=HTTP_200_OK)
    
    
    def create(self, request):
        """Create a new showtime instance."""
        serializer = ShowtimeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
# BookingViewSet with documentation
@extend_schema_view(
    list=extend_schema(
        summary="List of bookings",
        tags=['Bookings'],
        parameters=[
            OpenApiParameter(name='showtime', description='ID showtime', required=False, type=int),
            OpenApiParameter(name='user', description='ID user (for admins)', required=False, type=int),
        ],
        responses={200: BookingSerializer(many=True)}
    ),
    create=extend_schema(
        summary="Create a booking",
        description="Book seats. Accepts a list of seat IDs (seats).",
        tags=['Bookings'],
        request=BookingSerializer,
        responses={
            201: BookingSerializer, # Or BookingSerializer(many=True) if a list is returned
            400: OpenApiResponse(description="The seat is occupied or does not belong to the hall.")
        },
        examples=[
            OpenApiExample(
                'Book seats',
                value={
                    'showtime': 1,
                    'seats': [10, 11, 12] 
                },
                request_only=True,
                description="Pass showtime ID and array of seat IDs"
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Details of a booking",
        tags=['Bookings'],
        responses={200: BookingSerializer}
    )
)    
class BookingViewSet(ViewSet):
    """
    ViewSet for managing Bookings.
    
    Handles the creation of bookings (checking seat availability) and 
    retrieval of booking history.
    """
    
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer

    def get_serializer(self, *args, **kwargs):
        
        serializer_class = self.serializer_class
        kwargs.setdefault('context', {'request': self.request, 'view': self})
        return serializer_class(*args, **kwargs)
    
    def list(self, request):
        """List bookings with filtering by showtime or user."""
        showtime = request.query_params.get('showtime')
        user = request.query_params.get('user')
        filters = {}
        if showtime:
            filters['showtime'] = showtime
        if user:
            filters['user'] = user
        queryset = Booking.objects.select_related('showtime', 'seat').filter(**filters)
        serializer = BookingSerializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


    def retrieve(self, request, pk=None):
        """Retrieve a specific booking by its ID."""
        queryset = Booking.objects.select_related('showtime', 'seat').all()
        booking = queryset.get(pk=pk)
        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=HTTP_200_OK)
    
    
    def get_queryset(self):
        """
        Filter bookings by showtime or user.
        Regular users are restricted to their own bookings.
        """
        queryset = Booking.objects.select_related('showtime', 'seat').all()
        showtime = self.request.query_params.get('showtime')
        user_id = self.request.query_params.get('user')
        
        if showtime:
            queryset = queryset.filter(showtime_id=showtime)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        elif self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)
            
        return queryset

    def create(self, request, *args, **kwargs):
        """
        Create one or more bookings.
        
        Expects 'showtime' ID and a list of 'seats' IDs.
        Validates that seats belong to the correct hall and are not already booked.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()
        
  
        if isinstance(booking, list):
            return Response(BookingSerializer(booking, many=True).data, status=status.HTTP_201_CREATED)
        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)

# PaymentViewSet with documentation
@extend_schema_view(
    list=extend_schema(
        summary="List of payments",
        tags=['Payments'],
        responses={200: PaymentSerializer(many=True)}
    ),
    create=extend_schema(
        summary="Pay for a booking",
        tags=['Payments'],
        request=PaymentSerializer,
        responses={
            201: OpenApiResponse(description="Successful payment"),
            400: OpenApiResponse(description="Payment error")
        },
        examples=[
            OpenApiExample(
                'Payment',
                value={
                    'booking': 1,
                    'amount': 2500.00
                },
                request_only=True
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Details of a payment",
        tags=['Payments'],
        responses={200: PaymentSerializer}
    )
)    
class PaymentViewSet(ViewSet):
    """
    User payment management..

    This ViewSet handles ticket purchase transactions.
    
    Key features:
    * **Create payment**: Accepts booking ID and amount. . 
      - Automatically changes the payment status to `paid`.
      - Updates the status of the related booking (`Booking`) to `booked`.
    * **View history**: Users see only their own payments.
    * **Details**: Full information about a specific transaction.
    """
    permission_classes = [IsAuthenticated]
    
    serializer_class = PaymentSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.serializer_class
        kwargs.setdefault('context', {'request': self.request, 'view': self})
        return serializer_class(*args, **kwargs)
    
    def list(self, request):
        """
        Get a list of all payments for the current user.
        
        Returns transaction history with statuses and dates.
        """
        queryset = Payment.objects.select_related('booking').all()
        serializer = PaymentSerializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
    
    def retrieve(self, request, pk=None):
        """Retrieve a specific payment by its ID."""
        queryset = Payment.objects.select_related('booking').all()
        payment = queryset.get(pk=pk)
        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Pay for the booking.

        How it works:
        1. A payment record is created.
        2. The payment status is set to `paid`.
        3. The status of the related booking (`Booking`) is changed from `pending` to `booked`.

        In case of success, a message about the ticket purchase is returned.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = serializer.save(user=request.user)
        
        """ Automatically update booking status after payment """
        payment.status = 'paid'
        payment.save()
        payment.booking.status = 'booked'
        payment.booking.save()
        
        return Response({'message': 'You successfully purchased a ticket!'}, status=HTTP_201_CREATED)
    
# SeatViewSet with documentation
@extend_schema_view(
    list=extend_schema(
        summary="List of seats",
        tags=['Seats'],
        parameters=[
            OpenApiParameter(name='hall', description='ID of the hall', required=False, type=int),
        ],
        responses={200: SeatSerializer(many=True)}
    ),
    create=extend_schema(
        summary="Add a seat",
        tags=['Seats'],
        request=SeatSerializer,
        responses={201: SeatSerializer}
    ),
    retrieve=extend_schema(
        summary="Info about a seat",
        tags=['Seats'],
        responses={200: SeatSerializer}
    )
)  
class SeatViewSet(ViewSet):
    """
    ViewSet for managing Seats.
    
    Allows listing seats (optionally filtered by hall) and creating new seats.
    """
    permission_classes = [AllowAny]
    
    def list(self, request):
        """List all seats with optional filtering by hall."""
        hall_id = request.query_params.get('hall')
        queryset = Seat.objects.all()
        if hall_id:
            queryset = queryset.filter(hall__id=hall_id)
        serializer = SeatSerializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
    
    def retrieve(self, request, pk=None):
        """Retrieve a specific seat by its ID."""
        queryset = Seat.objects.all()
        seat = queryset.get(pk=pk)
        serializer = SeatSerializer(seat)
        return Response(serializer.data, status=HTTP_200_OK)
    
    def create(self, request):
        """Create a new seat instance."""
        serializer = SeatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    