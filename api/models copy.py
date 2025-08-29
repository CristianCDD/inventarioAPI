from django.db import models

class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=50)  # Usamos CharField si el código es alfanumérico

    def __str__(self):
        return self.nombre

class Movimientos(models.Model):
    id = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Referencia al producto
    tipo_movimiento = models.CharField(max_length=100)  # Tipo de movimiento (entrada, salida, etc.)
    cantidad = models.IntegerField(default=0)  # Cantidad del movimiento
    fecha = models.DateField()  # Solo la fecha, sin hora

    def __str__(self):
        return f"{self.tipo_movimiento} - {self.cantidad} unidades de {self.producto.nombre} en {self.fecha}"
