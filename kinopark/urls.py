
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/',include('apps.auths.urls')),
    path('api/v1/', include('apps.app.urls')),
    # File (JSON/YAML)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Beautiful UI (Swagger UI)
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # Alternative UI (Redoc)
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # --- DEBUG TOOLBAR ---
    path('__debug__/', include('debug_toolbar.urls')),
]+ static(settings.STATIC_URL)
