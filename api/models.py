from django.db import models

# Modelo Producto actualizado
class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=50, blank=True, null=True)  # opcional

    def __str__(self):
        return self.nombre

# Modelo Movimientos
class Movimientos(models.Model):
    id = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='movimientos')  # Añadido related_name
    tipo_movimiento = models.CharField(max_length=100)
    cantidad = models.IntegerField(default=0)
    fecha = models.DateField()

    def __str__(self):
        return f"{self.tipo_movimiento} - {self.cantidad} unidades de {self.producto.nombre} en {self.fecha}"
