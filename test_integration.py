import os
import django
from datetime import timedelta
from django.utils import timezone

# --- 1. DJANGO SETUP (Required to run the script) ---
# Replace 'kinopark.settings' with the name of your folder containing settings.py if different
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kinopark.env.local")
django.setup()

# --- 2. IMPORTS (Only after setting up django.setup!) ---
from django.contrib.auth import get_user_model
# Make sure the path 'apps.cinema.models' is correct. If the folder is 'apps/app', change to 'apps.app.models'
from apps.app.models import Cinema, Hall, Seat, Genre, Movie, Showtime, Booking, Payment

# Get the User model (this will be CustomUser from auths if configured in settings.py)
User = get_user_model()

def run_full_test():
    print("\n🚀 RUNNING FULL SYSTEM TEST (AUTH + CINEMA)...\n")
    

    # --- STEP 1: AUTH (Developer A's work) ---
    email = "test_client_integration@kinopark.kz" # Unique email for the test
    password = "StrongPassword123!"
    
    # Check if user exists, if not - create via CustomManager
    user = User.objects.filter(email=email).first()
    if not user:
        print(f"👤 Creating user {email}...")
        try:
            user = User.objects.create_user(
                email=email, 
                password=password, 
                full_name="Test Integration Client"
            )
        except Exception as e:
            print(f"❌ Error creating user: {e}")
            return
    else:
        print(f"👤 User {email} already exists.")
    
    print(f"✅ [AUTH] User ID: {user.id} (Is Active: {user.is_active})")

    # --- STEP 2: CINEMA CONTENT (Your work - Developer B) ---
    print("\n🎬 Creating/Checking cinema content...")
    cinema, _ = Cinema.objects.get_or_create(name="Esentai Mall Integration", city="Almaty")
    hall, _ = Hall.objects.get_or_create(name="IMAX Test Hall", cinema=cinema, total_seats=0)
    
    # Create 1 seat manually for the test
    seat, _ = Seat.objects.get_or_create(hall=hall, row=10, number=10)
    
    genre, _ = Genre.objects.get_or_create(name="Integration Test Genre")
    movie, _ = Movie.objects.get_or_create(title="Testing The System Movie", duration=120)
    movie.genre.add(genre)
    
    print(f"✅ [CONTENT] Movie '{movie.title}' in hall '{hall.name}'")

    # --- STEP 3: SHOWTIME  ---
    # Showtime for tomorrow
    start_time = timezone.now() + timedelta(days=1)
    end_time = start_time + timedelta(minutes=movie.duration)
    
    showtime, created = Showtime.objects.get_or_create(
        movie=movie,
        hall=hall,
        defaults={
            'start_time': start_time,
            'end_time': end_time,
            'price': 4000.00
        }
    )
    if created:
        print(f"✅ [SHOWTIME] Created new showtime at {showtime.start_time}")
    else:
        print(f"ℹ️ [SHOWTIME] Showtime already exists")

    # --- STEP 4: BOOKING (Connecting everything together) ---
    print("\n🎟️ Trying to book a ticket...")
    
    # Clearing old bookings for the test to avoid "Already booked" error
    deleted_count, _ = Booking.objects.filter(showtime=showtime, seat=seat).delete()
    if deleted_count:
        print("   (Previous test booking cleared)")

    try:
        booking = Booking.objects.create(
            user=user,         # <-- Reference to CustomUser (Auth)
            showtime=showtime, # <-- Reference to Showtime (Cinema)
            seat=seat,         # <-- Reference to Seat (Cinema)
            status='booked'
        )
        print(f"✅ [BOOKING] TICKET SUCCESSFULLY CREATED! ID: {booking.id}")
        print(f"   Details: {booking}")
    except Exception as e:
        print(f"❌ Error during booking: {e}")
        return

    # --- STEP 5: PAYMENT ---
    try:
        # Check if there is an old payment that might interfere (if OneToOne)
        Payment.objects.filter(booking=booking).delete()
        
        payment = Payment.objects.create(
            user=user,
            booking=booking,
            amount=showtime.price,
            status='paid'
        )
        print(f"✅ [PAYMENT] Payment successful! ID: {payment.id}")
    except Exception as e:
        print(f"❌ Error during payment: {e}")
        # Often an error occurs if Payment requires fields we forgot
        return

    print("\n✨✨✨ TEST COMPLETED SUCCESSFULLY! ALL MODULES CONNECTED! ✨✨✨")

if __name__ == "__main__":
    try:
        run_full_test()
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        print("Tip: Check your settings in os.environ (at the beginning of the file) and folder structure.")