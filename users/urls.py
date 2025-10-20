from django.urls import path, include
from .views import authView, home

from django.contrib.auth import views as auth_views
app_name = 'users'

urlpatterns = [
    path("", home, name="home"),
    path("signup/", authView, name="signup"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(next_page='login'), name="logout"),
]