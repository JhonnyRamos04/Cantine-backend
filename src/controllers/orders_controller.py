from flask import jsonify, request
from src.models.orders import Orders  # Importa el modelo Orders
from src.db.connection import db      # Asegúrate de importar tu instancia de la base de datos
import uuid

def get_orders():
    """Obtiene todas las órdenes"""
    try:
        all_orders = Orders.query.all()
        orders_list = [order.to_dict() for order in all_orders]
        return jsonify(orders_list)
    except Exception as e:
        # Para depuración, es útil imprimir el error
        print(e)
        return jsonify({"error": "Ocurrió un error al obtener las órdenes"}), 500

def get_order_by_id(order_id):
    """Obtiene una orden por su ID"""
    try:
        order = Orders.query.get(order_id)
        if order:
            return jsonify(order.to_dict())
        return jsonify({"message": "Orden no encontrada"}), 404
    except Exception as e:
        print(e)
        return jsonify({"error": "Ocurrió un error al obtener la orden"}), 500

def get_order_by_status(status_id):
    """Get dishes by status ID"""
    try:
        order = Orders.query.filter_by(status_id=status_id).all()
        order_list = [d.to_dict() for d in order]
        return jsonify(order_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== Controlador POST para Órdenes ====================
def create_order():
    """Crea una nueva orden"""
    try:
        data = request.get_json()
        
        # Validaciones básicas
        if not data or not 'user_id' in data or not 'dishes_id' in data:
            return jsonify({"error": "Faltan los campos 'user_id' y 'dishes_id'"}), 400

        # Crea una nueva orden
        new_order = Orders(
            order_id=uuid.uuid4(),
            user_id=data['user_id'],
            dishes_id=data['dishes_id'],
            status_id=data['status_id']
        )
        
        # Agrega a la base de datos
        db.session.add(new_order)
        db.session.commit()
        
        return jsonify({
            "message": "Orden creada exitosamente",
            "order": new_order.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"error": "Ocurrió un error al crear la orden"}), 500

# ==================== Controlador PUT para Órdenes ====================

def update_order(order_id):
    """Actualiza una orden existente"""
    try:
        order = Orders.query.get(order_id)
        if not order:
            return jsonify({"error": "Orden no encontrada"}), 404
            
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se proporcionaron datos para actualizar"}), 400
            
        # Actualiza los campos si se proporcionan
        if 'user_id' in data:
            order.user_id = data['user_id']
        if 'dishes_id' in data:
            order.dishes_id = data['dishes_id']
        if 'status_id' in data:
            order.status_id = data['status_id']
            
        db.session.commit()
        
        return jsonify({
            "message": "Orden actualizada exitosamente",
            "order": order.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"error": "Ocurrió un error al actualizar la orden"}), 500

# ==================== Controlador DELETE para Órdenes ====================

def delete_order(order_id):
    """Elimina una orden"""
    try:
        order = Orders.query.get(order_id)
        if not order:
            return jsonify({"error": "Orden no encontrada"}), 404
            
        db.session.delete(order)
        db.session.commit()
        
        return jsonify({
            "message": "Orden eliminada exitosamente"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"error": "Ocurrió un error al eliminar la orden"}), 500
