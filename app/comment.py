from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import db, Comment, Post

bp = Blueprint('comment', __name__, url_prefix='/comment')

@bp.route('/create/<int:post_id>', methods=['POST'])
@login_required
def create(post_id):
    """Crear un nuevo comentario"""
    post = Post.query.get_or_404(post_id)
    content = request.form.get('content')
    
    if not content or not content.strip():
        flash('El comentario no puede estar vacío.', 'danger')
        return redirect(url_for('post.view', post_id=post_id))
    
    comment = Comment(
        content=content,
        user_id=current_user.id,
        post_id=post_id
    )
    
    db.session.add(comment)
    db.session.commit()
    
    flash('Comentario agregado exitosamente.', 'success')
    return redirect(url_for('post.view', post_id=post_id))

@bp.route('/edit/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def edit(comment_id):
    """Editar un comentario"""
    comment = Comment.query.get_or_404(comment_id)
    
    # Verificar que el usuario sea el autor
    if comment.user_id != current_user.id:
        flash('No tienes permiso para editar este comentario.', 'danger')
        return redirect(url_for('post.view', post_id=comment.post_id))
    
    if request.method == 'POST':
        content = request.form.get('content')
        
        if not content or not content.strip():
            flash('El comentario no puede estar vacío.', 'danger')
            return redirect(url_for('post.view', post_id=comment.post_id))
        
        comment.content = content
        db.session.commit()
        
        flash('Comentario actualizado exitosamente.', 'success')
        return redirect(url_for('post.view', post_id=comment.post_id))
    
    return redirect(url_for('post.view', post_id=comment.post_id))

@bp.route('/delete/<int:comment_id>', methods=['POST'])
@login_required
def delete(comment_id):
    """Eliminar un comentario"""
    comment = Comment.query.get_or_404(comment_id)
    
    # Verificar que el usuario sea el autor o admin
    if comment.user_id != current_user.id and not current_user.is_admin():
        flash('No tienes permiso para eliminar este comentario.', 'danger')
        return redirect(url_for('post.view', post_id=comment.post_id))
    
    post_id = comment.post_id
    db.session.delete(comment)
    db.session.commit()
    
    flash('Comentario eliminado exitosamente.', 'info')
    return redirect(url_for('post.view', post_id=post_id))
