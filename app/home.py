from flask import Blueprint, render_template, request
from .models import Post

bp = Blueprint('home', __name__)

@bp.route('/')
def index():
    """Página de inicio"""
    return render_template('home.html')

@bp.route('/blog')
def blog():
    """Listar todas las publicaciones del blog con paginación"""
    page = request.args.get('page', 1, type=int)
    per_page = 6
    
    pagination = Post.query.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    posts = pagination.items
    
    return render_template('blog.html', posts=posts, pagination=pagination)

@bp.route('/search')
def search():
    """Buscar publicaciones por título o contenido"""
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    per_page = 6
    
    if query:
        # Buscar en título y contenido
        search_filter = Post.title.ilike(f'%{query}%') | Post.content.ilike(f'%{query}%')
        pagination = Post.query.filter(search_filter).order_by(Post.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
    else:
        pagination = Post.query.order_by(Post.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
    
    posts = pagination.items
    
    return render_template('search.html', posts=posts, pagination=pagination, query=query)