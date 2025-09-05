from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, F, Case, When, Max
from django.db.models.functions import Coalesce

from .serializer import ProductoSerializer, MovimientosSerializer
from .models import Producto, Movimientos


# ViewSet para Producto
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


# ViewSet para Movimientos
class MovimientosViewSet(viewsets.ModelViewSet):
    queryset = Movimientos.objects.all()
    serializer_class = MovimientosSerializer


class ProductoList(APIView):
    def get(self, request, format=None):
        productos = Producto.objects.annotate(
            # Última fecha de movimiento
            ultima_fecha_movimiento=Max('movimientos__fecha'),

            # Entradas acumuladas
            entradas=Coalesce(Sum(
                Case(
                    When(movimientos__tipo_movimiento='entrada', then=F('movimientos__cantidad')),
                    default=0
                )
            ), 0),

            # Salidas acumuladas
            salidas=Coalesce(Sum(
                Case(
                    When(movimientos__tipo_movimiento='salida', then=F('movimientos__cantidad')),
                    default=0
                )
            ), 0),
        ).annotate(
            stock_total=F('entradas') - F('salidas')
        )

        result = []
        for p in productos:
            result.append({
                "id_producto": p.id,
                "nombre": p.nombre,
                "codigo": p.codigo,
                "stock": int(p.stock_total) if p.stock_total is not None else 0,
                "ultima_fecha_movimiento": p.ultima_fecha_movimiento
            })

        return Response(result, status=status.HTTP_200_OK)


class EliminarMovimientosPorProducto(APIView):
    def delete(self, request, *args, **kwargs):
        producto_id = request.query_params.get('producto')
        if not producto_id:
            return Response({"error": "Producto no especificado"}, status=status.HTTP_400_BAD_REQUEST)

        borrados, _ = Movimientos.objects.filter(producto_id=producto_id).delete()
        return Response({"message": f"Movimientos eliminados: {borrados}"}, status=status.HTTP_200_OK)


class HistorialMovimientosPorProducto(APIView):
    # habilitamos GET, PATCH y DELETE
    http_method_names = ['get', 'patch', 'delete']

    def get(self, request, id_producto, format=None):
        """
        Devuelve el historial de movimientos de un producto,
        ordenados por fecha descendente (más recientes primero).
        """
        movimientos_qs = (
            Movimientos.objects
            .filter(producto_id=id_producto)
            .order_by('-fecha', '-id')   # 👈 ordenado: recientes primero
            .values('id', 'fecha', 'tipo_movimiento', 'cantidad')
        )

        if not movimientos_qs.exists():
            return Response(
                {"message": "No se encontraron movimientos para este producto"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {"historial_movimientos": list(movimientos_qs)},
            status=status.HTTP_200_OK
        )

    def patch(self, request, id_producto, format=None):
        """
        Actualiza parcialmente un movimiento del producto.
        """
        mov_id = request.data.get('id')
        if not mov_id:
            return Response(
                {"error": "Debes enviar el 'id' del movimiento a actualizar"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            mov = Movimientos.objects.get(id=mov_id, producto_id=id_producto)
        except Movimientos.DoesNotExist:
            return Response(
                {"error": "Movimiento no encontrado para este producto"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Solo actualizamos los campos enviados
        if 'cantidad' in request.data:
            mov.cantidad = request.data['cantidad']
        if 'fecha' in request.data:
            mov.fecha = request.data['fecha']
        if 'tipo_movimiento' in request.data:
            mov.tipo_movimiento = request.data['tipo_movimiento']

        mov.save()

        return Response({
            "message": "Movimiento actualizado",
            "movimiento": {
                "id": mov.id,
                "producto": mov.producto_id,
                "fecha": str(mov.fecha),
                "tipo_movimiento": mov.tipo_movimiento,
                "cantidad": mov.cantidad
            }
        }, status=status.HTTP_200_OK)

    def delete(self, request, id_producto, format=None):
      
        mov_id = request.data.get('id') or request.query_params.get('id')
        if not mov_id:
            return Response(
                {"error": "Debes enviar el 'id' del movimiento a eliminar"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            mov = Movimientos.objects.get(id=mov_id, producto_id=id_producto)
        except Movimientos.DoesNotExist:
            return Response(
                {"error": "Movimiento no encontrado para este producto"},
                status=status.HTTP_404_NOT_FOUND
            )

        mov.delete()
        return Response(
            {"message": f"Movimiento {mov_id} eliminado correctamente"},
            status=status.HTTP_200_OK
        )
