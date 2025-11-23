"""
Script para verificar usuario admin
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Crear app simple
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    role = db.Column(db.String(20), default='user')
    is_active = db.Column(db.Boolean, default=True)
    
    def is_admin(self):
        return self.role == 'admin'

with app.app_context():
    user = User.query.filter_by(username='robert').first()
    if user:
        print(f"✅ Usuario encontrado:")
        print(f"   Username: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Rol: {user.role}")
        print(f"   Activo: {user.is_active}")
        print(f"   Es admin: {user.is_admin()}")
        print()
        if user.is_admin():
            print("✅ El usuario ES administrador")
            print("   Debería ver el enlace 'Admin' en la navbar")
            print("   Puede acceder a: /admin/dashboard")
        else:
            print("❌ El usuario NO es administrador")
    else:
        print("❌ Usuario 'robert' no encontrado")
