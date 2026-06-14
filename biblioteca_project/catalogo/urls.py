from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    # Libros
    path('libros/', views.lista_libros, name='lista_libros'),
    path('libros/nuevo/', views.nuevo_libro, name='nuevo_libro'),
    path('libros/<int:pk>/', views.detalle_libro, name='detalle_libro'),
    path('libros/<int:pk>/editar/', views.editar_libro, name='editar_libro'),
    path('libros/<int:pk>/eliminar/', views.eliminar_libro, name='eliminar_libro'),
    # Autores
    path('autores/', views.lista_autores, name='lista_autores'),
    path('autores/nuevo/', views.nuevo_autor, name='nuevo_autor'),
    path('autores/<int:pk>/editar/', views.editar_autor, name='editar_autor'),
    path('autores/<int:pk>/eliminar/', views.eliminar_autor, name='eliminar_autor'),
    # Miembros
    path('miembros/', views.lista_miembros, name='lista_miembros'),
    path('miembros/nuevo/', views.nuevo_miembro, name='nuevo_miembro'),
    path('miembros/<int:pk>/editar/', views.editar_miembro, name='editar_miembro'),
    path('miembros/<int:pk>/eliminar/', views.eliminar_miembro, name='eliminar_miembro'),
    # Préstamos
    path('prestamos/', views.lista_prestamos, name='lista_prestamos'),
    path('prestamos/nuevo/', views.nuevo_prestamo, name='nuevo_prestamo'),
    path('prestamos/<int:pk>/devolver/', views.devolver_libro, name='devolver_libro'),
]
