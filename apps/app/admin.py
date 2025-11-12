from django.contrib import admin
from .models import User, Genre, Cinema, Hall, Seat, Movie, Show_time, Booking

# User model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "phone")
    search_fields = ("name", "email", "phone")

# Genre model
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

# Cinema model
@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "city", "address","created_at","updated_at")
    list_filter = ("city",)
    readonly_fields = (
        "created_at",
        "updated_at",
        "deleted_at"
    )
    list_display = ("id", "name", "city", "address")
    list_filter = ("city",)


# Hall model
@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "cinema", "total_seats")

# Seat model
@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ("id", "hall", "row", "number")

# Movie model
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "formatted_duration", "language", "rating","created_at","updated_at")
    filter_horizontal = ("genre",)
    readonly_fields = (
        "created_at",
        "updated_at",
        "deleted_at"
    )
    
    def formatted_duration(self, obj):
        return f"{obj.duration} мин"

# Show_time model
@admin.register(Show_time)
class ShowTimeAdmin(admin.ModelAdmin):
    list_display = ("id", "movie", "hall", "start_time", "end_time", "price")

# Booking model
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "show_time", "seats", "status")

