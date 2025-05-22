from flask import Blueprint
from src.controllers.dishes_detail_controller import delete_dish_detail, get_dish_details, get_dish_detail_by_id, create_dish_detail, update_dish_detail

dish_detail_bp = Blueprint('dish_detail', __name__)

@dish_detail_bp.route('/', methods=['GET'])
def all_dish_details():
    return get_dish_details()

@dish_detail_bp.route('/<uuid:dishes_details_id>', methods=['GET'])
def dish_detail_by_id(dishes_details_id):
    return get_dish_detail_by_id(dishes_details_id)

@dish_detail_bp.route('/', methods=['POST'])
def add_dish_detail():
    return create_dish_detail()

@dish_detail_bp.route('/<uuid:dishes_details_id>', methods=['PUT'])
def modify_dish_detail(dishes_details_id):
    return update_dish_detail(dishes_details_id)

@dish_detail_bp.route('/<uuid:dishes_details_id>', methods=['DELETE'])
def remove_dish_detail(dishes_details_id):
    return delete_dish_detail(dishes_details_id)
