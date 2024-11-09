from django.core.exceptions import ValidationError # type: ignore
from django.db import models # type: ignore

class Moneda(models.Model):
    nombre = models.CharField(max_length=50)  # e.g., "USD", "EUR", "MXN"
    tasa_cambio = models.DecimalField(max_digits=10, decimal_places=4)  # Exchange rate relative to CUP

    def __str__(self):
        return f"{self.nombre} - Tasa: {self.tasa_cambio}"

class Anuncio(models.Model):
    imagen = models.ImageField(upload_to='anuncios/')
    titulo = models.CharField(max_length=255)

    def __str__(self):
        return self.titulo


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=255)  # Obligatorio
    descripcion = models.TextField(null=True, blank=True)  # Opcional
    precio_normal = models.DecimalField(max_digits=10, decimal_places=2)  # Obligatorio
    precio_nuevo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Opcional
    imagen = models.ImageField(upload_to='productos/')  # Obligatorio
    es_nuevo = models.BooleanField(default=False)  # Opcional
    es_rebaja = models.BooleanField(default=False)  # Opcional
    domicilio_disponible = models.BooleanField(default=False)  # Opcional
    disponible = models.BooleanField(default=True)  # Obligatorio
    categorias_negocio = models.ManyToManyField(Categoria)  # Obligatorio
    valoracion = models.FloatField(null=True, blank=True)  # Opcional

    def __str__(self):
        return self.nombre

    def clean(self):
        # Validar que "es_nuevo" y "es_rebaja" no sean ambos True
        if self.es_nuevo and self.es_rebaja:
            raise ValidationError("Un producto no puede ser 'Nuevo' y estar en 'Rebaja' al mismo tiempo.")

        # Validar que si es rebaja, "precio_nuevo" debe estar definido
        if self.es_rebaja and self.precio_nuevo is None:
            raise ValidationError("Debes proporcionar un precio nuevo si el producto está en rebaja.")

        # Validar que si no es rebaja, "precio_nuevo" debe ser None
        if not self.es_rebaja and self.precio_nuevo is not None:
            raise ValidationError("El precio nuevo solo puede ser establecido si el producto está en rebaja.")

    def save(self, *args, **kwargs):
        # Ejecutar la validación antes de guardar
        self.clean()
        super().save(*args, **kwargs)


class Servicio(models.Model):
    titulo = models.CharField(max_length=255)
    imagen = models.ImageField(upload_to='servicios/')
    telefono = models.CharField(max_length=8)  # Teléfono de 8 dígitos

    def __str__(self):
        return self.titulo
