from flask import Blueprint
from src.controllers.provider_controller import delete_provider, get_providers, get_provider_by_id, create_provider, update_provider

provider_bp = Blueprint('provider', __name__)

@provider_bp.route('/', methods=['GET'])
def all_providers():
    return get_providers()

@provider_bp.route('/<uuid:provider_id>', methods=['GET'])
def provider_by_id(provider_id):
    return get_provider_by_id(provider_id)

@provider_bp.route('/', methods=['POST'])
def add_provider():
    return create_provider()

@provider_bp.route('/<uuid:provider_id>', methods=['PUT'])
def modify_provider(provider_id):
    return update_provider(provider_id)

@provider_bp.route('/<uuid:provider_id>', methods=['DELETE'])
def remove_provider(provider_id):
    return delete_provider(provider_id)
