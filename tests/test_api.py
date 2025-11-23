"""
Tests para la API REST
"""
import json

def test_login_success(client):
    """Test de login exitoso"""
    from app.models import User, db
    from flask import current_app
    
    with current_app.app_context():
        # Crear usuario
        user = User(username='testuser', email='test@test.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
    
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'token' in data
    assert data['user']['username'] == 'testuser'

def test_login_invalid_credentials(client):
    """Test de login con credenciales inválidas"""
    response = client.post('/api/auth/login', json={
        'username': 'noexiste',
        'password': 'wrong'
    })
    
    assert response.status_code == 401

def test_get_posts(client):
    """Test de obtener lista de publicaciones"""
    response = client.get('/api/posts')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'posts' in data
    assert 'total' in data

def test_get_post(client):
    """Test de obtener publicación específica"""
    from app.models import User, Post, db
    from flask import current_app
    
    with current_app.app_context():
        # Crear usuario y publicación
        user = User(username='author', email='author@test.com')
        user.set_password('pass')
        db.session.add(user)
        db.session.commit()
        
        post = Post(title='Test Post', content='Content', user_id=user.id)
        db.session.add(post)
        db.session.commit()
        post_id = post.id
    
    response = client.get(f'/api/posts/{post_id}')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Test Post'

def test_create_post_without_auth(client):
    """Test de crear publicación sin autenticación"""
    response = client.post('/api/posts', json={
        'title': 'Test',
        'content': 'Content'
    })
    
    assert response.status_code == 401

def test_create_post_with_auth(client, auth_headers):
    """Test de crear publicación con autenticación"""
    response = client.post('/api/posts', 
        headers=auth_headers,
        json={
            'title': 'New Post',
            'content': 'New Content',
            'category': 'tecnologia'
        }
    )
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['post']['title'] == 'New Post'
