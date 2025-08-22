from rest_framework import viewsets
from .serializer import ProductoSerializer, SedeSerializer
from .models import Sede, Producto

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()  # Define la consulta de los productos
    serializer_class = ProductoSerializer  # Usa el serializador de Producto

class SedeViewSet(viewsets.ModelViewSet):
    queryset = Sede.objects.all()  # Define la consulta de las sedes
    serializer_class = SedeSerializer  # Usa el serializador de Sede