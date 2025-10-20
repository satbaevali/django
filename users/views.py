from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

# View for the home page, accessible only to logged-in users
@login_required
def home(request):
    return render(request, "home.html", {})

# View for user registration (signup)
def authView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()  # Save the new user
            return redirect("users:login")  # Redirect to login page after successful registration
    else:
        form = UserCreationForm()  # Display empty signup form
    return render(request, "registration/signup.html", {"form": form})

# Custom logout view that redirects users to the login page after logout
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('users:login')  # URL to redirect after logout
