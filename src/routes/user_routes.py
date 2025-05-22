from flask import Blueprint
from src.controllers.user_controller import delete_user, get_users, get_user_by_id, get_users_by_role, create_user, update_user

user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['GET'])
def all_users():
    return get_users()

@user_bp.route('/<uuid:user_id>', methods=['GET'])
def user_by_id(user_id):
    return get_user_by_id(user_id)

@user_bp.route('/role/<uuid:roles_id>', methods=['GET'])
def users_by_role(roles_id):
    return get_users_by_role(roles_id)

@user_bp.route('/', methods=['POST'])
def add_user():
    return create_user()

@user_bp.route('/<uuid:user_id>', methods=['PUT'])
def modify_user(user_id):
    return update_user(user_id)

@user_bp.route('/<uuid:user_id>', methods=['DELETE'])
def remove_user(user_id):
    return delete_user(user_id)
