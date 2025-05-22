from flask import Blueprint
from src.controllers.product_controller import delete_product, get_products, get_product_by_id, get_products_by_category, create_product, update_product

product_bp = Blueprint('product', __name__)

@product_bp.route('/', methods=['GET'])
def all_products():
    return get_products()

@product_bp.route('/<uuid:products_id>', methods=['GET'])
def product_by_id(products_id):
    return get_product_by_id(products_id)

@product_bp.route('/category/<uuid:category_id>', methods=['GET'])
def products_by_category(category_id):
    return get_products_by_category(category_id)

@product_bp.route('/', methods=['POST'])
def add_product():
    return create_product()

@product_bp.route('/<uuid:products_id>', methods=['PUT'])
def modify_product(products_id):
    return update_product(products_id)

@product_bp.route('/<uuid:products_id>', methods=['DELETE'])
def remove_product(products_id):
    return delete_product(products_id)
