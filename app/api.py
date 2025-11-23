from flask import Blueprint, request, jsonify
from flask_cors import CORS
from functools import wraps
import jwt
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash
from .models import db, User, Post, Comment

bp = Blueprint('api', __name__, url_prefix='/api')

# Configurar CORS para el blueprint
CORS(bp)

def token_required(f):
    """Decorador para requerir token JWT"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token faltante'}), 401
        
        try:
            # Remover 'Bearer ' si está presente
            if token.startswith('Bearer '):
                token = token[7:]
            
            # Decodificar token
            from flask import current_app
            data = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            
            if not current_user:
                return jsonify({'error': 'Usuario no encontrado'}), 401
                
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token inválido'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

# ==================== AUTENTICACIÓN ====================

@bp.route('/auth/login', methods=['POST'])
def login():
    """Obtener token JWT con credenciales"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username y password requeridos'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Credenciales inválidas'}), 401
    
    # Generar token
    from flask import current_app
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.utcnow() + current_app.config['JWT_ACCESS_TOKEN_EXPIRES']
    }, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
    
    return jsonify({
        'token': token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
    }), 200

# ==================== PUBLICACIONES ====================

@bp.route('/posts', methods=['GET'])
def get_posts():
    """Listar todas las publicaciones"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    pagination = Post.query.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    posts = [{
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'category': post.category,
        'image_url': post.image_url,
        'created_at': post.created_at.isoformat(),
        'updated_at': post.updated_at.isoformat(),
        'author': {
            'id': post.author.id,
            'username': post.author.username
        }
    } for post in pagination.items]
    
    return jsonify({
        'posts': posts,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page
    }), 200

@bp.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Obtener una publicación específica"""
    post = Post.query.get_or_404(post_id)
    
    return jsonify({
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'category': post.category,
        'image_url': post.image_url,
        'created_at': post.created_at.isoformat(),
        'updated_at': post.updated_at.isoformat(),
        'author': {
            'id': post.author.id,
            'username': post.author.username,
            'email': post.author.email
        },
        'comments_count': len(post.comments)
    }), 200

@bp.route('/posts', methods=['POST'])
@token_required
def create_post(current_user):
    """Crear nueva publicación (requiere autenticación)"""
    data = request.get_json()
    
    if not data or not data.get('title') or not data.get('content'):
        return jsonify({'error': 'Título y contenido requeridos'}), 400
    
    post = Post(
        title=data['title'],
        content=data['content'],
        category=data.get('category', 'otros'),
        user_id=current_user.id
    )
    
    db.session.add(post)
    db.session.commit()
    
    return jsonify({
        'message': 'Publicación creada',
        'post': {
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'category': post.category
        }
    }), 201

@bp.route('/posts/<int:post_id>', methods=['PUT'])
@token_required
def update_post(current_user, post_id):
    """Actualizar publicación (solo el autor)"""
    post = Post.query.get_or_404(post_id)
    
    if post.user_id != current_user.id:
        return jsonify({'error': 'No autorizado'}), 403
    
    data = request.get_json()
    
    if data.get('title'):
        post.title = data['title']
    if data.get('content'):
        post.content = data['content']
    if data.get('category'):
        post.category = data['category']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Publicación actualizada',
        'post': {
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'category': post.category
        }
    }), 200

@bp.route('/posts/<int:post_id>', methods=['DELETE'])
@token_required
def delete_post(current_user, post_id):
    """Eliminar publicación (solo el autor)"""
    post = Post.query.get_or_404(post_id)
    
    if post.user_id != current_user.id:
        return jsonify({'error': 'No autorizado'}), 403
    
    db.session.delete(post)
    db.session.commit()
    
    return jsonify({'message': 'Publicación eliminada'}), 200

# ==================== COMENTARIOS ====================

@bp.route('/posts/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    """Obtener comentarios de una publicación"""
    post = Post.query.get_or_404(post_id)
    
    comments = [{
        'id': comment.id,
        'content': comment.content,
        'created_at': comment.created_at.isoformat(),
        'author': {
            'id': comment.author.id,
            'username': comment.author.username
        }
    } for comment in post.comments.order_by(Comment.created_at.desc()).all()]
    
    return jsonify({'comments': comments}), 200

@bp.route('/posts/<int:post_id>/comments', methods=['POST'])
@token_required
def create_comment(current_user, post_id):
    """Crear comentario (requiere autenticación)"""
    post = Post.query.get_or_404(post_id)
    data = request.get_json()
    
    if not data or not data.get('content'):
        return jsonify({'error': 'Contenido requerido'}), 400
    
    comment = Comment(
        content=data['content'],
        user_id=current_user.id,
        post_id=post_id
    )
    
    db.session.add(comment)
    db.session.commit()
    
    return jsonify({
        'message': 'Comentario creado',
        'comment': {
            'id': comment.id,
            'content': comment.content
        }
    }), 201

# ==================== USUARIOS ====================

@bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Obtener información de usuario"""
    user = User.query.get_or_404(user_id)
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'created_at': user.created_at.isoformat(),
        'posts_count': len(user.posts)
    }), 200
