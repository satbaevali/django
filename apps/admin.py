from django.contrib import admin
from .models import User, Genre, Cinema, Hall, Seat, Movie, Show_time, Booking, Payment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "phone")
    search_fields = ("name", "email", "phone")
    list_filter = ("name",)
    ordering = ("id",)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "city", "address")
    search_fields = ("name", "city")
    list_filter = ("city",)


@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "cinema", "total_seats")
    list_filter = ("cinema",)
    search_fields = ("name", "cinema__name")


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ("id", "hall", "row", "number")
    list_filter = ("hall",)
    search_fields = ("hall__name",)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "duration", "language", "rating")
    search_fields = ("title", "language")
    list_filter = ("genre",)
    filter_horizontal = ("genre",)


@admin.register(Show_time)
class ShowTimeAdmin(admin.ModelAdmin):
    list_display = ("id", "movie", "hall", "start_time", "end_time", "price")
    list_filter = ("hall", "movie")
    search_fields = ("movie__title",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "show_time", "seats", "status", "booking_time")
    list_filter = ("status", "show_time")
    search_fields = ("user_id__name", "show_time__movie__title")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "booking", "amount", "payment_method", "status", "payment_time")
    list_filter = ("payment_method", "status")
    search_fields = ("booking__user_id__name",)
