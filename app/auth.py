from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import db, User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registro de nuevos usuarios"""
    # Si el usuario ya está autenticado, redirigir al inicio
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validaciones
        if not username or not email or not password:
            flash('Todos los campos son obligatorios.', 'danger')
            return render_template('auth/register.html')
        
        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'danger')
            return render_template('auth/register.html')
        
        # Verificar si el usuario ya existe
        if User.query.filter_by(username=username).first():
            flash('El nombre de usuario ya está en uso.', 'danger')
            return render_template('auth/register.html')
        
        if User.query.filter_by(email=email).first():
            flash('El correo electrónico ya está registrado.', 'danger')
            return render_template('auth/register.html')
        
        # Crear nuevo usuario
        user = User(username=username, email=email)
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            print(f"Error al registrar usuario: {e}")  # Para logs
            flash('Error al registrar usuario. Inténtalo de nuevo.', 'danger')
            return render_template('auth/register.html')
    
    return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Inicio de sesión de usuarios"""
    # Si el usuario ya está autenticado, redirigir al inicio
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        # Validaciones
        if not email or not password:
            flash('Por favor ingresa tu correo y contraseña.', 'danger')
            return render_template('auth/login.html')
        
        # Buscar usuario por email
        user = User.query.filter_by(email=email).first()
        
        # Verificar credenciales
        if user and user.check_password(password):
            login_user(user, remember=bool(remember))
            flash(f'¡Bienvenido, {user.username}!', 'success')
            
            # Redirigir a la página solicitada o al inicio
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home.index'))
        else:
            flash('Correo o contraseña incorrectos.', 'danger')
    
    return render_template('auth/login.html')


@bp.route('/logout')
@login_required
def logout():
    """Cierre de sesión"""
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('home.index'))


@bp.route('/profile')
@login_required
def profile():
    """Perfil del usuario"""
    # Obtener las publicaciones del usuario
    posts = current_user.posts
    return render_template('auth/profile.html', posts=posts)