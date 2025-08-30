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
                "id_producto": producto.id,
                "nombre": producto.nombre,
                "codigo": producto.codigo,
                "stock": producto.stock_total,
                "ultima_fecha_movimiento": producto.ultima_fecha_movimiento
            }
            result.append(producto_data)

        return Response(result)
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Movimientos

class EliminarMovimientosPorProducto(APIView):
    def delete(self, request, *args, **kwargs):
        producto_id = request.query_params.get('producto', None)
        if producto_id:
            Movimientos.objects.filter(producto_id=producto_id).delete()
            return Response({"message": "Movimientos eliminados correctamente"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Producto no especificado"}, status=status.HTTP_400_BAD_REQUEST)


class HistorialMovimientosPorProducto(APIView):
    def get(self, request, id_producto, format=None):
        # Filtrar los movimientos por producto y obtener las fechas, tipo de movimiento y cantidad
        movimientos = Movimientos.objects.filter(producto_id=id_producto).values('fecha', 'tipo_movimiento', 'cantidad')
        
        if not movimientos:
            return Response({"message": "No se encontraron movimientos para este producto"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({"historial_movimientos": list(movimientos)}, status=status.HTTP_200_OK)
