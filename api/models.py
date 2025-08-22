from django.db import models

class Sede(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=200)
    stock = models.IntegerField(default=0)
    url_imagen = models.TextField(null=True, blank=True)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)

    class Meta:
        # No se permite que haya dos productos con el mismo codigo en la misma sede.
        unique_together = ['codigo', 'sede']

    def __str__(self):
        return self.nombre
