from flask import Blueprint, request, jsonify
from flask_cors import CORS
from models import db, User

user_controller = Blueprint('user_controller', __name__)

# Aplicar CORS al blueprint
CORS(user_controller)

# Crear usuario
@user_controller.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()

    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')

    if not nombre or not email or not password:
        return jsonify({'message': 'Datos incompletos'}), 400

    nuevo_usuario = User(nombre=nombre, email=email)
    nuevo_usuario.set_password(password)
    db.session.add(nuevo_usuario)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error al guardar usuario', 'error': str(e)}), 500

    return jsonify({'message': 'Usuario creado exitosamente'}), 201

# Editar usuario
@user_controller.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    usuario = User.query.get(id)

    if not usuario:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    usuario.nombre = data.get('nombre', usuario.nombre)
    usuario.email = data.get('email', usuario.email)

    # Actualizar la contraseña si se proporciona
    if 'password' in data and data['password']:
        usuario.set_password(data['password'])

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error al actualizar usuario', 'error': str(e)}), 500

    return jsonify({'message': 'Usuario actualizado exitosamente'}), 200

# Eliminar usuario
@user_controller.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    usuario = User.query.get(id)

    if not usuario:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    db.session.delete(usuario)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error al eliminar usuario', 'error': str(e)}), 500

    return jsonify({'message': 'Usuario eliminado exitosamente'}), 200

# Obtener lista de usuarios
@user_controller.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [{"id": user.id, "nombre": user.nombre, "email": user.email} for user in users]
    return jsonify(users_list), 200

