
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/',include('apps.auths.urls'))
]+ static(settings.STATIC_URL)
