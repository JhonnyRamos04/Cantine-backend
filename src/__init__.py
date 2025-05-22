#========== lib imports ===========
from flask import Flask
from flask_cors import CORS

# ============ app imports ========
from src.config.config import ProductionConfig, DevelopmentConfig, TestingConfig
from src.db.connection import db
from src.routes.auth_routes import auth_bp
from src.routes.protected_routes import protected_bp
from src.routes.status_routes import status_bp
from src.routes.role_routes import role_bp
from src.routes.category_routes import category_bp
from src.routes.dishes_detail_routes import dish_detail_bp
from src.routes.dishes_routes import dish_bp
from src.routes.providers_routes import provider_bp
from src.routes.material_detail_routes import material_detail_bp
from src.routes.material_routes import material_bp
from src.routes.product_detail_routes import product_detail_bp
from src.routes.product_routes import product_bp
from src.routes.user_routes import user_bp
from src.config.cors_config import get_cors_config
# Comentamos la importación de JWT para desactivarla
# from src.jwt.jwt import init_jwt
import os

def create_app():
    app = Flask(__name__)
    env = os.environ.get('FLASK_ENV', 'development')

    if env == 'production':
        app.config.from_object(ProductionConfig)
    elif env == 'testing':
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevelopmentConfig)
    
    # Inicializar la base de datos
    db.init_app(app)
    
    # Comentamos la inicialización de JWT para desactivarla
    # init_jwt(app)

    # Configurar CORS
    CORS(app, resources=get_cors_config(env))

    with app.app_context():
        # Registrar rutas
        from src.routes.routes import main
        
        # Registrar blueprint principal
        app.register_blueprint(main)
        
        # Registrar blueprints de recursos
        app.register_blueprint(role_bp, url_prefix='/roles')
        app.register_blueprint(user_bp, url_prefix='/users')
        app.register_blueprint(status_bp, url_prefix='/status')
        app.register_blueprint(category_bp, url_prefix='/categories')
        app.register_blueprint(provider_bp, url_prefix='/providers')
        app.register_blueprint(product_detail_bp, url_prefix='/product-details')
        app.register_blueprint(product_bp, url_prefix='/products')
        app.register_blueprint(dish_detail_bp, url_prefix='/dish-details')
        app.register_blueprint(dish_bp, url_prefix='/dishes')
        app.register_blueprint(material_detail_bp, url_prefix='/material-details')
        app.register_blueprint(material_bp, url_prefix='/materials')
        
        # Registrar blueprints de autenticación y rutas protegidas
        # Mantenemos las rutas pero no serán obligatorias
        app.register_blueprint(auth_bp)
        app.register_blueprint(protected_bp, url_prefix='/protected')

    return app
