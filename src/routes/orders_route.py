from flask import Blueprint
# Importar las funciones del controlador de órdenes que creamos
from src.controllers.orders_controller import (
    delete_order, 
    get_orders, 
    get_order_by_id, 
    get_order_by_status,
    create_order, 
    update_order
)

# Renombrar el Blueprint para reflejar que ahora maneja órdenes
orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/', methods=['GET'])
def all_orders():
    """Ruta para obtener todas las órdenes."""
    return get_orders()

@orders_bp.route('/<uuid:order_id>', methods=['GET'])
def order_by_id(order_id):
    """Ruta para obtener una orden por su ID."""
    return get_order_by_id(order_id)

@orders_bp.route('/', methods=['POST'])
def add_order():
    """Ruta para crear una nueva orden."""
    return create_order()

@orders_bp.route('/<uuid:order_id>', methods=['PUT'])
def modify_order(order_id):
    """Ruta para actualizar una orden existente."""
    return update_order(order_id)

@orders_bp.route('/status/<uuid:status_id>', methods=['GET'])
def dishes_by_status(status_id):
    return get_order_by_status(status_id)

@orders_bp.route('/<uuid:order_id>', methods=['DELETE'])
def remove_order(order_id):
    """Ruta para eliminar una orden."""
    return delete_order(order_id)
