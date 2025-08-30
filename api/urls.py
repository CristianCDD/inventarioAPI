from django.urls import path, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()

# Registra los viewsets
router.register(r'productos', views.ProductoViewSet)  # Registra el ProductoViewSet
router.register(r'movimientos', views.MovimientosViewSet)  # Registra el MovimientosViewSet

urlpatterns = [
    path('', include(router.urls)),  # Incluye las rutas generadas por el router
    path('eliminar/', views.EliminarMovimientosPorProducto.as_view(), name='eliminar-movimientos'),
    path('listado/', views.ProductoList.as_view(), name='producto-listado'),  # Ruta para la vista personalizada
]
