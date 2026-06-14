from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count
from .models import Libro, Autor, Miembro, Prestamo, Genero
from datetime import timedelta


# ─── DASHBOARD ───────────────────────────────────────────────────────────────
def dashboard(request):
    total_libros = Libro.objects.count()
    total_autores = Autor.objects.count()
    total_miembros = Miembro.objects.filter(activo=True).count()
    prestamos_activos = Prestamo.objects.filter(estado='activo').count()
    prestamos_vencidos = [p for p in Prestamo.objects.filter(estado='activo') if p.esta_vencido()]
    ultimos_prestamos = Prestamo.objects.select_related('libro', 'miembro').order_by('-fecha_prestamo')[:5]
    libros_populares = Libro.objects.annotate(num_prestamos=Count('prestamos')).order_by('-num_prestamos')[:5]

    context = {
        'total_libros': total_libros,
        'total_autores': total_autores,
        'total_miembros': total_miembros,
        'prestamos_activos': prestamos_activos,
        'prestamos_vencidos': len(prestamos_vencidos),
        'ultimos_prestamos': ultimos_prestamos,
        'libros_populares': libros_populares,
    }
    return render(request, 'catalogo/dashboard.html', context)


# ─── LIBROS ──────────────────────────────────────────────────────────────────
def lista_libros(request):
    query = request.GET.get('q', '')
    genero_id = request.GET.get('genero', '')
    estado = request.GET.get('estado', '')
    libros = Libro.objects.select_related('autor', 'genero').all()
    if query:
        libros = libros.filter(Q(titulo__icontains=query) | Q(autor__nombre__icontains=query) | Q(autor__apellido__icontains=query))
    if genero_id:
        libros = libros.filter(genero_id=genero_id)
    if estado:
        libros = libros.filter(estado=estado)
    generos = Genero.objects.all()
    return render(request, 'catalogo/libros.html', {'libros': libros, 'generos': generos, 'query': query, 'genero_id': genero_id, 'estado': estado})


def detalle_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    prestamos = libro.prestamos.select_related('miembro').order_by('-fecha_prestamo')[:5]
    return render(request, 'catalogo/libro_detalle.html', {'libro': libro, 'prestamos': prestamos})


def nuevo_libro(request):
    autores = Autor.objects.all()
    generos = Genero.objects.all()
    if request.method == 'POST':
        try:
            libro = Libro(
                titulo=request.POST['titulo'],
                autor_id=request.POST['autor'],
                genero_id=request.POST.get('genero') or None,
                isbn=request.POST.get('isbn') or None,
                anio_publicacion=request.POST.get('anio_publicacion') or None,
                editorial=request.POST.get('editorial', ''),
                descripcion=request.POST.get('descripcion', ''),
                num_paginas=request.POST.get('num_paginas') or None,
                cantidad_total=int(request.POST.get('cantidad_total', 1)),
                cantidad_disponible=int(request.POST.get('cantidad_total', 1)),
            )
            libro.save()
            messages.success(request, f'✅ Libro "{libro.titulo}" agregado exitosamente.')
            return redirect('detalle_libro', pk=libro.pk)
        except Exception as e:
            messages.error(request, f'Error: {e}')
    return render(request, 'catalogo/libro_form.html', {'autores': autores, 'generos': generos, 'accion': 'Nuevo'})


def editar_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    autores = Autor.objects.all()
    generos = Genero.objects.all()
    if request.method == 'POST':
        try:
            libro.titulo = request.POST['titulo']
            libro.autor_id = request.POST['autor']
            libro.genero_id = request.POST.get('genero') or None
            libro.isbn = request.POST.get('isbn') or None
            libro.anio_publicacion = request.POST.get('anio_publicacion') or None
            libro.editorial = request.POST.get('editorial', '')
            libro.descripcion = request.POST.get('descripcion', '')
            libro.num_paginas = request.POST.get('num_paginas') or None
            libro.cantidad_total = int(request.POST.get('cantidad_total', 1))
            libro.save()
            messages.success(request, f'✅ Libro actualizado.')
            return redirect('detalle_libro', pk=libro.pk)
        except Exception as e:
            messages.error(request, f'Error: {e}')
    return render(request, 'catalogo/libro_form.html', {'libro': libro, 'autores': autores, 'generos': generos, 'accion': 'Editar'})


def eliminar_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    if request.method == 'POST':
        titulo = libro.titulo
        libro.delete()
        messages.success(request, f'🗑️ Libro "{titulo}" eliminado.')
        return redirect('lista_libros')
    return render(request, 'catalogo/confirmar_eliminar.html', {'objeto': libro, 'tipo': 'libro'})


# ─── AUTORES ─────────────────────────────────────────────────────────────────
def lista_autores(request):
    query = request.GET.get('q', '')
    autores = Autor.objects.annotate(num_libros=Count('libros'))
    if query:
        autores = autores.filter(Q(nombre__icontains=query) | Q(apellido__icontains=query))
    return render(request, 'catalogo/autores.html', {'autores': autores, 'query': query})


def nuevo_autor(request):
    if request.method == 'POST':
        try:
            autor = Autor(
                nombre=request.POST['nombre'],
                apellido=request.POST['apellido'],
                fecha_nacimiento=request.POST.get('fecha_nacimiento') or None,
                nacionalidad=request.POST.get('nacionalidad', ''),
                biografia=request.POST.get('biografia', ''),
            )
            autor.save()
            messages.success(request, f'✅ Autor "{autor}" agregado.')
            return redirect('lista_autores')
        except Exception as e:
            messages.error(request, f'Error: {e}')
    return render(request, 'catalogo/autor_form.html', {'accion': 'Nuevo'})


def editar_autor(request, pk):
    autor = get_object_or_404(Autor, pk=pk)
    if request.method == 'POST':
        try:
            autor.nombre = request.POST['nombre']
            autor.apellido = request.POST['apellido']
            autor.fecha_nacimiento = request.POST.get('fecha_nacimiento') or None
            autor.nacionalidad = request.POST.get('nacionalidad', '')
            autor.biografia = request.POST.get('biografia', '')
            autor.save()
            messages.success(request, '✅ Autor actualizado.')
            return redirect('lista_autores')
        except Exception as e:
            messages.error(request, f'Error: {e}')
    return render(request, 'catalogo/autor_form.html', {'autor': autor, 'accion': 'Editar'})


def eliminar_autor(request, pk):
    autor = get_object_or_404(Autor, pk=pk)
    if request.method == 'POST':
        nombre = str(autor)
        autor.delete()
        messages.success(request, f'🗑️ Autor "{nombre}" eliminado.')
        return redirect('lista_autores')
    return render(request, 'catalogo/confirmar_eliminar.html', {'objeto': autor, 'tipo': 'autor'})


# ─── MIEMBROS ────────────────────────────────────────────────────────────────
def lista_miembros(request):
    query = request.GET.get('q', '')
    miembros = Miembro.objects.annotate(num_prestamos=Count('prestamos'))
    if query:
        miembros = miembros.filter(Q(nombre__icontains=query) | Q(apellido__icontains=query) | Q(email__icontains=query))
    return render(request, 'catalogo/miembros.html', {'miembros': miembros, 'query': query})


def nuevo_miembro(request):
    if request.method == 'POST':
        try:
            miembro = Miembro(
                nombre=request.POST['nombre'],
                apellido=request.POST['apellido'],
                email=request.POST['email'],
                telefono=request.POST.get('telefono', ''),
                tipo=request.POST.get('tipo', 'estudiante'),
            )
            miembro.save()
            messages.success(request, f'✅ Miembro "{miembro}" registrado.')
            return redirect('lista_miembros')
        except Exception as e:
            messages.error(request, f'Error: {e}')
    return render(request, 'catalogo/miembro_form.html', {'accion': 'Nuevo'})


def editar_miembro(request, pk):
    miembro = get_object_or_404(Miembro, pk=pk)
    if request.method == 'POST':
        try:
            miembro.nombre = request.POST['nombre']
            miembro.apellido = request.POST['apellido']
            miembro.email = request.POST['email']
            miembro.telefono = request.POST.get('telefono', '')
            miembro.tipo = request.POST.get('tipo', 'estudiante')
            miembro.activo = 'activo' in request.POST
            miembro.save()
            messages.success(request, '✅ Miembro actualizado.')
            return redirect('lista_miembros')
        except Exception as e:
            messages.error(request, f'Error: {e}')
    return render(request, 'catalogo/miembro_form.html', {'miembro': miembro, 'accion': 'Editar'})


def eliminar_miembro(request, pk):
    miembro = get_object_or_404(Miembro, pk=pk)
    if request.method == 'POST':
        nombre = str(miembro)
        miembro.delete()
        messages.success(request, f'🗑️ Miembro "{nombre}" eliminado.')
        return redirect('lista_miembros')
    return render(request, 'catalogo/confirmar_eliminar.html', {'objeto': miembro, 'tipo': 'miembro'})


# ─── PRÉSTAMOS ───────────────────────────────────────────────────────────────
def lista_prestamos(request):
    estado = request.GET.get('estado', '')
    prestamos = Prestamo.objects.select_related('libro', 'miembro').all()
    if estado:
        prestamos = prestamos.filter(estado=estado)
    hoy = timezone.now().date()
    for p in prestamos:
        if p.estado == 'activo' and p.fecha_devolucion_esperada < hoy:
            p.estado = 'vencido'
            p.save()
    return render(request, 'catalogo/prestamos.html', {'prestamos': prestamos, 'estado': estado})


def nuevo_prestamo(request):
    libros = Libro.objects.filter(cantidad_disponible__gt=0)
    miembros = Miembro.objects.filter(activo=True)
    if request.method == 'POST':
        try:
            libro = get_object_or_404(Libro, pk=request.POST['libro'])
            miembro = get_object_or_404(Miembro, pk=request.POST['miembro'])
            dias = int(request.POST.get('dias_prestamo', 14))
            prestamo = Prestamo(
                libro=libro,
                miembro=miembro,
                fecha_devolucion_esperada=timezone.now().date() + timedelta(days=dias),
                notas=request.POST.get('notas', ''),
            )
            prestamo.save()
            libro.cantidad_disponible = max(0, libro.cantidad_disponible - 1)
            if libro.cantidad_disponible == 0:
                libro.estado = 'prestado'
            libro.save()
            messages.success(request, f'✅ Préstamo registrado: "{libro.titulo}" → {miembro}')
            return redirect('lista_prestamos')
        except Exception as e:
            messages.error(request, f'Error: {e}')
    return render(request, 'catalogo/prestamo_form.html', {'libros': libros, 'miembros': miembros})


def devolver_libro(request, pk):
    prestamo = get_object_or_404(Prestamo, pk=pk)
    if request.method == 'POST':
        prestamo.estado = 'devuelto'
        prestamo.fecha_devolucion_real = timezone.now().date()
        prestamo.save()
        libro = prestamo.libro
        libro.cantidad_disponible = min(libro.cantidad_total, libro.cantidad_disponible + 1)
        libro.estado = 'disponible'
        libro.save()
        messages.success(request, f'📚 Libro "{libro.titulo}" devuelto exitosamente.')
        return redirect('lista_prestamos')
    return render(request, 'catalogo/confirmar_devolucion.html', {'prestamo': prestamo})
