from flask import jsonify, request
from src.models.dishes import Dish, db
import uuid

def get_dishes():
    """Get all dishes"""
    try:
        # Usar opciones de carga para cargar relaciones
        all_dishes = Dish.query.options(
            db.joinedload(Dish.status),
            db.joinedload(Dish.category),
            db.joinedload(Dish.product)
        ).all()
        dishes_list = [d.to_dict() for d in all_dishes]
        return jsonify(dishes_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_dish_by_id(dishes_id):
    """Get a dish by ID"""
    try:
        # Usar opciones de carga para cargar relaciones
        dish = Dish.query.options(
            db.joinedload(Dish.status),
            db.joinedload(Dish.category),
            db.joinedload(Dish.product)
        ).get(dishes_id)
        if dish:
            return jsonify(dish.to_dict())
        return jsonify({"message": "Dish not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_dishes_by_category(category_id):
    """Get dishes by category ID"""
    try:
        dishes = Dish.query.filter_by(category_id=category_id).all()
        dishes_list = [d.to_dict() for d in dishes]
        return jsonify(dishes_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_dishes_by_status(status_id):
    """Get dishes by status ID"""
    try:
        dishes = Dish.query.filter_by(status_id=status_id).all()
        dishes_list = [d.to_dict() for d in dishes]
        return jsonify(dishes_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== Dish POST Controller ====================

def create_dish():
    """Create a new dish"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'name' not in data:
            return jsonify({"error": "Name is required"}), 400
                
        # Create new dish
        new_dish = Dish(
            dishes_id=uuid.uuid4(),
            name=data['name'],
            status_id=data.get('status_id'),
            category_id=data.get('category_id'),
            products_id=data.get('products_id')
        )
        
        # Add to database
        db.session.add(new_dish)
        db.session.commit()
        
        return jsonify({
            "message": "Dish created successfully",
            "dish": new_dish.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ==================== Dish PUT Controller ====================

def update_dish(dishes_id):
    """Update an existing dish"""
    try:
        dish = Dish.query.get(dishes_id)
        if not dish:
            return jsonify({"error": "Dish not found"}), 404
            
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        # Update fields if provided
        if 'name' in data:
            dish.name = data['name']
        if 'status_id' in data:
            dish.status_id = data['status_id']
        if 'category_id' in data:
            dish.category_id = data['category_id']
        if 'products_id' in data:
            dish.products_id = data['products_id']
            
        db.session.commit()
        
        return jsonify({
            "message": "Dish updated successfully",
            "dish": dish.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ==================== Dish DELETE Controller ====================

def delete_dish(dishes_id):
    """Delete a dish"""
    try:
        dish = Dish.query.get(dishes_id)
        if not dish:
            return jsonify({"error": "Dish not found"}), 404
            
        db.session.delete(dish)
        db.session.commit()
        
        return jsonify({
            "message": "Dish deleted successfully"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
