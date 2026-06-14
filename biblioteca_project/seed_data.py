import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biblioteca_project.settings')
sys.path.insert(0, '/home/claude/biblioteca_project')
django.setup()

from catalogo.models import Autor, Libro, Miembro, Prestamo, Genero
from datetime import date, timedelta

# Géneros
generos_data = ['Novela', 'Ciencia Ficción', 'Historia', 'Poesía', 'Filosofía', 'Tecnología', 'Biografía']
generos = {g: Genero.objects.get_or_create(nombre=g)[0] for g in generos_data}

# Autores
autores_data = [
    ('Gabriel', 'García Márquez', '1927-03-06', 'Colombiana'),
    ('Jorge Luis', 'Borges', '1899-08-24', 'Argentina'),
    ('Octavio', 'Paz', '1914-03-31', 'Mexicana'),
    ('Isabel', 'Allende', '1942-08-02', 'Chilena'),
    ('Mario', 'Vargas Llosa', '1936-03-28', 'Peruana'),
    ('Laura', 'Esquivel', '1950-09-30', 'Mexicana'),
]
autores = []
for n, a, fn, nac in autores_data:
    obj, _ = Autor.objects.get_or_create(nombre=n, apellido=a, defaults={'fecha_nacimiento': fn, 'nacionalidad': nac})
    autores.append(obj)

# Libros
libros_data = [
    ('Cien años de soledad', autores[0], 'Novela', '978-84-397-0494-0', 1967, 'Sudamericana', 432, 3),
    ('El amor en los tiempos del cólera', autores[0], 'Novela', '978-84-397-0679-1', 1985, 'Oveja Negra', 474, 2),
    ('Ficciones', autores[1], 'Novela', '978-84-206-1309-9', 1944, 'Sur', 224, 4),
    ('El Aleph', autores[1], 'Novela', '978-84-206-1310-5', 1949, 'Losada', 160, 2),
    ('El laberinto de la soledad', autores[2], 'Filosofía', '978-968-16-0289-3', 1950, 'FCE', 191, 3),
    ('La casa de los espíritus', autores[3], 'Novela', '978-84-9793-690-7', 1982, 'Plaza & Janés', 432, 2),
    ('La ciudad y los perros', autores[4], 'Novela', '978-84-322-0158-0', 1963, 'Seix Barral', 364, 2),
    ('Como agua para chocolate', autores[5], 'Novela', '978-968-6941-02-3', 1989, 'Planeta', 245, 5),
    ('Crónica de una muerte anunciada', autores[0], 'Novela', '978-84-397-1223-5', 1981, 'Norma', 120, 3),
    ('Rayuela', autores[1], 'Novela', None, 1963, 'Sudamericana', 635, 2),
]

libros = []
for titulo, autor, genero, isbn, anio, editorial, paginas, cant in libros_data:
    obj, _ = Libro.objects.get_or_create(titulo=titulo, defaults={
        'autor': autor, 'genero': generos[genero], 'isbn': isbn,
        'anio_publicacion': anio, 'editorial': editorial,
        'num_paginas': paginas, 'cantidad_total': cant, 'cantidad_disponible': cant
    })
    libros.append(obj)

# Miembros
miembros_data = [
    ('Ana', 'González', 'ana.gonzalez@uni.mx', '555-0101', 'estudiante'),
    ('Carlos', 'Ramírez', 'carlos.r@uni.mx', '555-0102', 'estudiante'),
    ('María', 'López', 'mlopez@docente.mx', '555-0103', 'docente'),
    ('Juan', 'Hernández', 'juan.h@uni.mx', '555-0104', 'estudiante'),
    ('Sofía', 'Torres', 'sofia.t@ext.mx', '555-0105', 'externo'),
]
miembros = []
for n, a, e, t, tipo in miembros_data:
    obj, _ = Miembro.objects.get_or_create(email=e, defaults={'nombre': n, 'apellido': a, 'telefono': t, 'tipo': tipo})
    miembros.append(obj)

# Préstamos de ejemplo
from django.utils import timezone
hoy = timezone.now().date()

if Prestamo.objects.count() == 0:
    ejemplos = [
        (libros[0], miembros[0], hoy - timedelta(days=5), hoy + timedelta(days=9), 'activo'),
        (libros[2], miembros[1], hoy - timedelta(days=10), hoy + timedelta(days=4), 'activo'),
        (libros[4], miembros[2], hoy - timedelta(days=20), hoy - timedelta(days=6), 'vencido'),
        (libros[6], miembros[3], hoy - timedelta(days=30), hoy - timedelta(days=16), 'devuelto'),
        (libros[7], miembros[4], hoy - timedelta(days=3), hoy + timedelta(days=11), 'activo'),
    ]
    for libro, miembro, fp, fde, estado in ejemplos:
        p = Prestamo.objects.create(
            libro=libro, miembro=miembro,
            fecha_prestamo=fp, fecha_devolucion_esperada=fde,
            estado=estado,
            fecha_devolucion_real=fde if estado == 'devuelto' else None
        )
        if estado in ('activo', 'vencido'):
            libro.cantidad_disponible = max(0, libro.cantidad_disponible - 1)
            if libro.cantidad_disponible == 0:
                libro.estado = 'prestado'
            libro.save()

print("✅ Datos de ejemplo cargados correctamente.")
print(f"   {Genero.objects.count()} géneros")
print(f"   {Autor.objects.count()} autores")
print(f"   {Libro.objects.count()} libros")
print(f"   {Miembro.objects.count()} miembros")
print(f"   {Prestamo.objects.count()} préstamos")
