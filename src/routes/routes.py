from flask import Blueprint, jsonify
from src.routes.role_routes import role_bp
from src.routes.user_routes import user_bp
from src.routes.status_routes import status_bp
from src.routes.category_routes import category_bp
from src.routes.providers_routes import provider_bp
from src.routes.product_detail_routes import product_detail_bp
from src.routes.product_routes import product_bp
from src.routes.orders_route import orders_bp
from src.routes.dishes_routes import dish_bp
from src.routes.material_detail_routes import material_detail_bp
from src.routes.material_routes import material_bp
from src.routes.auth_routes import auth_bp
from src.routes.protected_routes import protected_bp

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return jsonify({"message": "Bienvenido a la API del sistema de restaurante"})

@main.route('/state')
def status():
    return jsonify({"status": "OK", "message": "La API está funcionando correctamente"})

# Registrar los blueprints
app_route = Blueprint('app_route', __name__)

def register_routes(app):
    # Registrar blueprint principal
    app.register_blueprint(main, url_prefix='/')
    
    # Registrar blueprints de recursos
    app.register_blueprint(role_bp, url_prefix='/roles')
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(status_bp, url_prefix='/status')
    app.register_blueprint(category_bp, url_prefix='/categories')
    app.register_blueprint(provider_bp, url_prefix='/providers')
    app.register_blueprint(product_detail_bp, url_prefix='/product-details')
    app.register_blueprint(product_bp, url_prefix='/products')
    app.register_blueprint(orders_bp, url_prefix='/orders')
    app.register_blueprint(dish_bp, url_prefix='/dishes')
    app.register_blueprint(material_detail_bp, url_prefix='/material-details')
    app.register_blueprint(material_bp, url_prefix='/materials')
    
    # Registrar blueprints de autenticación y rutas protegidas
    app.register_blueprint(auth_bp)
    app.register_blueprint(protected_bp, url_prefix='/protected')
    
    return app
