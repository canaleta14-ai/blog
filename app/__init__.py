from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS
from .models import db, User
from config import config

def create_app(config_name='default'):
    """Factory para crear la aplicación Flask"""
    app = Flask(__name__)
    
    # Cargar configuración
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Configurar Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Registrar blueprints
    from .home import bp as home_bp
    app.register_blueprint(home_bp)
    
    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    
    from .post import bp as post_bp
    app.register_blueprint(post_bp)
    
    from .comment import bp as comment_bp
    app.register_blueprint(comment_bp)
    
    from .admin import bp as admin_bp
    app.register_blueprint(admin_bp)
    
    from .api import bp as api_bp
    app.register_blueprint(api_bp)
    
    # Configurar CORS para el blueprint API
    CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})
    
    # Crear tablas si no existen (solo para desarrollo)
    with app.app_context():
        try:
            db.create_all()
            print("Tablas creadas/verficadas exitosamente")
        except Exception as e:
            print(f"Error al crear tablas: {e}")
            # En producción, las migraciones deberían manejar esto
            pass
    
    return app