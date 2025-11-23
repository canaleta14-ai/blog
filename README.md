# Blog Flask - Proyecto Completo

Sistema de blog completo desarrollado con Flask, incluyendo autenticación, CRUD de publicaciones, comentarios, panel de administración y API REST.

## Características

✅ **Autenticación de Usuarios**
- Registro y login
- Gestión de sesiones con Flask-Login
- Contraseñas hasheadas

✅ **Gestión de Publicaciones**
- CRUD completo
- Categorías
- Upload de imágenes
- Paginación (6 posts/página)

✅ **Sistema de Comentarios**
- Comentarios en publicaciones
- Solo autenticados pueden comentar
- Eliminar comentarios propios

✅ **Búsqueda**
- Búsqueda en título y contenido
- Resultados paginados

✅ **Sistema de Roles**
- Roles: user, editor, admin
- Permisos por rol

✅ **Panel de Administración**
- Dashboard con estadísticas
- Gestión de usuarios
- Cambiar roles
- Activar/desactivar usuarios

✅ **API REST**
- Autenticación JWT
- Endpoints CRUD de posts
- Endpoints de comentarios
- CORS configurado

✅ **Tests**
- Tests unitarios
- Tests de API
- Pytest configurado

## Instalación

```bash
# Clonar repositorio
git clone <url>
cd blog-posts

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Crear usuario admin
python create_admin.py

# Ejecutar aplicación
python run.py
```

## Uso

### Aplicación Web
- Acceder a `http://127.0.0.1:5000`
- Registrarse o iniciar sesión
- Crear publicaciones
- Comentar
- Panel admin: `/admin/dashboard` (solo admins)

### API REST

**Obtener token:**
```bash
curl -X POST http://127.0.0.1:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

**Listar publicaciones:**
```bash
curl http://127.0.0.1:5000/api/posts
```

**Crear publicación:**
```bash
curl -X POST http://127.0.0.1:5000/api/posts \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title":"Mi Post","content":"Contenido","category":"tecnologia"}'
```

## Tests

```bash
# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=app

# Tests específicos
pytest tests/test_api.py
pytest tests/test_models.py
```

## Estructura del Proyecto

```
blog-posts/
├── app/
│   ├── static/
│   │   ├── style.css
│   │   └── uploads/
│   ├── templates/
│   │   ├── auth/
│   │   ├── post/
│   │   ├── admin/
│   │   ├── base.html
│   │   ├── blog.html
│   │   ├── home.html
│   │   └── search.html
│   ├── __init__.py
│   ├── models.py
│   ├── auth.py
│   ├── home.py
│   ├── post.py
│   ├── comment.py
│   ├── admin.py
│   ├── api.py
│   └── decorators.py
├── tests/
│   ├── conftest.py
│   ├── test_api.py
│   └── test_models.py
├── config.py
├── run.py
├── create_admin.py
├── requirements.txt
└── README.md
```

## Tecnologías

- **Backend:** Flask 3.0.0
- **Base de Datos:** SQLAlchemy + SQLite
- **Autenticación:** Flask-Login + JWT
- **Frontend:** Bootstrap 5
- **Tests:** Pytest
- **API:** Flask-CORS

## Endpoints API

### Autenticación
- `POST /api/auth/login` - Obtener token JWT

### Publicaciones
- `GET /api/posts` - Listar publicaciones
- `GET /api/posts/<id>` - Ver publicación
- `POST /api/posts` - Crear (requiere token)
- `PUT /api/posts/<id>` - Actualizar (requiere token)
- `DELETE /api/posts/<id>` - Eliminar (requiere token)

### Comentarios
- `GET /api/posts/<id>/comments` - Listar comentarios
- `POST /api/posts/<id>/comments` - Crear (requiere token)

### Usuarios
- `GET /api/users/<id>` - Ver usuario

## Configuración

Variables de entorno (opcional):
```
SECRET_KEY=tu-clave-secreta
JWT_SECRET_KEY=tu-jwt-secret
DATABASE_URL=sqlite:///blog.db
```

## Licencia

MIT
