#!/usr/bin/env python3
"""
Script para verificar el estado de la base de datos
"""
from app import create_app
from app.models import db, User

def check_database():
    """Verificar conexión y tablas de la base de datos"""
    app = create_app()

    with app.app_context():
        try:
            # Verificar conexión
            db.engine.execute('SELECT 1')
            print("✅ Conexión a la base de datos exitosa")

            # Verificar tablas
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📋 Tablas encontradas: {tables}")

            # Verificar tabla users
            if 'users' in tables:
                print("✅ Tabla 'users' existe")

                # Contar usuarios
                user_count = User.query.count()
                print(f"👥 Usuarios registrados: {user_count}")

                # Mostrar usuarios recientes
                if user_count > 0:
                    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
                    print("📝 Usuarios recientes:")
                    for user in recent_users:
                        print(f"  - {user.username} ({user.email}) - {user.created_at}")
            else:
                print("❌ Tabla 'users' no existe")

        except Exception as e:
            print(f"❌ Error en la base de datos: {e}")

if __name__ == "__main__":
    check_database()