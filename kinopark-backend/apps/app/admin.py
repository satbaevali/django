from django.contrib import admin
from .models import  Genre, Cinema, Hall, Seat, Movie, Showtime


# Genre model
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

# Cinema model
@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "city", "address")
    list_filter = ("city",)
    list_editable = ("name",)
    fieldsets = (
        (
            "Cinema Information",
            {
                "fields": (
                    "name",
                    "city",
                    "address",
                )
            }
        ),
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "deleted_at",
    )


# Hall model
@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "cinema", "total_seats")
    list_filter = ("cinema",)

# Seat model
@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ("id", "hall", "row", "number")
    list_filter = ("hall__cinema","hall",)
    search_fields = ("hall__name",)

# Movie model
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "formatted_duration", "language", "rating","created_at","updated_at")
    filter_horizontal = ("genre",)
    search_fields = ("title",)
    list_filter = ("rating", "language")
    readonly_fields = (
        "created_at",
        "updated_at",
        "deleted_at"
    )
    
    def formatted_duration(self, obj):
        return f"{obj.duration} мин"

# Showtime model
@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ("id", "movie", "hall", "start_time", "end_time", "price")
    list_filter = ("start_time", "hall__cinema")
# Booking model
""" @admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "show_time", "seats", "status")

 """