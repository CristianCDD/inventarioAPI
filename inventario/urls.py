from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta para el panel de administración
    path('', include('api.urls')),  # Ruta para la API, incluir las URLs de la aplicación 'api'
]
