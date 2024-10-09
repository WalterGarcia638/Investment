"""
from flask import Flask, jsonify
from flask_cors import CORS
from login_controller import login_controller

app = Flask(__name__)

app.register_blueprint(login_controller, url_prefix='/api')

@app.route('/api', methods=['GET'])
def get_api():
    return jsonify({"message": "Hello, World!"})

if __name__ == '__main__':
    app.run(debug=True)
    """
"""# app.py
from flask import Flask, jsonify
from flask_cors import CORS
from login_controller import login_controller
from investment_controller import investment_controller
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:wg920129@localhost/investment' # Actualiza con tus credenciales
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
CORS(app)

app.register_blueprint(login_controller, url_prefix='/api')
app.register_blueprint(investment_controller, url_prefix='/api')


@app.route('/api', methods=['GET'])
def get_api():
    return jsonify({"message": "Hello, World!"})

if __name__ == '__main__':
    app.run(debug=True)"""

from flask import Flask, jsonify
from flask_cors import CORS
from login_controller import login_controller
from investment_controller import investment_controller
from user_controller import user_controller
from product_controller import product_controller
from models import db

# Configurar el logging para SQLAlchemy
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:wg920129@localhost/investment'  # Actualiza con tus credenciales
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
CORS(app)

app.register_blueprint(login_controller, url_prefix='/api')
app.register_blueprint(investment_controller, url_prefix='/api')
app.register_blueprint(user_controller, url_prefix='/api')
app.register_blueprint(product_controller, url_prefix='/api')


@app.route('/api', methods=['GET'])
def get_api():
    return jsonify({"message": "Hello, World!"})

if __name__ == '__main__':
    app.run(debug=True)
