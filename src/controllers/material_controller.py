from flask import jsonify, request
from sqlalchemy.orm import joinedload
from src.models.material import Material, db
from src.models.material_detail import MaterialDetail
import uuid

def get_materials():
    """Get all materials with their details and providers"""
    try:
        # Eagerly load the 'material_detail' and the nested 'provider'
        all_materials = Material.query.options(
            joinedload(Material.material_detail).joinedload(MaterialDetail.provider)
        ).all()
        
        materials_list = []
        for material in all_materials:
            material_data = {
                'materials_id': str(material.materials_id),
                'name': material.name,
                'type_id': material.type_id,
                'type_name': material.get_type_name(),
                'materials_details_id': str(material.materials_details_id) if material.materials_details_id else None,
                'material_detail': None
            }
            
            if material.material_detail:
                material_detail_data = {
                    'materials_details_id': str(material.material_detail.materials_details_id),
                    'description': material.material_detail.description,
                    'quantity': material.material_detail.quantity,
                    'price': float(material.material_detail.price) if material.material_detail.price else None,
                    'provider': None
                }
                
                if material.material_detail.provider:
                    material_detail_data['provider'] = {
                        'provider_id': str(material.material_detail.provider.provider_id),
                        'name': material.material_detail.provider.name,
                        'direction': material.material_detail.provider.direction,
                        'phone': material.material_detail.provider.phone
                    }
                
                material_data['material_detail'] = material_detail_data
            
            materials_list.append(material_data)
            
        return jsonify(materials_list)
    except Exception as e:
        print(f"Error in get_materials: {e}")
        return jsonify({"error": str(e)}), 500

def get_material_by_id(materials_id):
    """Get a material by ID with details"""
    try:
        # Eagerly load details
        material = Material.query.options(
            joinedload(Material.material_detail).joinedload(MaterialDetail.provider)
        ).get(materials_id)

        if not material:
            return jsonify({"message": "Material not found"}), 404

        material_data = {
            'materials_id': str(material.materials_id),
            'name': material.name,
            'type_id': material.type_id,
            'type_name': material.get_type_name(),
            'materials_details_id': str(material.materials_details_id) if material.materials_details_id else None,
            'material_detail': None
        }
        
        if material.material_detail:
            material_detail_data = {
                'materials_details_id': str(material.material_detail.materials_details_id),
                'description': material.material_detail.description,
                'quantity': material.material_detail.quantity,
                'price': float(material.material_detail.price) if material.material_detail.price else None,
                'provider': None
            }
            
            if material.material_detail.provider:
                material_detail_data['provider'] = {
                    'provider_id': str(material.material_detail.provider.provider_id),
                    'name': material.material_detail.provider.name,
                    'direction': material.material_detail.provider.direction,
                    'phone': material.material_detail.provider.phone
                }
            
            material_data['material_detail'] = material_detail_data

        return jsonify(material_data)
        
    except Exception as e:
        print(f"Error in get_material_by_id: {e}")
        return jsonify({"error": str(e)}), 500

def get_materials_by_type(type_id):
    """Get materials by type ID with details"""
    try:
        materials = Material.query.options(
            joinedload(Material.material_detail).joinedload(MaterialDetail.provider)
        ).filter_by(type_id=type_id).all()
        
        materials_list = []
        for material in materials:
            material_data = {
                'materials_id': str(material.materials_id),
                'name': material.name,
                'type_id': material.type_id,
                'type_name': material.get_type_name(),
                'materials_details_id': str(material.materials_details_id) if material.materials_details_id else None,
                'material_detail': None
            }
            
            if material.material_detail:
                material_detail_data = {
                    'materials_details_id': str(material.material_detail.materials_details_id),
                    'description': material.material_detail.description,
                    'quantity': material.material_detail.quantity,
                    'price': float(material.material_detail.price) if material.material_detail.price else None,
                    'provider': None
                }
                
                if material.material_detail.provider:
                    material_detail_data['provider'] = {
                        'provider_id': str(material.material_detail.provider.provider_id),
                        'name': material.material_detail.provider.name,
                        'direction': material.material_detail.provider.direction,
                        'phone': material.material_detail.provider.phone
                    }
                
                material_data['material_detail'] = material_detail_data
            
            materials_list.append(material_data)
        
        return jsonify(materials_list)

    except Exception as e:
        print(f"Error in get_materials_by_type: {e}")
        return jsonify({"error": str(e)}), 500

# ==================== Material POST Controller ====================

def create_material():
    """Create a new material"""
    try:
        data = request.get_json()
        
        if not data or 'name' not in data:
            return jsonify({"error": "Name is required"}), 400
                
        new_material = Material(
            materials_id=uuid.uuid4(),
            name=data['name'],
            type_id=data.get('type_id'),
            materials_details_id=data.get('materials_details_id')
        )
        
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
