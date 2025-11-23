"""
Script para crear un usuario administrador
Ejecutar con: python create_admin.py
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from datetime import datetime

# Crear app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definir modelo User (copia del original)
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='user')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    # Buscar el primer usuario
    user = User.query.first()
    
    if user:
        # Cambiar rol a admin
        user.role = 'admin'
        db.session.commit()
        print(f"✅ Usuario '{user.username}' (ID: {user.id}) ahora es administrador")
        print(f"   Email: {user.email}")
        print(f"   Rol: {user.role}")
        print("\n🔐 Ahora puedes acceder al panel de administración en /admin/dashboard")
    else:
        # Crear usuario admin
        admin = User(
            username='admin',
            email='admin@blog.com',
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Usuario administrador creado:")
        print("   Username: admin")
        print("   Email: admin@blog.com")
        print("   Password: admin123")
        print("\n⚠️  Cambia la contraseña después de iniciar sesión")
        print("🔐 Accede al panel de administración en /admin/dashboard")
