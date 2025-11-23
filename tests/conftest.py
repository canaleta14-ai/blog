"""
Configuración de tests con pytest
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app import create_app
from app.models import db, User, Post

@pytest.fixture
def app():
    """Crear aplicación para tests"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Cliente de prueba"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Runner CLI"""
    return app.test_cli_runner()

@pytest.fixture
def auth_headers(client, app):
    """Headers con token de autenticación"""
    with app.app_context():
        # Crear usuario de prueba
        user = User(username='testuser', email='test@test.com', role='user')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
    
    # Obtener token
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    
    token = response.get_json()['token']
    return {'Authorization': f'Bearer {token}'}
