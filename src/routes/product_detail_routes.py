from flask import Blueprint
from src.controllers.product_detail_controller import delete_product_detail, get_product_details, get_product_detail_by_id, get_product_details_by_provider, create_product_detail, update_product_detail

product_detail_bp = Blueprint('product_detail', __name__)

@product_detail_bp.route('/', methods=['GET'])
def all_product_details():
    return get_product_details()

@product_detail_bp.route('/<uuid:products_details_id>', methods=['GET'])
def product_detail_by_id(products_details_id):
    return get_product_detail_by_id(products_details_id)

@product_detail_bp.route('/provider/<uuid:provided_id>', methods=['GET'])
def product_details_by_provider(provided_id):
    return get_product_details_by_provider(provided_id)

@product_detail_bp.route('/', methods=['POST'])
def add_product_detail():
    return create_product_detail()

@product_detail_bp.route('/<uuid:products_details_id>', methods=['PUT'])
def modify_product_detail(products_details_id):
    return update_product_detail(products_details_id)

@product_detail_bp.route('/<uuid:products_details_id>', methods=['DELETE'])
def remove_product_detail(products_details_id):
    return delete_product_detail(products_details_id)
