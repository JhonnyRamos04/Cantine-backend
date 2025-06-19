from flask import Blueprint
# Importamos nuestro jwt_required personalizado en lugar del de flask_jwt_extended
from src.middlewares.auth import jwt_required, admin_required, role_required

#========= App Imports =========
from src.controllers.role_controller import create_role
from src.controllers.user_controller import create_user
from src.controllers.status_controller import create_status
from src.controllers.category_controller import create_category
from src.controllers.provider_controller import create_provider
from src.controllers.product_detail_controller import create_product_detail
from src.controllers.product_controller import create_product
from src.controllers.orders_controller import create_order
from src.controllers.dishes_controller import create_dish
from src.controllers.material_detail_controller import create_material_detail
from src.controllers.material_controller import create_material

protected_bp = Blueprint('protected', __name__)

# Rutas que requieren autenticación básica - AHORA ACCESIBLES SIN AUTENTICACIÓN
@protected_bp.route('/products', methods=['POST'])
@jwt_required()  # Este decorador ahora permite acceso a todos
def add_product():
    return create_product()

@protected_bp.route('/product-details', methods=['POST'])
@jwt_required()  # Este decorador ahora permite acceso a todos
def add_product_detail():
    return create_product_detail()

# Rutas que requieren rol de administrador - AHORA ACCESIBLES SIN AUTENTICACIÓN
@protected_bp.route('/status', methods=['POST'])
@admin_required()  # Este decorador ahora permite acceso a todos
def add_status():
    return create_status()

@protected_bp.route('/roles', methods=['POST'])
@admin_required()  # Este decorador ahora permite acceso a todos
def add_role():
    return create_role()

@protected_bp.route('/categories', methods=['POST'])
@admin_required()  # Este decorador ahora permite acceso a todos
def add_category():
    return create_category()

@protected_bp.route('/users', methods=['POST'])
@admin_required()  # Este decorador ahora permite acceso a todos
def add_user():
    return create_user()

# Rutas que requieren roles específicos - AHORA ACCESIBLES SIN AUTENTICACIÓN
@protected_bp.route('/dishes', methods=['POST'])
@role_required(['1', '2'])  # Este decorador ahora permite acceso a todos
def add_dish():
    return create_dish()

@protected_bp.route('/dish-details', methods=['POST'])
@role_required(['1', '2'])  # Este decorador ahora permite acceso a todos
def add_dish_detail():
    return create_order()

@protected_bp.route('/providers', methods=['POST'])
@role_required(['1', '2'])  # Este decorador ahora permite acceso a todos
def add_provider():
    return create_provider()

@protected_bp.route('/materials', methods=['POST'])
@role_required(['1', '2', '3'])  # Este decorador ahora permite acceso a todos
def add_material():
    return create_material()

@protected_bp.route('/material-details', methods=['POST'])
@role_required(['1', '2', '3'])  # Este decorador ahora permite acceso a todos
def add_material_detail():
    return create_material_detail()
