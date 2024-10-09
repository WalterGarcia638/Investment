from flask import Blueprint, request, jsonify
from flask_cors import CORS
from models import User
import jwt
import datetime

login_controller = Blueprint('login_controller', __name__)

# Aplicar CORS al blueprint
CORS(login_controller)

@login_controller.route('/login', methods=['POST'])
def login():
    auth = request.json
    if not auth or not auth.get('username') or not auth.get('password'):
        return jsonify({'message': 'Datos incompletos'}), 400

    # Buscar usuario por nombre
    user = User.query.filter_by(nombre=auth['username']).first()

    if user and user.check_password(auth['password']):
        # Generar token JWT si las credenciales son correctas
        token = jwt.encode({
            'sub': user.nombre,
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, 'your_secret_key', algorithm="HS256")

        return jsonify({'token': token})

    return jsonify({'message': 'Credenciales inválidas'}), 401

