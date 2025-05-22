from flask import jsonify, request
from src.models.dishes_details import DishDetail, db
import uuid

def get_dish_details():
    """Get all dish details"""
    try:
        all_details = DishDetail.query.all()
        details_list = [d.to_dict() for d in all_details]
        return jsonify(details_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_dish_detail_by_id(dishes_details_id):
    """Get a dish detail by ID"""
    try:
        detail = DishDetail.query.get(dishes_details_id)
        if detail:
            return jsonify(detail.to_dict())
        return jsonify({"message": "Dish detail not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== Dish Detail POST Controller ====================
def create_dish_detail():
    """Create a new dish detail"""
    try:
        data = request.get_json()
        
        # Create new dish detail
        new_detail = DishDetail(
            dishes_details_id=uuid.uuid4(),
            description=data.get('description'),
            price=data.get('price')
        )
        
        # Add to database
        db.session.add(new_detail)
        db.session.commit()
        
        return jsonify({
            "message": "Dish detail created successfully",
            "dish_detail": new_detail.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ==================== Dish Detail PUT Controller ====================

def update_dish_detail(dishes_details_id):
    """Update an existing dish detail"""
    try:
        detail = DishDetail.query.get(dishes_details_id)
        if not detail:
            return jsonify({"error": "Dish detail not found"}), 404
            
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        # Update fields if provided
        if 'description' in data:
            detail.description = data['description']
        if 'price' in data:
            detail.price = data['price']
            
        db.session.commit()
        
        return jsonify({
            "message": "Dish detail updated successfully",
            "dish_detail": detail.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ==================== Dish Detail DELETE Controller ====================

def delete_dish_detail(dishes_details_id):
    """Delete a dish detail"""
    try:
        detail = DishDetail.query.get(dishes_details_id)
        if not detail:
            return jsonify({"error": "Dish detail not found"}), 404
            
        # Check if dish detail is being used
        if detail.dishes:
            return jsonify({"error": "Cannot delete dish detail that is in use"}), 400
            
        db.session.delete(detail)
        db.session.commit()
        
        return jsonify({
            "message": "Dish detail deleted successfully"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
