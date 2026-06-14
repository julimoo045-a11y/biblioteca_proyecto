from django.contrib import admin
from .models import Libro, Autor, Miembro, Prestamo, Genero

@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ['nombre']

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellido', 'nacionalidad', 'fecha_nacimiento']
    search_fields = ['nombre', 'apellido']

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'genero', 'anio_publicacion', 'estado', 'cantidad_disponible']
    list_filter = ['estado', 'genero']
    search_fields = ['titulo', 'isbn']

@admin.register(Miembro)
class MiembroAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellido', 'email', 'tipo', 'activo']
    list_filter = ['tipo', 'activo']

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ['libro', 'miembro', 'fecha_prestamo', 'fecha_devolucion_esperada', 'estado']
    list_filter = ['estado']
