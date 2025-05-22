from flask import Blueprint
from src.controllers.role_controller import delete_role, get_roles, get_role_by_id, create_role, update_role

role_bp = Blueprint('role', __name__)

@role_bp.route('/', methods=['GET'])
def all_roles():
    return get_roles()

@role_bp.route('/<uuid:roles_id>', methods=['GET'])
def role_by_id(roles_id):
    return get_role_by_id(roles_id)

@role_bp.route('/', methods=['POST'])
def add_role():
    return create_role()

@role_bp.route('/<uuid:roles_id>', methods=['PUT'])
def modify_role(roles_id):
    return update_role(roles_id)

@role_bp.route('/<uuid:roles_id>', methods=['DELETE'])
def remove_role(roles_id):
    return delete_role(roles_id)
