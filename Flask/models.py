# models.py
"""from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    dias_menor_igual_operativa_no_reinversion = db.Column(db.Integer)
    dias_mayor_operativa_no_reinversion = db.Column(db.Integer)
    dias_menor_igual_operativa_reinversion = db.Column(db.Integer)
    dias_mayor_operativa_reinversion = db.Column(db.Integer)
    hora_operativa = db.Column(db.Time)"""


"""
# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    dias_menor_igual_operativa_no_reinversion = db.Column(db.Integer)
    dias_mayor_operativa_no_reinversion = db.Column(db.Integer)
    dias_menor_igual_operativa_reinversion = db.Column(db.Integer)
    dias_mayor_operativa_reinversion = db.Column(db.Integer)
    hora_operativa = db.Column(db.Time)

class Investment(db.Model):
    __tablename__ = 'investment'
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    en_reinversion = db.Column(db.Boolean, nullable=False)
    plazo = db.Column(db.Integer, nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=False)
    plazo_real = db.Column(db.Integer, nullable=False)

    producto = db.relationship('Product', backref=db.backref('investments', lazy=True))"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    dias_menor_igual_operativa_no_reinversion = db.Column(db.Integer)
    dias_mayor_operativa_no_reinversion = db.Column(db.Integer)
    dias_menor_igual_operativa_reinversion = db.Column(db.Integer)
    dias_mayor_operativa_reinversion = db.Column(db.Integer)
    hora_operativa = db.Column(db.Time)

class Investment(db.Model):
    __tablename__ = 'investment'
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    en_reinversion = db.Column(db.Boolean, nullable=False)
    plazo = db.Column(db.Integer, nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=False)
    plazo_real = db.Column(db.Integer, nullable=False)

    producto = db.relationship('Product', backref=db.backref('investments', lazy=True))

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Almacena el hash de la contraseña

    # Método para establecer una contraseña hash
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # Método para verificar una contraseña
    def check_password(self, password):
        return check_password_hash(self.password, password)