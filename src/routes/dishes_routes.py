from flask import Blueprint
from src.controllers.dishes_controller import delete_dish, get_dishes, get_dish_by_id, get_dishes_by_category, get_dishes_by_status, create_dish, update_dish

dish_bp = Blueprint('dish', __name__)

@dish_bp.route('/', methods=['GET'])
def all_dishes():
    return get_dishes()

@dish_bp.route('/<uuid:dishes_id>', methods=['GET'])
def dish_by_id(dishes_id):
    return get_dish_by_id(dishes_id)

@dish_bp.route('/category/<uuid:category_id>', methods=['GET'])
def dishes_by_category(category_id):
    return get_dishes_by_category(category_id)

@dish_bp.route('/status/<uuid:status_id>', methods=['GET'])
def dishes_by_status(status_id):
    return get_dishes_by_status(status_id)

@dish_bp.route('/', methods=['POST'])
def add_dish():
    return create_dish()

@dish_bp.route('/<uuid:dishes_id>', methods=['PUT'])
def modify_dish(dishes_id):
    return update_dish(dishes_id)

@dish_bp.route('/<uuid:dishes_id>', methods=['DELETE'])
def remove_dish(dishes_id):
    return delete_dish(dishes_id)
