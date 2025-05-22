from flask import Blueprint
from src.controllers.status_controller import delete_status, get_status, get_status_by_id, create_status, update_status

status_bp = Blueprint('status', __name__)

@status_bp.route('/', methods=['GET'])
def all_status():
    return get_status()

@status_bp.route('/<uuid:status_id>', methods=['GET'])
def status_by_id(status_id):
    return get_status_by_id(status_id)

@status_bp.route('/', methods=['POST'])
def add_status():
    return create_status()

@status_bp.route('/<uuid:status_id>', methods=['PUT'])
def modify_status(status_id):
    return update_status(status_id)

@status_bp.route('/<uuid:status_id>', methods=['DELETE'])
def remove_status(status_id):
    return delete_status(status_id)
