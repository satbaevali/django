"""
Serializers for movie booking system with city-based filtering.

This module provides nested serializers for:
- Browsing movies by city
- Viewing cinema details with available movies
- Booking seats with validation
- Payment processing

Key features:
- City-based cinema filtering
- Nested showtime information
- Available seats calculation
- Booking validation
"""

from rest_framework.serializers import(
    ModelSerializer,
    Serializer,
    CharField,
    IntegerField,
    DecimalField,
    DateTimeField,
    ImageField,
    SerializerMethodField,
    PrimaryKeyRelatedField,
    ListField,
    DictField,
    ValidationError,
)
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


# ============================================
# GENRE SERIALIZERS
# ============================================

class GenreSerializer(ModelSerializer):
    """Simple genre serializer for movie categorization."""
    
    class Meta:
        model = Genre
        fields = ['id', 'name']
        read_only_fields = ['id']


# ============================================
# CINEMA & LOCATION SERIALIZERS
# ============================================

class CinemaListSerializer(ModelSerializer):
    """
    Cinema list with basic info and statistics.
    Used for browsing cinemas by city.
    """
    
    total_halls = IntegerField(read_only=True)
    current_movies_count = SerializerMethodField()
    city_display = CharField(source='city', read_only=True)
    
    class Meta:
        model = Cinema
        fields = [
            'id',
            'name',
            'city',
            'city_display',
            'address',
            'total_halls',
            'current_movies_count',
        ]
        read_only_fields = ['id', 'total_halls', 'current_movies_count']
    
    def get_current_movies_count(self, obj) -> int:
        """Return count of unique movies currently showing."""
        now = timezone.now()
        return Showtime.objects.filter(
            hall__cinema=obj,
            start_time__gte=now,
            is_active=True
        ).values('movie').distinct().count()


class CinemaDetailSerializer(ModelSerializer):
    """
    Detailed cinema information with halls and current movies.
    Used for cinema-specific page.
    """
    
    halls = SerializerMethodField()
    current_movies = SerializerMethodField()
    total_capacity = IntegerField(read_only=True)
    
    class Meta:
        model = Cinema
        fields = [
            'id',
            'name',
            'city',
            'address',
            'description',
            'total_halls',
            'total_capacity',
            'halls',
            'current_movies',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_halls(self, obj):
        """Return simplified hall information."""
        return [
            {
                'id': hall.id,
                'name': hall.name,
                'total_seats': hall.total_seats,
                'hall_type': hall.get_hall_type_display(),
            }
            for hall in obj.halls.all()
        ]
    
    def get_current_movies(self, obj):
        """Return movies currently showing at this cinema."""
        now = timezone.now()
        movies = Movie.objects.filter(
            showtimes__hall__cinema=obj,
            showtimes__start_time__gte=now,
            showtimes__is_active=True
        ).distinct()
        return MovieSimpleSerializer(movies, many=True).data


class HallSerializer(ModelSerializer):
    """Hall information with cinema details."""
    
    cinema = CinemaListSerializer(read_only=True)
    cinema_id = PrimaryKeyRelatedField(
        queryset=Cinema.objects.all(),
        source='cinema',
        write_only=True
    )
    hall_type_display = CharField(
        source='get_hall_type_display',
        read_only=True
    )
    
    class Meta:
        model = Hall
        fields = [
            'id',
            'name',
            'cinema',
            'cinema_id',
            'total_seats',
            'hall_type',
            'hall_type_display',
            'available_seats',
        ]
        read_only_fields = ['id', 'available_seats']


# ============================================
# SEAT SERIALIZERS
# ============================================

class SeatSerializer(ModelSerializer):
    """Seat information with availability status."""
    
    hall_name = CharField(source='hall.name', read_only=True)
    seat_type_display = CharField(
        source='get_seat_type_display',
        read_only=True
    )
    is_available = SerializerMethodField()
    
    class Meta:
        model = Seat
        fields = [
            'id',
            'row',
            'number',
            'seat_type',
            'seat_type_display',
            'hall_name',
            'is_available',
        ]
        read_only_fields = ['id']
    
    def get_is_available(self, obj) -> bool:
        """Check if seat is available for given showtime."""
        showtime_id = self.context.get('showtime_id')
        if not showtime_id:
            return True
        
        return not Booking.objects.filter(
            showtime_id=showtime_id,
            seat=obj,
            status='booked'
        ).exists()


class SeatMapSerializer(Serializer):
    """
    Seat map for a specific showtime showing availability.
    Used for seat selection UI.
    """
    
    row = IntegerField()
    seats = ListField(
        child=DictField()
    )


# ============================================
# MOVIE SERIALIZERS
# ============================================

class MovieSimpleSerializer(ModelSerializer):
    """Simplified movie info for lists."""
    
    genres = GenreSerializer(source='genre', many=True, read_only=True)
    duration_display = SerializerMethodField()
    
    class Meta:
        model = Movie
        fields = [
            'id',
            'title',
            'genres',
            'rating',
            'duration',
            'duration_display',
            'language',
            'poster',
        ]
        read_only_fields = ['id']
    
    def get_duration_display(self, obj) -> str:
        """Return formatted duration (e.g., '2h 30min')."""
        hours = obj.duration // 60
        minutes = obj.duration % 60
        if hours:
            return f"{hours}h {minutes}min"
        return f"{minutes}min"


class MovieDetailSerializer(ModelSerializer):
    """
    Detailed movie information with available showtimes.
    Groups showtimes by cinema and city.
    """
    
    genres = GenreSerializer(source='genre', many=True, read_only=True)
    genre_ids = PrimaryKeyRelatedField(
        queryset=Genre.objects.all(),
        source='genre',
        many=True,
        write_only=True
    )
    duration_display = SerializerMethodField()
    available_cities = SerializerMethodField()
    showtimes_by_city = SerializerMethodField()
    
    class Meta:
        model = Movie
        fields = [
            'id',
            'title',
            'description',
            'genres',
            'genre_ids',
            'rating',
            'duration',
            'duration_display',
            'language',
            'poster',
            'release_date',
            'available_cities',
            'showtimes_by_city',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_duration_display(self, obj) -> str:
        """Return formatted duration."""
        hours = obj.duration // 60
        minutes = obj.duration % 60
        if hours:
            return f"{hours}h {minutes}min"
        return f"{minutes}min"
    
    def get_available_cities(self, obj) -> list:
        """Return cities where this movie is currently showing."""
        now = timezone.now()
        cities = Cinema.objects.filter(
            halls__showtimes__movie=obj,
            halls__showtimes__start_time__gte=now,
            halls__showtimes__is_active=True
        ).values_list('city', flat=True).distinct()
        return list(cities)
    
    def get_showtimes_by_city(self, obj) -> dict:
        """
        Return showtimes grouped by city and cinema.
        Format: {city: [{cinema: {...}, showtimes: [...]}]}
        """
        now = timezone.now()
        showtimes = Showtime.objects.filter(
            movie=obj,
            start_time__gte=now,
            is_active=True
        ).select_related('hall__cinema').order_by('start_time')
        
        result = {}
        for showtime in showtimes:
            city = showtime.hall.cinema.city
            cinema_name = showtime.hall.cinema.name
            
            if city not in result:
                result[city] = {}
            
            if cinema_name not in result[city]:
                result[city][cinema_name] = {
                    'cinema_id': showtime.hall.cinema.id,
                    'cinema_name': cinema_name,
                    'address': showtime.hall.cinema.address,
                    'showtimes': []
                }
            
            result[city][cinema_name]['showtimes'].append({
                'id': showtime.id,
                'start_time': showtime.start_time,
                'hall_name': showtime.hall.name,
                'hall_type': showtime.hall.get_hall_type_display(),
                'price': str(showtime.price),
                'available_seats': showtime.available_seats_count,
            })
        
        # Convert nested dict to list format
        return {
            city: list(cinemas.values())
            for city, cinemas in result.items()
        }


# ============================================
# SHOWTIME SERIALIZERS
# ============================================

class ShowtimeListSerializer(ModelSerializer):
    """Showtime list with movie and cinema info."""
    
    movie = MovieSimpleSerializer(read_only=True)
    cinema_name = CharField(source='hall.cinema.name', read_only=True)
    cinema_city = CharField(source='hall.cinema.city', read_only=True)
    hall_name = CharField(source='hall.name', read_only=True)
    available_seats = IntegerField(
        source='available_seats_count',
        read_only=True
    )
    
    class Meta:
        model = Showtime
        fields = [
            'id',
            'movie',
            'cinema_name',
            'cinema_city',
            'hall_name',
            'start_time',
            'end_time',
            'price',
            'available_seats',
            'is_active',
        ]
        read_only_fields = ['id']


class ShowtimeDetailSerializer(ModelSerializer):
    """
    Detailed showtime with seat map.
    Used for booking page.
    """
    
    movie = MovieSimpleSerializer(read_only=True)
    hall = HallSerializer(read_only=True)
    cinema = SerializerMethodField()
    seat_map = SerializerMethodField()
    available_seats = IntegerField(
        source='available_seats_count',
        read_only=True
    )
    
    class Meta:
        model = Showtime
        fields = [
            'id',
            'movie',
            'hall',
            'cinema',
            'start_time',
            'end_time',
            'price',
            'available_seats',
            'seat_map',
            'is_active',
        ]
        read_only_fields = ['id']
    
    def get_cinema(self, obj):
        """Return cinema information."""
        return {
            'id': obj.hall.cinema.id,
            'name': obj.hall.cinema.name,
            'city': obj.hall.cinema.city,
            'address': obj.hall.cinema.address,
        }
    
    def get_seat_map(self, obj):
        """Return seat map with availability."""
        seats = obj.hall.seats.all().order_by('row', 'number')
        booked_seats = set(
            Booking.objects.filter(
                showtime=obj,
                status='booked'
            ).values_list('seat_id', flat=True)
        )
        
        seat_map = {}
        for seat in seats:
            if seat.row not in seat_map:
                seat_map[seat.row] = []
            
            seat_map[seat.row].append({
                'id': seat.id,
                'number': seat.number,
                'type': seat.seat_type,
                'is_available': seat.id not in booked_seats,
            })
        
        return [
            {'row': row, 'seats': seats}
            for row, seats in sorted(seat_map.items())
        ]


class ShowtimeCreateSerializer(ModelSerializer):
    """Serializer for creating showtimes with validation."""
    
    movie_id = PrimaryKeyRelatedField(
        queryset=Movie.objects.all(),
        source='movie',
        write_only=True
    )
    hall_id = PrimaryKeyRelatedField(
        queryset=Hall.objects.all(),
        source='hall',
        write_only=True
    )
    
    class Meta:
        model = Showtime
        fields = [
            'id',
            'movie_id',
            'hall_id',
            'start_time',
            'end_time',
            'price',
            'is_active',
        ]
        read_only_fields = ['id']
    
    def validate(self, attrs):
        """Validate showtime doesn't overlap with existing ones."""
        hall = attrs['hall']
        start = attrs['start_time']
        end = attrs['end_time']
        
        # Check for overlapping showtimes
        overlapping = Showtime.objects.filter(
            hall=hall,
            start_time__lt=end,
            end_time__gt=start,
            is_active=True
        )
        
        if self.instance:
            overlapping = overlapping.exclude(pk=self.instance.pk)
        
        if overlapping.exists():
            raise ValidationError(
                "This time slot overlaps with an existing showtime."
            )
        
        return attrs


# ============================================
# BOOKING SERIALIZERS
# ============================================

class BookingListSerializer(ModelSerializer):
    """Booking list for user's ticket history."""
    
    movie_title = CharField(source='showtime.movie.title', read_only=True)
    movie_poster = ImageField(source='showtime.movie.poster', read_only=True)
    cinema_name = CharField(source='showtime.hall.cinema.name', read_only=True)
    cinema_city = CharField(source='showtime.hall.cinema.city', read_only=True)
    hall_name = CharField(source='showtime.hall.name', read_only=True)
    showtime_start = DateTimeField(source='showtime.start_time', read_only=True)
    seat_info = SerializerMethodField()
    price = DecimalField(
        source='showtime.price',
        max_digits=8,
        decimal_places=2,
        read_only=True
    )
    status_display = CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id',
            'movie_title',
            'movie_poster',
            'cinema_name',
            'cinema_city',
            'hall_name',
            'showtime_start',
            'seat_info',
            'price',
            'status',
            'status_display',
            'booking_time',
        ]
        read_only_fields = ['id', 'booking_time']
    
    def get_seat_info(self, obj) -> str:
        """Return formatted seat information."""
        return f"Row {obj.seat.row}, Seat {obj.seat.number}"


class BookingCreateSerializer(ModelSerializer):
    """
    Serializer for creating bookings with multi-seat support.
    Validates seat availability and hall matching.
    """
    
    showtime_id = PrimaryKeyRelatedField(
        queryset=Showtime.objects.filter(is_active=True),
        source='showtime',
        write_only=True
    )
    seat_ids = ListField(
        child=IntegerField(),
        write_only=True,
        min_length=1,
        max_length=10
    )
    
    class Meta:
        model = Booking
        fields = [
            'id',
            'showtime_id',
            'seat_ids',
            'status',
            'booking_time',
        ]
        read_only_fields = ['id', 'status', 'booking_time']
    
    def validate_seat_ids(self, value):
        """Validate seat IDs exist."""
        seats = Seat.objects.filter(id__in=value)
        if len(seats) != len(value):
            raise ValidationError(
                "One or more seat IDs are invalid."
            )
        return value
    
    def validate(self, attrs):
        """Validate seats belong to showtime hall and are available."""
        showtime = attrs['showtime']
        seat_ids = attrs['seat_ids']
        
        seats = Seat.objects.filter(id__in=seat_ids)
        
        # Check seats belong to correct hall
        for seat in seats:
            if seat.hall != showtime.hall:
                raise ValidationError(
                    f"Seat {seat.row}-{seat.number} does not belong to this hall."
                )
        
        # Check seats are not already booked
        already_booked = Booking.objects.filter(
            showtime=showtime,
            seat__in=seats,
            status='booked'
        )
        
        if already_booked.exists():
            booked_seats = already_booked.values_list('seat__row', 'seat__number')
            raise ValidationError(
                f"Some seats are already booked: {list(booked_seats)}"
            )
        
        return attrs
    
    def create(self, validated_data):
        """Create multiple bookings for selected seats."""
        user = self.context['request'].user
        showtime = validated_data['showtime']
        seat_ids = validated_data.pop('seat_ids')
        
        bookings = []
        for seat_id in seat_ids:
            booking = Booking.objects.create(
                user=user,
                showtime=showtime,
                seat_id=seat_id,
                status='pending'
            )
            bookings.append(booking)
        
        return bookings[0]  # Return first booking for response


# ============================================
# PAYMENT SERIALIZERS
# ============================================

class PaymentSerializer(ModelSerializer):
    """Payment information with booking details."""
    
    booking_details = BookingListSerializer(source='booking', read_only=True)
    status_display = CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id',
            'booking',
            'booking_details',
            'amount',
            'status',
            'status_display',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']


class PaymentCreateSerializer(ModelSerializer):
    """Create payment for booking."""
    
    booking_id = PrimaryKeyRelatedField(
        queryset=Booking.objects.all(),
        source='booking',
        write_only=True
    )
    
    class Meta:
        model = Payment
        fields = [
            'id',
            'booking_id',
            'amount',
        ]
        read_only_fields = ['id']
    
    def validate_booking_id(self, value):
        """Validate booking belongs to user and has no payment."""
        user = self.context['request'].user
        
        if value.user != user:
            raise ValidationError(
                "This booking does not belong to you."
            )
        
        if hasattr(value, 'payment'):
            raise ValidationError(
                "This booking already has a payment."
            )
        
        return value
    
    def validate_amount(self, value):
        """Validate payment amount matches booking price."""
        # This will be checked in validate() method
        return value
    
    def validate(self, attrs):
        """Validate amount matches showtime price."""
        booking = attrs['booking']
        amount = attrs['amount']
        expected_amount = booking.showtime.price
        
        if amount != expected_amount:
            raise ValidationError(
                f"Payment amount ({amount}) does not match ticket price ({expected_amount})."
            )
        
        return attrs