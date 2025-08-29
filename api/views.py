from rest_framework import viewsets
from .serializer import ProductoSerializer, MovimientosSerializer
from .models import Producto, Movimientos
from django.db.models import Sum, F, Case, When
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Max

# ViewSet para Producto
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()  # Define la consulta de los productos
    serializer_class = ProductoSerializer  # Usa el serializador de Producto

# ViewSet para Movimientos
class MovimientosViewSet(viewsets.ModelViewSet):
    queryset = Movimientos.objects.all()  # Define la consulta de los movimientos
    serializer_class = MovimientosSerializer  # Usa el serializador de Movimientos


class ProductoList(APIView):
    def get(self, request, format=None):
        productos = Producto.objects.annotate(
            # Obtener la última fecha de movimiento
            ultima_fecha_movimiento=Max('movimientos__fecha'),
            
            # Calcular el stock total (entradas - salidas)
            stock_total=Sum(
                Case(
                    When(movimientos__tipo_movimiento='entrada', then=F('movimientos__cantidad')),
                    default=0
                )
            ) - Sum(
                Case(
                    When(movimientos__tipo_movimiento='salida', then=F('movimientos__cantidad')),
                    default=0
                )
            )
        )

        result = []
        for producto in productos:
            producto_data = {
                "nombre": producto.nombre,
                "codigo": producto.codigo,
                "stock": producto.stock_total,
                "ultima_fecha_movimiento": producto.ultima_fecha_movimiento,
            }
            result.append(producto_data)

        return Response(result)