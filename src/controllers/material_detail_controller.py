from flask import jsonify, request
from src.models.material_detail import MaterialDetail, db
import uuid

def get_material_details():
    """Get all material details"""
    try:
        # Usar opciones de carga para cargar relaciones
        all_details = MaterialDetail.query.options(
            db.joinedload(MaterialDetail.provider)
        ).all()
        details_list = [d.to_dict() for d in all_details]
        return jsonify(details_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_material_detail_by_id(materials_details_id):
    """Get a material detail by ID"""
    try:
        # Usar opciones de carga para cargar relaciones
        detail = MaterialDetail.query.options(
            db.joinedload(MaterialDetail.provider)
        ).get(materials_details_id)
        if detail:
            return jsonify(detail.to_dict())
        return jsonify({"message": "Material detail not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_material_details_by_provider(provided_id):
    """Get material details for a specific provider"""
    try:
        details = MaterialDetail.query.filter_by(provided_id=provided_id).all()
        details_list = [d.to_dict() for d in details]
        return jsonify(details_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== Material Detail POST Controller ====================
def create_material_detail():
    """Create a new material detail"""
    try:
        data = request.get_json()
        
        # Create new material detail
        new_detail = MaterialDetail(
            materials_details_id=uuid.uuid4(),
            description=data.get('description'),
            quantity=data.get('quantity'),
            price=data.get('price'),
            provided_id=data.get('provided_id')
        )
        
        # Add to database
        db.session.add(new_detail)
        db.session.commit()
        
        return jsonify({
            "message": "Material detail created successfully",
            "material_detail": new_detail.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ==================== Material Detail PUT Controller ====================

def update_material_detail(materials_details_id):
    """Update an existing material detail"""
    try:
        detail = MaterialDetail.query.get(materials_details_id)
        if not detail:
            return jsonify({"error": "Material detail not found"}), 404
            
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        # Update fields if provided
        if 'description' in data:
            detail.description = data['description']
        if 'quantity' in data:
            detail.quantity = data['quantity']
        if 'price' in data:
            detail.price = data['price']
        if 'provided_id' in data:
            detail.provided_id = data['provided_id']
            
        db.session.commit()
        
        return jsonify({
            "message": "Material detail updated successfully",
            "material_detail": detail.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ==================== Material Detail DELETE Controller ====================

def delete_material_detail(materials_details_id):
    """Delete a material detail"""
    try:
        detail = MaterialDetail.query.get(materials_details_id)
        if not detail:
            return jsonify({"error": "Material detail not found"}), 404
            
        # Check if material detail is being used
        if detail.materials:
            return jsonify({"error": "Cannot delete material detail that is in use"}), 400
            
        db.session.delete(detail)
        db.session.commit()
        
        return jsonify({
            "message": "Material detail deleted successfully"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
