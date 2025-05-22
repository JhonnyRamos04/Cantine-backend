from flask import Blueprint
from src.controllers.material_detail_controller import delete_material_detail, get_material_details, get_material_detail_by_id, get_material_details_by_provider, create_material_detail, update_material_detail

material_detail_bp = Blueprint('material_detail', __name__)

@material_detail_bp.route('/', methods=['GET'])
def all_material_details():
    return get_material_details()

@material_detail_bp.route('/<uuid:materials_details_id>', methods=['GET'])
def material_detail_by_id(materials_details_id):
    return get_material_detail_by_id(materials_details_id)

@material_detail_bp.route('/provider/<uuid:provided_id>', methods=['GET'])
def material_details_by_provider(provided_id):
    return get_material_details_by_provider(provided_id)

@material_detail_bp.route('/', methods=['POST'])
def add_material_detail():
    return create_material_detail()

@material_detail_bp.route('/<uuid:materials_details_id>', methods=['PUT'])
def modify_material_detail(materials_details_id):
    return update_material_detail(materials_details_id)

@material_detail_bp.route('/<uuid:materials_details_id>', methods=['DELETE'])
def remove_material_detail(materials_details_id):
    return delete_material_detail(materials_details_id)
