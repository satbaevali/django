from rest_framework import serializers
from apps.app.models import (
    Genre, Cinema, Hall, Seat, Movie, Showtime
)

""" # Serialize app users
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
 """
# Serialize movie genres
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

# Serialize cinemas, halls, seats, and movies
class CinemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cinema
        fields = ['id', 'name', 'city', 'address']

class HallSerializer(serializers.ModelSerializer):
    # READ: Full cinema object
    cinema = CinemaSerializer(read_only=True)
    # WRITE: Accept only ID (cinema_id)
    cinema_id = serializers.PrimaryKeyRelatedField(
        queryset=Cinema.objects.all(), source='cinema', write_only=True
    )

    class Meta:
        model = Hall
        # Use cinema_id instead of cinema__id (cleaner this way)
        fields = ['id', 'name', 'total_seats', 'cinema', 'cinema_id']

class SeatSerializer(serializers.ModelSerializer):
    # For the list of seats, the full hall object is often not needed, but if needed - keep it
    hall_id = serializers.PrimaryKeyRelatedField(
        queryset=Hall.objects.all(), source='hall', write_only=True
    )

    class Meta:
        model = Seat
        fields = ['id', 'row', 'number', 'hall_id'] # Hall read_only убрал для скорости, ID обычно хватает

class MovieSerializer(serializers.ModelSerializer):
    # READ: List of genres with names
    genres = GenreSerializer(many=True, read_only=True)
    # WRITE: List of genre IDs [1, 2, 5]
    genre_ids = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(), source='genre', many=True, write_only=True
    )

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'duration', 'language', 'rating', 'poster', 'genres', 'genre_ids']

# -----------------------------
# 2. SCHEDULE SERIALIZERS (Твоя часть)
# -----------------------------

class ShowtimeSerializer(serializers.ModelSerializer):
    # READ: Полные объекты
    hall = HallSerializer(read_only=True)
    movie = MovieSerializer(read_only=True)
    
    # WRITE: Только ID
    hall_id = serializers.PrimaryKeyRelatedField(
        queryset=Hall.objects.all(), source='hall', write_only=True
    )
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.all(), source='movie', write_only=True
    )

    class Meta:
        model = Showtime
        fields = ['id', 'start_time', 'end_time', 'price', 'hall', 'hall_id', 'movie', 'movie_id']

""" # Serialize bookings with user, show_time, and seat info
class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user__id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True
    )
    show_time = ShowTimeSerializer(read_only=True)
    show_time__id = serializers.PrimaryKeyRelatedField(
        queryset=Show_time.objects.all(), source='show_time', write_only=True
    )
    seat = SeatSerializer(read_only=True)
    seat__id = serializers.PrimaryKeyRelatedField(
        queryset=Seat.objects.all(), source='seat', write_only=True
    )

    class Meta:
        model = Booking
        fields = ['id', 'booking_time', 'status', 'user', 'user__id', 'show_time', 'show_time__id', 'seat', 'seat__id']

 """