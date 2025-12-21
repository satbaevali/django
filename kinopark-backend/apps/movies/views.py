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



# Create your views here.
class MovieViewSet(ViewSet):
    """
    A viewset for viewing and editing Movie instances.
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
    

class CinemaViewSet(ViewSet):
    """
    A viewset for viewing and editing Cinema instances.
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
    

class ShowtimeViewSet(ViewSet):
    """Showtime viewset with filtering capabilities."""
    permission_classes = [AllowAny]
    
    def list(self, request):
        """List all showtimes with filtering options."""
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
    
    
class BookingViewSet(ViewSet):
    """Booking viewset with user-specific data retrieval and filtering."""
    
    permission_classes = [IsAuthenticated]
    
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
        """Override get_queryset to filter bookings by showtime or user."""
        if self.request.query_params.get('showtime'):
            return Booking.objects.select_related('showtime', 'seat').all()
        if self.request.user.is_authenticated:
            return Booking.objects.filter(user=self.request.user).select_related('showtime', 'seat')
        return Booking.objects.none()
        

    def create(self, request, *args, **kwargs):
        """Override create to return a list of all created bookings"""
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bookings = serializer.save()
        out_serializer = BookingSerializer(bookings, many=True)
        return Response(out_serializer.data, status=HTTP_201_CREATED)
    
    
class PaymentViewSet(ViewSet):
    """Payment viewset with automatic booking status update after payment."""
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        """List all payments."""
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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = serializer.save()
        
        """ Automatically update booking status after payment """
        payment.status = 'paid'
        payment.save()
        payment.booking.status = 'booked'
        payment.booking.save()
        
        return Response({'message': 'You successfully purchased a ticket!'}, status=HTTP_201_CREATED)
    
  
class SeatViewSet(ViewSet):
    """Seat viewset with filtering by hall."""
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
    
    