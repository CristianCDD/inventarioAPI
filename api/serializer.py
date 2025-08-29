from rest_framework import serializers
from .models import Producto, Movimientos

# Serializer para Producto
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'  # Incluye todos los campos del modelo Producto

# Serializer para Movimientos
class MovimientosSerializer(serializers.ModelSerializer):
    producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())  # Esto generará un select con los IDs de los productos

    class Meta:
        model = Movimientos
        fields = '__all__'  # Incluye todos los campos del modelo Movimientos
