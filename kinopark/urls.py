
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/',include('apps.auths.urls')),
    path('api/app/', include('apps.app.urls'))
]+ static(settings.STATIC_URL)
