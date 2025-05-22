from flask import jsonify, request
from src.models.role import Role, db
import uuid

def get_roles():
    """Get all roles"""
    try:
        all_roles = Role.query.all()
        roles_list = [r.to_dict() for r in all_roles]
        return jsonify(roles_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_role_by_id(roles_id):
    """Get a role by ID"""
    try:
        role = Role.query.get(roles_id)
        if role:
            return jsonify(role.to_dict())
        return jsonify({"message": "Role not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== Role POST Controller ====================
def create_role():
    """Create a new role"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'name' not in data:
            return jsonify({"error": "Name is required"}), 400
            
        # Create new role
        new_role = Role(
            roles_id=uuid.uuid4(),
            name=data['name'],
            description=data.get('description')
        )
        
        # Add to database
        db.session.add(new_role)
        db.session.commit()
        
        return jsonify({
            "message": "Role created successfully",
            "role": new_role.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ==================== Role PUT Controller ====================

def update_role(roles_id):
    """Update an existing role"""
    try:
        role = Role.query.get(roles_id)
        if not role:
            return jsonify({"error": "Role not found"}), 404
            
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        # Update fields if provided
        if 'name' in data:
            role.name = data['name']
        if 'description' in data:
            role.description = data['description']
            
        db.session.commit()
        
        return jsonify({
            "message": "Role updated successfully",
            "role": role.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
# ==================== Role DELETE Controller ====================

def delete_role(roles_id):
    """Delete a role"""
    try:
        role = Role.query.get(roles_id)
        if not role:
            return jsonify({"error": "Role not found"}), 404
            
        # Check if role is being used
        if role.users:
            return jsonify({"error": "Cannot delete role that is assigned to users"}), 400
            
        db.session.delete(role)
        db.session.commit()
        
        return jsonify({
            "message": "Role deleted successfully"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
