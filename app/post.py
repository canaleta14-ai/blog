from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .models import db, Post, Comment
import os
import uuid

bp = Blueprint('post', __name__, url_prefix='/post')

def allowed_file(filename):
    """Verificar si el archivo tiene una extensión permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_image(file):
    """Guardar imagen y retornar la URL"""
    if file and allowed_file(file.filename):
        # Generar nombre único
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        
        # Crear carpeta si no existe
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        
        # Guardar archivo
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        # Retornar URL relativa
        return f"uploads/{filename}"
    return None

@bp.route('/post')
def post():
    """Listar todas las publicaciones"""
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('post/post.html', posts=posts)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Crear nueva publicación"""
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category', 'otros')
        
        # Validaciones
        if not title or not content:
            flash('El título y el contenido son obligatorios.', 'danger')
            return render_template('post/create.html')
        
        # Manejar imagen
        image_url = None
        if 'image' in request.files:
            file = request.files['image']
            if file.filename:
                image_url = save_image(file)
                if not image_url:
                    flash('Formato de imagen no válido. Use PNG, JPG, JPEG, GIF o WEBP.', 'warning')
        
        # Crear nueva publicación
        post = Post(
            title=title,
            content=content,
            category=category,
            image_url=image_url,
            user_id=current_user.id
        )
        
        db.session.add(post)
        db.session.commit()
        
        flash('¡Publicación creada exitosamente!', 'success')
        return redirect(url_for('home.blog'))
    
    return render_template('post/create.html')

@bp.route('/update/<int:post_id>', methods=['GET', 'POST'])
@login_required
def update(post_id):
    """Actualizar publicación existente"""
    post = Post.query.get_or_404(post_id)
    
    # Verificar que el usuario sea el autor
    if post.user_id != current_user.id:
        flash('No tienes permiso para editar esta publicación.', 'danger')
        return redirect(url_for('home.blog'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category', 'otros')
        
        # Validaciones
        if not title or not content:
            flash('El título y el contenido son obligatorios.', 'danger')
            return render_template('post/update.html', post=post)
        
        # Manejar imagen
        if 'image' in request.files:
            file = request.files['image']
            if file.filename:
                image_url = save_image(file)
                if image_url:
                    post.image_url = image_url
                else:
                    flash('Formato de imagen no válido.', 'warning')
        
        # Actualizar publicación
        post.title = title
        post.content = content
        post.category = category
        
        db.session.commit()
        
        flash('¡Publicación actualizada exitosamente!', 'success')
        return redirect(url_for('post.view', post_id=post.id))
    
    return render_template('post/update.html', post=post)

@bp.route('/delete/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete(post_id):
    """Eliminar publicación"""
    post = Post.query.get_or_404(post_id)
    
    # Verificar que el usuario sea el autor
    if post.user_id != current_user.id:
        flash('No tienes permiso para eliminar esta publicación.', 'danger')
        return redirect(url_for('home.blog'))
    
    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        
        flash('Publicación eliminada exitosamente.', 'info')
        return redirect(url_for('home.blog'))
    
    return render_template('post/delete.html', post=post)

@bp.route('/view/<int:post_id>')
def view(post_id):
    """Ver detalles de una publicación"""
    post = Post.query.get_or_404(post_id)
    comments = post.comments.order_by(Comment.created_at.desc()).all()
    return render_template('post/view.html', post=post, comments=comments)