"""
Punto de entrada de la aplicación Flask
"""
import os
from dotenv import load_dotenv
from app import create_app

# Cargar variables de entorno desde .env
load_dotenv()

# Crear aplicación
app = create_app()

if __name__ == '__main__':
    # Solo para desarrollo local
    # En producción, usar Gunicorn (ver Procfile)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_ENV') != 'production')