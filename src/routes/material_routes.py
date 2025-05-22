from flask import Blueprint
from src.controllers.material_controller import delete_material, get_materials, get_material_by_id, get_materials_by_type, create_material, update_material

material_bp = Blueprint('material', __name__)

@material_bp.route('/', methods=['GET'])
def all_materials():
    return get_materials()

@material_bp.route('/<uuid:materials_id>', methods=['GET'])
def material_by_id(materials_id):
    return get_material_by_id(materials_id)

@material_bp.route('/type/<int:type_id>', methods=['GET'])
def materials_by_type(type_id):
    return get_materials_by_type(type_id)

@material_bp.route('/', methods=['POST'])
def add_material():
    return create_material()

@material_bp.route('/<uuid:materials_id>', methods=['PUT'])
def modify_material(materials_id):
    return update_material(materials_id)

@material_bp.route('/<uuid:materials_id>', methods=['DELETE'])
def remove_material(materials_id):
    return delete_material(materials_id)
