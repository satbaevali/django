from django.contrib import admin
from .models import  Genre, Cinema, Hall, Seat, Movie, Showtime,Booking,Payment
from django.utils.html import format_html
from django.urls import reverse
from django.contrib import admin

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
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "showtime", "seat", "booking_time")
    list_filter = ("booking_time", "showtime__movie")
    search_fields = ("user__username", "showtime__movie__title")

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse


# Payment model
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "booking", "amount", "status", "mark_paid", "created_at")
    list_filter = ("status", "created_at") # filter by status and creation date
    search_fields = ("booking__user__username",)

    # Кнопка для ручной оплаты
    def mark_paid(self, obj):
        if obj.status != 'paid':
            return format_html(
                '<a class="button" href="{}">Оплатить</a>',
                reverse('admin:mark_payment_paid', args=[obj.id])
            )
        return "paid"
    
    mark_paid.short_description = 'Action'

    # Automatic update of booking status after payment
    def save_model(self, request, obj, form, change):
        if obj.status == 'paid' and obj.booking.status != 'booked':
            obj.booking.save()
        super().save_model(request, obj, form, change)