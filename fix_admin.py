"""
Script para activar usuario y asegurar que sea admin
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password_hash = db.Column(db.String(200))
    role = db.Column(db.String(20), default='user')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    user = User.query.filter_by(username='robert').first()
    if user:
        # Asegurar que está activo y es admin
        user.is_active = True
        user.role = 'admin'
        db.session.commit()
        
        print(f"✅ Usuario actualizado:")
        print(f"   Username: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Rol: {user.role}")
        print(f"   Activo: {user.is_active}")
        print()
        print("✅ Ahora puedes:")
        print("   1. Iniciar sesión con 'robert'")
        print("   2. Ver el enlace 'Admin' en la navbar")
        print("   3. Acceder a /admin/dashboard")
        print()
        print("⚠️  Reinicia el servidor (Ctrl+C y python run.py)")
    else:
        print("❌ Usuario no encontrado")
