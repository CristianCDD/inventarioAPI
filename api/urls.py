from django.urls import path, include  # Agrega 'include' aquí
from rest_framework import routers
from api import views

router = routers.DefaultRouter()

# Registrar los viewsets en lugar de los serializadores
router.register(r'productos', views.ProductoViewSet)  # Registra el ProductoViewSet
router.register(r'sedes', views.SedeViewSet)  # Registra el SedeViewSet

urlpatterns = [
    path('', include(router.urls)),  # Incluye las rutas generadas por el router
]
