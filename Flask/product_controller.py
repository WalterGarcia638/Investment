from flask import Blueprint, request, jsonify
from models import db, Product
from datetime import time

product_controller = Blueprint('product_controller', __name__)

# Crear producto
@product_controller.route('/product', methods=['POST'])
def create_product():
    data = request.get_json()

    nombre = data.get('nombre')
    dias_menor_igual_operativa_no_reinversion = data.get('dias_menor_igual_operativa_no_reinversion')
    dias_mayor_operativa_no_reinversion = data.get('dias_mayor_operativa_no_reinversion')
    dias_menor_igual_operativa_reinversion = data.get('dias_menor_igual_operativa_reinversion')
    dias_mayor_operativa_reinversion = data.get('dias_mayor_operativa_reinversion')
    hora_operativa_str = data.get('hora_operativa')

    if not nombre or not hora_operativa_str:
        return jsonify({'message': 'Datos incompletos'}), 400

    # Convertir hora_operativa a time
    hora_operativa = time.fromisoformat(hora_operativa_str)

    nuevo_producto = Product(
        nombre=nombre,
        dias_menor_igual_operativa_no_reinversion=dias_menor_igual_operativa_no_reinversion,
        dias_mayor_operativa_no_reinversion=dias_mayor_operativa_no_reinversion,
        dias_menor_igual_operativa_reinversion=dias_menor_igual_operativa_reinversion,
        dias_mayor_operativa_reinversion=dias_mayor_operativa_reinversion,
        hora_operativa=hora_operativa
    )
    db.session.add(nuevo_producto)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error al guardar producto', 'error': str(e)}), 500

    return jsonify({'message': 'Producto creado exitosamente'}), 201

# Obtener todos los productos
@product_controller.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    products_list = [{"id": product.id, "nombre": product.nombre, "dias_menor_igual_operativa_no_reinversion": product.dias_menor_igual_operativa_no_reinversion, "dias_mayor_operativa_no_reinversion": product.dias_mayor_operativa_no_reinversion, "dias_menor_igual_operativa_reinversion": product.dias_menor_igual_operativa_reinversion, "dias_mayor_operativa_reinversion": product.dias_mayor_operativa_reinversion, "hora_operativa": product.hora_operativa.isoformat()} for product in products]
    return jsonify(products_list), 200

# Actualizar producto
@product_controller.route('/product/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    product = Product.query.get(id)

    if not product:
        return jsonify({'message': 'Producto no encontrado'}), 404

    product.nombre = data.get('nombre', product.nombre)
    product.dias_menor_igual_operativa_no_reinversion = data.get('dias_menor_igual_operativa_no_reinversion', product.dias_menor_igual_operativa_no_reinversion)
    product.dias_mayor_operativa_no_reinversion = data.get('dias_mayor_operativa_no_reinversion', product.dias_mayor_operativa_no_reinversion)
    product.dias_menor_igual_operativa_reinversion = data.get('dias_menor_igual_operativa_reinversion', product.dias_menor_igual_operativa_reinversion)
    product.dias_mayor_operativa_reinversion = data.get('dias_mayor_operativa_reinversion', product.dias_mayor_operativa_reinversion)
    hora_operativa_str = data.get('hora_operativa')

    if hora_operativa_str:
        product.hora_operativa = time.fromisoformat(hora_operativa_str)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error al actualizar producto', 'error': str(e)}), 500

    return jsonify({'message': 'Producto actualizado exitosamente'}), 200

# Eliminar producto
@product_controller.route('/product/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)

    if not product:
        return jsonify({'message': 'Producto no encontrado'}), 404

    db.session.delete(product)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error al eliminar producto', 'error': str(e)}), 500

    return jsonify({'message': 'Producto eliminado exitosamente'}), 200
