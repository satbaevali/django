from django.urls import path,include

from .views import (
    RegisterView,
    LoginView,
    UserProfileView
)


urlpatterns = [
    path('register/',view=RegisterView.as_view({'post':'create'})),
    path('login/', LoginView.as_view({'post': 'create'}), name='login'),
    path('profile/',UserProfileView.as_view({'get':'list'}))
]

