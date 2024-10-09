from app import app
from models import db, Product, User
from datetime import time

with app.app_context():
    db.create_all()

    # Crear producto de ejemplo si no existe
    if not Product.query.get(1):
        product = Product(
            id=1,
            nombre='Producto 1',
            dias_menor_igual_operativa_no_reinversion=2,
            dias_mayor_operativa_no_reinversion=3,
            dias_menor_igual_operativa_reinversion=1,
            dias_mayor_operativa_reinversion=2,
            hora_operativa=time(10, 30)  # 10:30 AM
        )
        db.session.add(product)
        db.session.commit()
        print("Producto de ejemplo creado.")
    else:
        print("El producto ya existe.")

            # Crear un usuario por defecto si no existe
    if not User.query.filter_by(email='admin@example.com').first():
        user = User(
            nombre='admin',
            email='admin@example.com'
        )
        user.set_password('password123')  # Establecer la contraseña hash
        db.session.add(user)
        db.session.commit()
        print("Usuario de ejemplo creado.")
    else:
        print("El usuario ya existe.")

