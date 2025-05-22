from functools import wraps
from flask import jsonify

# Desactivamos la importación de JWT
# from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
# from src.models.user import User

def admin_required():
    """Decorator para rutas que requieren rol de administrador - DESACTIVADO PARA PRUEBAS"""
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            # Desactivamos la verificación de JWT y permitimos acceso a todos
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def role_required(roles):
    """Decorator para rutas que requieren roles específicos - DESACTIVADO PARA PRUEBAS"""
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            # Desactivamos la verificación de JWT y permitimos acceso a todos
            return fn(*args, **kwargs)
        return decorator
    return wrapper

# Función para reemplazar jwt_required en las rutas
def jwt_required(refresh=False):
    """Reemplazo para jwt_required - DESACTIVADO PARA PRUEBAS"""
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            # Permitimos acceso a todos sin verificar JWT
            return fn(*args, **kwargs)
        return decorator
    return wrapper
