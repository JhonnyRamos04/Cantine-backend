from flask import jsonify, request
# Importamos nuestro jwt_required personalizado en lugar del de flask_jwt_extended
from src.middlewares.auth import jwt_required
from src.models.user import User, db
import uuid

def get_users():
    """Get all users"""
    try:
        # Usar opciones de carga para cargar relaciones
        all_users = User.query.options(
            db.joinedload(User.role)
        ).all()
        users_list = [u.to_dict() for u in all_users]
        return jsonify(users_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_user_by_id(user_id):
    """Get a user by ID"""
    try:
        # Usar opciones de carga para cargar relaciones
        user = User.query.options(
            db.joinedload(User.role)
        ).get(user_id)
        if user:
            return jsonify(user.to_dict())
        return jsonify({"message": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_users_by_role(roles_id):
    """Get users by role ID"""
    try:
        users = User.query.filter_by(roles_id=roles_id).all()
        users_list = [u.to_dict() for u in users]
        return jsonify(users_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# ==================== User POST Controller ====================
@jwt_required()  # Este decorador ahora permite acceso a todos
def create_user():
    """Create a new user"""
    try:
        # Desactivamos la verificación de permisos
        # current_user_id = get_jwt_identity()
        # current_user = User.query.get(current_user_id)
        # 
        # if not current_user or current_user.roles_id != 1:
        #     return jsonify({"error": "No tienes permisos para crear usuarios"}), 403
        
        data = request.get_json()
        
        # Validar required fields
        required_fields = ['name', 'email', 'password', 'roles_id']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400
                
        # Check if email already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({"error": "Email already exists"}), 409
            
        # Create new user
        new_user = User(
            user_id=uuid.uuid4(),
            name=data['name'],
            email=data['email'],
            roles_id=data['roles_id']
        )
        
        # Set hashed password
        new_user.set_password(data['password'])
        
        # Add to database
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            "message": "User created successfully",
            "user": new_user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@jwt_required()  # Este decorador ahora permite acceso a todos
def update_user(user_id):
    """Update an existing user"""
    try:
        # Desactivamos la verificación de permisos
        # current_user_id = get_jwt_identity()
        # current_user = User.query.get(current_user_id)
        # 
        # if not current_user or (current_user.roles_id != 1 and str(current_user.user_id) != user_id):
        #     return jsonify({"error": "No tienes permisos para actualizar este usuario"}), 403
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        data = request.get_json()
        
        # Update fields if provided
        if 'name' in data:
            user.name = data['name']
            
        if 'email' in data and data['email'] != user.email:
            # Check if new email already exists
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user:
                return jsonify({"error": "Email already exists"}), 409
            user.email = data['email']
            
        if 'password' in data:
            user.set_password(data['password'])
            
        # Permitimos cambiar el rol sin verificar permisos
        if 'roles_id' in data:
            user.roles_id = data['roles_id']
            
        db.session.commit()
        
        return jsonify({
            "message": "User updated successfully",
            "user": user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@jwt_required()  # Este decorador ahora permite acceso a todos
def delete_user(user_id):
    """Delete a user"""
    try:
        # Desactivamos la verificación de permisos
        # current_user_id = get_jwt_identity()
        # current_user = User.query.get(current_user_id)
        # 
        # if not current_user or current_user.roles_id != 1:
        #     return jsonify({"error": "No tienes permisos para eliminar usuarios"}), 403
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({
            "message": "User deleted successfully"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
