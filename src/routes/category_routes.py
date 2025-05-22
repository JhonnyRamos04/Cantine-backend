from flask import Blueprint
from src.controllers.category_controller import delete_category, get_categories, get_category_by_id, create_category, update_category

category_bp = Blueprint('category', __name__)

@category_bp.route('/', methods=['GET'])
def all_categories():
    return get_categories()

@category_bp.route('/<uuid:category_id>', methods=['GET'])
def category_by_id(category_id):
    return get_category_by_id(category_id)

@category_bp.route('/', methods=['POST'])
def add_category():
    return create_category()

@category_bp.route('/<uuid:category_id>', methods=['PUT'])
def modify_category(category_id):
    return update_category(category_id)

@category_bp.route('/<uuid:category_id>', methods=['DELETE'])
def remove_category(category_id):
    return delete_category(category_id)
