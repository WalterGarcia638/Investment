"""# investment_controller.py
from flask import Blueprint, request, jsonify
from models import db, Product
from datetime import datetime, timedelta, time
from dateutil.parser import parse
import holidays

investment_controller = Blueprint('investment_controller', __name__)

@investment_controller.route('/calculate_dates', methods=['POST'])
def calculate_dates():
    data = request.get_json()
    producto_id = data.get('producto')
    en_reinversion = data.get('enReinversion')
    plazo = data.get('plazo')
    fecha_creacion_str = data.get('fechaCreacion')

    # Validar datos de entrada
    if not all([producto_id, en_reinversion is not None, plazo is not None, fecha_creacion_str]):
        return jsonify({'message': 'Datos de entrada incompletos'}), 400

    # Convertir fechaCreacion a datetime usando parse
    try:
        fecha_creacion = parse(fecha_creacion_str)
    except ValueError:
        return jsonify({'message': 'Formato de fecha inválido'}), 400

    # Obtener producto de la base de datos
    product = Product.query.get(producto_id)
    if not product:
        return jsonify({'message': 'Producto no encontrado'}), 404

    # Hora operativa
    hora_operativa = product.hora_operativa

    # Determinar días a sumar
    if fecha_creacion.time() <= hora_operativa:
        if en_reinversion:
            dias_a_sumar = product.dias_menor_igual_operativa_reinversion
        else:
            dias_a_sumar = product.dias_menor_igual_operativa_no_reinversion
    else:
        if en_reinversion:
            dias_a_sumar = product.dias_mayor_operativa_reinversion
        else:
            dias_a_sumar = product.dias_mayor_operativa_no_reinversion

    # Sumar días a fecha_creacion
    fecha_inicio = add_business_days(fecha_creacion, dias_a_sumar)

    # Sumar plazo a fecha_inicio
    fecha_fin = add_business_days(fecha_inicio, plazo)

    # Calcular plazoReal
    plazo_real = (fecha_fin - fecha_inicio).days

    response = {
        'producto': producto_id,
        'plazo': plazo,
        'fechaInicio': fecha_inicio.strftime('%Y-%m-%d %H:%M:%S'),
        'fechaFin': fecha_fin.strftime('%Y-%m-%d %H:%M:%S'),
        'plazoReal': plazo_real
    }

    return jsonify(response)

def add_business_days(from_date, business_days):
    dr_holidays = holidays.DominicanRepublic(years=from_date.year)
    current_date = from_date
    days_added = 0
    while days_added < business_days:
        current_date += timedelta(days=1)
        if current_date.weekday() >= 5:  # Sábado o Domingo
            continue
        if current_date.date() in dr_holidays:
            continue
        days_added += 1
    return current_date"""

"""# investment_controller.py
from flask import Blueprint, request, jsonify
from models import db, Product, Investment
from datetime import datetime, timedelta, time
from dateutil.parser import parse
import holidays

investment_controller = Blueprint('investment_controller', __name__)

@investment_controller.route('/calculate_dates', methods=['POST'])
def calculate_dates():
    data = request.get_json()
    producto_id = data.get('producto')
    en_reinversion = data.get('enReinversion')
    plazo = data.get('plazo')
    fecha_creacion_str = data.get('fechaCreacion')

    # Validar datos de entrada
    if not all([producto_id, en_reinversion is not None, plazo is not None, fecha_creacion_str]):
        return jsonify({'message': 'Datos de entrada incompletos'}), 400

    # Convertir fechaCreacion a datetime usando parse
    try:
        fecha_creacion = parse(fecha_creacion_str)
    except ValueError:
        return jsonify({'message': 'Formato de fecha inválido'}), 400

    # Obtener producto de la base de datos
    product = Product.query.get(producto_id)
    if not product:
        return jsonify({'message': 'Producto no encontrado'}), 404

    # Hora operativa
    hora_operativa = product.hora_operativa

    # Determinar días a sumar
    if fecha_creacion.time() <= hora_operativa:
        if en_reinversion:
            dias_a_sumar = product.dias_menor_igual_operativa_reinversion
        else:
            dias_a_sumar = product.dias_menor_igual_operativa_no_reinversion
    else:
        if en_reinversion:
            dias_a_sumar = product.dias_mayor_operativa_reinversion
        else:
            dias_a_sumar = product.dias_mayor_operativa_no_reinversion

    # Sumar días a fecha_creacion
    fecha_inicio = add_business_days(fecha_creacion, dias_a_sumar)

    # Sumar plazo a fecha_inicio
    fecha_fin = add_business_days(fecha_inicio, plazo)

    # Calcular plazoReal
    plazo_real = (fecha_fin - fecha_inicio).days

    # Crear instancia de Investment y guardarla en la base de datos
    nueva_inversion = Investment(
        producto_id=producto_id,
        en_reinversion=en_reinversion,
        plazo=plazo,
        fecha_creacion=fecha_creacion,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        plazo_real=plazo_real
    )

    db.session.add(nueva_inversion)
    db.session.commit()

    response = {
        'id': nueva_inversion.id,
        'producto': producto_id,
        'plazo': plazo,
        'fechaInicio': fecha_inicio.strftime('%Y-%m-%d %H:%M:%S'),
        'fechaFin': fecha_fin.strftime('%Y-%m-%d %H:%M:%S'),
        'plazoReal': plazo_real
    }

    return jsonify(response), 201

def add_business_days(from_date, business_days):
    dr_holidays = holidays.DominicanRepublic(years=from_date.year)
    current_date = from_date
    days_added = 0
    while days_added < business_days:
        current_date += timedelta(days=1)
        if current_date.weekday() >= 5:  # Sábado o Domingo
            continue
        if current_date.date() in dr_holidays:
            continue
        days_added += 1
    return current_date"""

"""from flask import Blueprint, request, jsonify
from models import db, Product, Investment
from datetime import datetime, timedelta, time
from dateutil.parser import parse
import holidays

investment_controller = Blueprint('investment_controller', __name__)

@investment_controller.route('/calculate_dates', methods=['POST'])
def calculate_dates():
    data = request.get_json()

    # Convertir y validar los tipos de datos de entrada
    try:
        producto_id = int(data.get('producto'))
        plazo = int(data.get('plazo'))
    except (ValueError, TypeError):
        return jsonify({'message': 'El producto y el plazo deben ser números enteros'}), 400

    en_reinversion = data.get('enReinversion')
    if isinstance(en_reinversion, str):
        en_reinversion = en_reinversion.lower() == 'true'
    elif isinstance(en_reinversion, int):
        en_reinversion = bool(en_reinversion)
    elif not isinstance(en_reinversion, bool):
        return jsonify({'message': 'El valor de enReinversion debe ser booleano'}), 400

    fecha_creacion_str = data.get('fechaCreacion')

    # Validar datos de entrada
    if not all([producto_id, en_reinversion is not None, plazo is not None, fecha_creacion_str]):
        return jsonify({'message': 'Datos de entrada incompletos'}), 400

    # Convertir fechaCreacion a datetime usando parse
    try:
        fecha_creacion = parse(fecha_creacion_str)
    except ValueError:
        return jsonify({'message': 'Formato de fecha inválido'}), 400

    # Obtener producto de la base de datos
    product = Product.query.get(producto_id)
    if not product:
        return jsonify({'message': 'Producto no encontrado'}), 404

    # Hora operativa
    hora_operativa = product.hora_operativa

    # Determinar días a sumar
    if fecha_creacion.time() <= hora_operativa:
        if en_reinversion:
            dias_a_sumar = product.dias_menor_igual_operativa_reinversion
        else:
            dias_a_sumar = product.dias_menor_igual_operativa_no_reinversion
    else:
        if en_reinversion:
            dias_a_sumar = product.dias_mayor_operativa_reinversion
        else:
            dias_a_sumar = product.dias_mayor_operativa_no_reinversion

    # Sumar días a fecha_creacion
    fecha_inicio = add_business_days(fecha_creacion, dias_a_sumar)

    # Sumar plazo a fecha_inicio
    fecha_fin = add_business_days(fecha_inicio, plazo)

    # Calcular plazoReal
    plazo_real = (fecha_fin - fecha_inicio).days

    # Crear instancia de Investment y guardarla en la base de datos
    nueva_inversion = Investment(
        producto_id=producto_id,
        en_reinversion=en_reinversion,
        plazo=plazo,
        fecha_creacion=fecha_creacion,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        plazo_real=plazo_real
    )

    db.session.add(nueva_inversion)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error al guardar la inversión: {e}")
        return jsonify({'message': 'Error al guardar la inversión', 'error': str(e)}), 500

    response = {
        'id': nueva_inversion.id,
        'producto': producto_id,
        'plazo': plazo,
        'fechaInicio': fecha_inicio.strftime('%Y-%m-%d %H:%M:%S'),
        'fechaFin': fecha_fin.strftime('%Y-%m-%d %H:%M:%S'),
        'plazoReal': plazo_real
    }

    return jsonify(response), 201

def add_business_days(from_date, business_days):
    dr_holidays = holidays.DominicanRepublic(years=from_date.year)
    current_date = from_date
    days_added = 0
    while days_added < business_days:
        current_date += timedelta(days=1)
        if current_date.weekday() >= 5:  # Sábado o Domingo
            continue
        if current_date.date() in dr_holidays:
            continue
        days_added += 1
    return current_date"""

from flask import Blueprint, request, jsonify
from models import db, Product, Investment
from datetime import datetime, timedelta, time
from dateutil.parser import parse
import holidays

investment_controller = Blueprint('investment_controller', __name__)

@investment_controller.route('/calculate_dates', methods=['POST'])
def calculate_dates():
    data = request.get_json()

    # Convertir y validar los tipos de datos de entrada
    try:
        producto_id = int(data.get('producto'))
        plazo = int(data.get('plazo'))
    except (ValueError, TypeError):
        return jsonify({'message': 'El producto y el plazo deben ser números enteros'}), 400

    en_reinversion = data.get('enReinversion')
    if isinstance(en_reinversion, str):
        en_reinversion = en_reinversion.lower() == 'true'
    elif isinstance(en_reinversion, int):
        en_reinversion = bool(en_reinversion)
    elif not isinstance(en_reinversion, bool):
        return jsonify({'message': 'El valor de enReinversion debe ser booleano'}), 400

    fecha_creacion_str = data.get('fechaCreacion')

    # Validar datos de entrada
    if not all([producto_id, en_reinversion is not None, plazo is not None, fecha_creacion_str]):
        return jsonify({'message': 'Datos de entrada incompletos'}), 400

    # Convertir fechaCreacion a datetime usando parse
    try:
        fecha_creacion = parse(fecha_creacion_str)
    except ValueError:
        return jsonify({'message': 'Formato de fecha inválido'}), 400

    # Obtener producto de la base de datos
    product = Product.query.get(producto_id)
    if not product:
        return jsonify({'message': 'Producto no encontrado'}), 404

    # Hora operativa
    hora_operativa = product.hora_operativa

    # Determinar días a sumar
    if fecha_creacion.time() <= hora_operativa:
        if en_reinversion:
            dias_a_sumar = product.dias_menor_igual_operativa_reinversion
        else:
            dias_a_sumar = product.dias_menor_igual_operativa_no_reinversion
    else:
        if en_reinversion:
            dias_a_sumar = product.dias_mayor_operativa_reinversion
        else:
            dias_a_sumar = product.dias_mayor_operativa_no_reinversion

    # Sumar días a fecha_creacion
    fecha_inicio = add_business_days(fecha_creacion, dias_a_sumar)
    fecha_inicio = fecha_inicio.replace(hour=0, minute=0, second=0, microsecond=0)

    # Sumar plazo a fecha_inicio
    fecha_fin = fecha_inicio + timedelta(days=plazo)
    fecha_fin = adjust_to_next_business_day(fecha_fin)
    fecha_fin = fecha_fin.replace(hour=0, minute=0, second=0, microsecond=0)

    # Calcular plazoReal
    plazo_real = (fecha_fin - fecha_inicio).days

    # Crear instancia de Investment y guardarla en la base de datos
    nueva_inversion = Investment(
        producto_id=producto_id,
        en_reinversion=en_reinversion,
        plazo=plazo,
        fecha_creacion=fecha_creacion,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        plazo_real=plazo_real
    )

    db.session.add(nueva_inversion)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error al guardar la inversión: {e}")
        return jsonify({'message': 'Error al guardar la inversión', 'error': str(e)}), 500

    response = {
        'id': nueva_inversion.id,
        'producto': producto_id,
        'plazo': plazo,
        'fechaInicio': fecha_inicio.strftime('%Y-%m-%d %H:%M:%S'),
        'fechaFin': fecha_fin.strftime('%Y-%m-%d %H:%M:%S'),
        'plazoReal': plazo_real
    }

    return jsonify(response), 201

def add_business_days(from_date, business_days):
    dr_holidays = holidays.DominicanRepublic(years=from_date.year)
    current_date = from_date
    days_added = 0
    while days_added < business_days:
        current_date += timedelta(days=1)
        if current_date.weekday() >= 5:  # Sábado o Domingo
            continue
        if current_date.date() in dr_holidays:
            continue
        days_added += 1
    return current_date

def adjust_to_next_business_day(date):
    dr_holidays = holidays.DominicanRepublic(years=date.year)
    while date.weekday() >= 5 or date.date() in dr_holidays:
        date += timedelta(days=1)
    return date




