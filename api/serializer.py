from rest_framework import serializers
from .models import Producto, Sede

# Serializer para Sede
class SedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sede
        fields = '__all__'  # Puedes especificar los campos que desees, por ejemplo: ['id', 'nombre']

# Serializer para Producto
class ProductoSerializer(serializers.ModelSerializer):
    sede = serializers.PrimaryKeyRelatedField(queryset=Sede.objects.all())  # Usa el ID de la sede

    class Meta:
        model = Producto
        fields = '__all__'
