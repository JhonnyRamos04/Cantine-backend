from flask import jsonify, request
from src.models.material import Material, db
import uuid

def get_materials():
    """Get all materials"""
    try:
        all_materials = Material.query.all()
        materials_list = [m.to_dict() for m in all_materials]
        return jsonify(materials_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_material_by_id(materials_id):
    """Get a material by ID"""
    try:
        material = Material.query.get(materials_id)
        if material:
            return jsonify(material.to_dict())
        return jsonify({"message": "Material not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_materials_by_type(type_id):
    """Get materials by type ID"""
    try:
        materials = Material.query.filter_by(type_id=type_id).all()
        materials_list = [m.to_dict() for m in materials]
        return jsonify(materials_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== Material POST Controller ====================

def create_material():
    """Create a new material"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'name' not in data:
            return jsonify({"error": "Name is required"}), 400
                
        # Create new material
        new_material = Material(
            materials_id=uuid.uuid4(),
            name=data['name'],
            type_id=data.get('type_id'),
            materials_details_id=data.get('materials_details_id')
        )
        
        # Add to database
        db.session.add(new_material)
        db.session.commit()
        
        return jsonify({
            "message": "Material created successfully",
            "material": new_material.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ==================== Material PUT Controller ====================

def update_material(materials_id):
    """Update an existing material"""
    try:
        material = Material.query.get(materials_id)
        if not material:
            return jsonify({"error": "Material not found"}), 404
            
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        # Update fields if provided
        if 'name' in data:
            material.name = data['name']
        if 'type_id' in data:
            material.type_id = data['type_id']
        if 'materials_details_id' in data:
            material.materials_details_id = data['materials_details_id']
            
        db.session.commit()
        
        return jsonify({
            "message": "Material updated successfully",
            "material": material.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ==================== Material DELETE Controller ====================

def delete_material(materials_id):
    """Delete a material"""
    try:
        material = Material.query.get(materials_id)
        if not material:
            return jsonify({"error": "Material not found"}), 404
            
        db.session.delete(material)
        db.session.commit()
        
        return jsonify({
            "message": "Material deleted successfully"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
