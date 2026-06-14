# 📚 BiblioTeca — Sistema de Gestión Bibliográfica
**Django + SQLite3 | Proyecto completo**

## 🚀 Cómo ejecutar

```bash
# 1. Instalar dependencias
pip install django

# 2. Aplicar migraciones (ya está hecho, pero si es nueva instalación)
python manage.py migrate

# 3. Cargar datos de ejemplo (opcional)
python seed_data.py

# 4. ¡Ejecutar el servidor!
python manage.py runserver
```

Luego abre: **http://127.0.0.1:8000**

## 🔑 Acceso al panel admin
- URL: http://127.0.0.1:8000/admin
- Usuario: `admin`
- Contraseña: `admin123`

## 🗄️ Base de datos SQLite3 (DB Browser)
El archivo `db.sqlite3` se encuentra en la raíz del proyecto.
Ábrelo con **DB Browser for SQLite** para ver las tablas:

| Tabla | Descripción |
|-------|-------------|
| `catalogo_libro` | Catálogo de libros |
| `catalogo_autor` | Autores registrados |
| `catalogo_miembro` | Miembros de la biblioteca |
| `catalogo_prestamo` | Registro de préstamos |
| `catalogo_genero` | Géneros literarios |

## 📂 Estructura del proyecto
```
biblioteca_project/
├── manage.py
├── db.sqlite3          ← Abrir con DB Browser
├── seed_data.py        ← Datos de ejemplo
├── README.md
├── biblioteca_project/ ← Configuración Django
│   ├── settings.py
│   └── urls.py
└── catalogo/           ← App principal
    ├── models.py       ← Modelos de BD
    ├── views.py        ← Lógica de vistas
    ├── urls.py         ← Rutas URL
    └── templates/      ← Plantillas HTML
```

## ✨ Funcionalidades
- ✅ Dashboard con estadísticas
- ✅ CRUD completo de libros, autores, miembros
- ✅ Sistema de préstamos y devoluciones
- ✅ Detección automática de préstamos vencidos
- ✅ Búsqueda y filtros
- ✅ Admin de Django incluido
