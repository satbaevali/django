
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment

@receiver(post_save, sender=Payment)
def update_booking_status(sender, instance, **kwargs):
    if instance.status == 'paid':
        instance.booking.status = 'booked'
        instance.booking.save()
