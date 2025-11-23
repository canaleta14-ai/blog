from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def admin_required(f):
    """Decorador para requerir rol de administrador"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Por favor inicia sesión para acceder a esta página.', 'warning')
            return redirect(url_for('auth.login'))
        
        if not current_user.is_admin():
            flash('No tienes permisos de administrador.', 'danger')
            return redirect(url_for('home.index'))
        
        return f(*args, **kwargs)
    return decorated_function

def editor_required(f):
    """Decorador para requerir rol de editor o superior"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Por favor inicia sesión para acceder a esta página.', 'warning')
            return redirect(url_for('auth.login'))
        
        if not current_user.is_editor():
            flash('No tienes permisos de editor.', 'danger')
            return redirect(url_for('home.index'))
        
        return f(*args, **kwargs)
    return decorated_function
