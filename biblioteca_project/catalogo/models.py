from django.db import models
from django.utils import timezone


class Genero(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Género")

    class Meta:
        verbose_name = "Género"
        verbose_name_plural = "Géneros"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Autor(models.Model):
    nombre = models.CharField(max_length=150, verbose_name="Nombre")
    apellido = models.CharField(max_length=150, verbose_name="Apellido")
    fecha_nacimiento = models.DateField(null=True, blank=True, verbose_name="Fecha de nacimiento")
    nacionalidad = models.CharField(max_length=100, blank=True, verbose_name="Nacionalidad")
    biografia = models.TextField(blank=True, verbose_name="Biografía")

    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"


class Libro(models.Model):
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('prestado', 'Prestado'),
        ('reservado', 'Reservado'),
        ('mantenimiento', 'En mantenimiento'),
    ]

    titulo = models.CharField(max_length=300, verbose_name="Título")
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='libros', verbose_name="Autor")
    genero = models.ForeignKey(Genero, on_delete=models.SET_NULL, null=True, blank=True, related_name='libros', verbose_name="Género")
    isbn = models.CharField(max_length=20, unique=True, blank=True, null=True, verbose_name="ISBN")
    anio_publicacion = models.IntegerField(null=True, blank=True, verbose_name="Año de publicación")
    editorial = models.CharField(max_length=200, blank=True, verbose_name="Editorial")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    num_paginas = models.IntegerField(null=True, blank=True, verbose_name="Número de páginas")
    cantidad_total = models.IntegerField(default=1, verbose_name="Cantidad total")
    cantidad_disponible = models.IntegerField(default=1, verbose_name="Cantidad disponible")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible', verbose_name="Estado")
    fecha_ingreso = models.DateField(default=timezone.now, verbose_name="Fecha de ingreso")

    class Meta:
        verbose_name = "Libro"
        verbose_name_plural = "Libros"
        ordering = ['titulo']

    def __str__(self):
        return self.titulo


class Miembro(models.Model):
    TIPO_CHOICES = [
        ('estudiante', 'Estudiante'),
        ('docente', 'Docente'),
        ('externo', 'Externo'),
    ]
    nombre = models.CharField(max_length=150, verbose_name="Nombre")
    apellido = models.CharField(max_length=150, verbose_name="Apellido")
    email = models.EmailField(unique=True, verbose_name="Correo electrónico")
    telefono = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='estudiante', verbose_name="Tipo")
    fecha_registro = models.DateField(default=timezone.now, verbose_name="Fecha de registro")
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Miembro"
        verbose_name_plural = "Miembros"
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Prestamo(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('devuelto', 'Devuelto'),
        ('vencido', 'Vencido'),
    ]
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='prestamos', verbose_name="Libro")
    miembro = models.ForeignKey(Miembro, on_delete=models.CASCADE, related_name='prestamos', verbose_name="Miembro")
    fecha_prestamo = models.DateField(default=timezone.now, verbose_name="Fecha de préstamo")
    fecha_devolucion_esperada = models.DateField(verbose_name="Fecha de devolución esperada")
    fecha_devolucion_real = models.DateField(null=True, blank=True, verbose_name="Fecha de devolución real")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo', verbose_name="Estado")
    notas = models.TextField(blank=True, verbose_name="Notas")

    class Meta:
        verbose_name = "Préstamo"
        verbose_name_plural = "Préstamos"
        ordering = ['-fecha_prestamo']

    def __str__(self):
        return f"{self.libro.titulo} → {self.miembro}"

    def esta_vencido(self):
        if self.estado == 'activo' and self.fecha_devolucion_esperada < timezone.now().date():
            return True
        return False
