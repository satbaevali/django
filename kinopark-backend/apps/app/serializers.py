from rest_framework import serializers
from apps.app.models import (
    Genre, Cinema, Hall, Seat, Movie, Showtime,Booking, Payment
)
from apps.auths.models import CustomUser


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
    
    # WRITE: Только IDы
    hall_id = serializers.PrimaryKeyRelatedField(
        queryset=Hall.objects.all(), source='hall', write_only=True
    )
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.all(), source='movie', write_only=True
    )

    class Meta:
        model = Showtime
        fields = ['id', 'start_time', 'end_time', 'price', 'hall', 'hall_id', 'movie', 'movie_id']




class BookingSerializer(serializers.ModelSerializer):
    # Принимаем список seat_id для бронирования
    seats = serializers.PrimaryKeyRelatedField(
        queryset=Seat.objects.all(),
        many=True,
        write_only=True
    )

    class Meta:
        model = Booking
        fields = ['id', 'user', 'showtime', 'seats', 'booking_time', 'status']
        read_only_fields = ['user', 'booking_time', 'status']

    def validate(self, attrs):
        showtime = attrs['showtime']
        seats = attrs['seats']

        # 1) Проверяем, что все места принадлежат залу
        for seat in seats:
            if seat.hall != showtime.hall:
                raise serializers.ValidationError(
                    f"Seat {seat.id} does not belong to hall {showtime.hall.name}"
                )

        # 2) Проверяем, что места не заняты
        already_booked = Booking.objects.filter(
            showtime=showtime,
            seat__in=seats,
            status='booked'
        ).exists()

        if already_booked:
            raise serializers.ValidationError(
                "One or more seats are already booked"
            )

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        showtime = validated_data['showtime']
        seats = validated_data.pop('seats')

        # Создаём несколько записей Booking, по одной на каждое место
        bookings = []
        for seat in seats:
            booking = Booking.objects.create(
                user=user,
                showtime=showtime,
                seat=seat,
                status='booked'
            )
            bookings.append(booking)

        return bookings
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'booking', 'amount', 'status', 'created_at', 'updated_at', 'payment_time']
        read_only_fields = ['status', 'created_at', 'amount',]
