from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .decorators import admin_required
from .models import db, User, Post, Comment
from sqlalchemy import func

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Panel de administración principal"""
    # Estadísticas generales
    total_users = User.query.count()
    total_posts = Post.query.count()
    total_comments = Comment.query.count()
    
    # Usuarios recientes
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    # Publicaciones recientes
    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    
    # Estadísticas por categoría
    category_stats = db.session.query(
        Post.category,
        func.count(Post.id).label('count')
    ).group_by(Post.category).all()
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_posts=total_posts,
                         total_comments=total_comments,
                         recent_users=recent_users,
                         recent_posts=recent_posts,
                         category_stats=category_stats)

@bp.route('/users')
@login_required
@admin_required
def users():
    """Gestión de usuarios"""
    page = request.args.get('page', 1, type=int)
    pagination = User.query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    users = pagination.items
    return render_template('admin/users.html', users=users, pagination=pagination)

@bp.route('/users/change-role/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def change_role(user_id):
    """Cambiar rol de usuario"""
    user = User.query.get_or_404(user_id)
    new_role = request.form.get('role')
    
    if new_role not in ['user', 'editor', 'admin']:
        flash('Rol no válido.', 'danger')
        return redirect(url_for('admin.users'))
    
    # No permitir que el admin se quite sus propios permisos
    if user.id == current_user.id and new_role != 'admin':
        flash('No puedes cambiar tu propio rol de administrador.', 'danger')
        return redirect(url_for('admin.users'))
    
    user.role = new_role
    db.session.commit()
    
    flash(f'Rol de {user.username} cambiado a {new_role}.', 'success')
    return redirect(url_for('admin.users'))

@bp.route('/users/toggle-active/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def toggle_active(user_id):
    """Activar/desactivar usuario"""
    user = User.query.get_or_404(user_id)
    
    # No permitir desactivar al propio admin
    if user.id == current_user.id:
        flash('No puedes desactivar tu propia cuenta.', 'danger')
        return redirect(url_for('admin.users'))
    
    user.is_active = not user.is_active
    db.session.commit()
    
    status = 'activado' if user.is_active else 'desactivado'
    flash(f'Usuario {user.username} {status}.', 'success')
    return redirect(url_for('admin.users'))

@bp.route('/posts')
@login_required
@admin_required
def posts():
    """Gestión de publicaciones"""
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    posts = pagination.items
    return render_template('admin/posts.html', posts=posts, pagination=pagination)

@bp.route('/comments')
@login_required
@admin_required
def comments():
    """Gestión de comentarios"""
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    comments = pagination.items
    return render_template('admin/comments.html', comments=comments, pagination=pagination)
