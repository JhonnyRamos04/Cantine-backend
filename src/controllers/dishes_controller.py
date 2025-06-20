from flask import jsonify, request
from src.models.dishes import Dish, db
from src.models.product import Product # Importar Product para acceder a sus relaciones si es necesario
from src.models.category import Category # Importar Category para acceder a sus relaciones si es necesario
import uuid

def get_dishes():
    """Obtener todos los platos con detalles de categoría y producto."""
    try:
        # Usar opciones de carga para cargar relaciones de manera segura
        all_dishes = Dish.query.options(
            db.joinedload(Dish.category),
            db.joinedload(Dish.product).joinedload(Product.product_detail), # Cargar detalles del producto si existen
            db.joinedload(Dish.product).joinedload(Product.category) # Cargar categoría del producto si existe
        ).all()
        
        dishes_list = []
        for dish in all_dishes:
            dish_dict = {
                'dishes_id': str(dish.dishes_id),
                'name': dish.name,
                'price': str(dish.price) if dish.price else None,
                'img': dish.img if dish.img else None, # Incluir img aquí
                'category': None,
                'product': None
            }
            
            # Añadir información de categoría si existe
            if dish.category:
                dish_dict['category'] = {
                    'category_id': str(dish.category.category_id),
                    'name': dish.category.name,
                    'description': dish.category.description
                }
            
            # Añadir información de producto si existe
            if dish.product:
                product_info = {
                    'products_id': str(dish.product.products_id),
                    'name': dish.product.name,
                    'product_detail': None,
                    'category': None # Categoría del producto
                }

                # Añadir detalles del producto si existen
                if dish.product.product_detail:
                    product_info['product_detail'] = {
                        'products_details_id': str(dish.product.product_detail.products_details_id),
                        'description': dish.product.product_detail.description,
                        'quantity': dish.product.product_detail.quantity,
                        'price': float(dish.product.product_detail.price) if dish.product.product_detail.price else None
                        # No se carga el proveedor aquí para evitar anidación excesiva a menos que sea explícitamente necesario
                    }
                
                # Añadir categoría del producto si existe
                if dish.product.category:
                    product_info['category'] = {
                        'category_id': str(dish.product.category.category_id),
                        'name': dish.product.category.name
                    }

                dish_dict['product'] = product_info
            
            dishes_list.append(dish_dict)
            
        return jsonify(dishes_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_dish_by_id(dishes_id):
    """Obtener un plato por ID con detalles de categoría y producto."""
    try:
        # Usar opciones de carga para cargar relaciones de manera segura
        dish = Dish.query.options(
            db.joinedload(Dish.category),
            db.joinedload(Dish.product).joinedload(Product.product_detail),
            db.joinedload(Dish.product).joinedload(Product.category)
        ).get(dishes_id)
        
        if not dish:
            return jsonify({"message": "Dish not found"}), 404
            
        # Construir respuesta manualmente para evitar problemas con relaciones anidadas
        dish_dict = {
            'dishes_id': str(dish.dishes_id),
            'name': dish.name,
            'price': str(dish.price) if dish.price else None,
            'img': dish.img if dish.img else None, # Incluir img aquí
            'category': None,
            'product': None
        }
        
        # Añadir información de categoría si existe
        if dish.category:
            dish_dict['category'] = {
                'category_id': str(dish.category.category_id),
                'name': dish.category.name,
                'description': dish.category.description
            }
        
        # Añadir información de producto si existe
        if dish.product:
            product_info = {
                'products_id': str(dish.product.products_id),
                'name': dish.product.name,
                'product_detail': None,
                'category': None # Categoría del producto
            }

            # Añadir detalles del producto si existen
            if dish.product.product_detail:
                product_info['product_detail'] = {
                    'products_details_id': str(dish.product.product_detail.products_details_id),
                    'description': dish.product.product_detail.description,
                    'quantity': dish.product.product_detail.quantity,
                    'price': float(dish.product.product_detail.price) if dish.product.product_detail.price else None
                }
            
            # Añadir categoría del producto si existe
            if dish.product.category:
                product_info['category'] = {
                    'category_id': str(dish.product.category.category_id),
                    'name': dish.product.category.name
                }

            dish_dict['product'] = product_info
        
        return jsonify(dish_dict)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_dishes_by_category(category_id):
    """Obtener platos por ID de categoría."""
    try:
        dishes = Dish.query.filter_by(category_id=category_id).all()
        dishes_list = [d.to_dict() for d in dishes] # to_dict aquí solo incluirá los IDs
        return jsonify(dishes_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== Dish POST Controller ====================

def create_dish():
    """Crear un nuevo plato."""
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        if not data or 'name' not in data or 'price' not in data:
            return jsonify({"error": "Name and price are required"}), 400
                
        # Crear nuevo plato
        new_dish = Dish(
            dishes_id=uuid.uuid4(),
            name=data['name'],
            category_id=data.get('category_id'),
            products_id=data.get('products_id'),
            price=data['price'], # Agregada coma aquí
            img=data.get('img') # Nuevo campo img
        )
        
        # Añadir a la base de datos
        db.session.add(new_dish)
        db.session.commit()
        
        # Construir respuesta manualmente para incluir el plato creado
        created_dish_dict = {
            'dishes_id': str(new_dish.dishes_id),
            'name': new_dish.name,
            'category_id': str(new_dish.category_id) if new_dish.category_id else None,
            'products_id': str(new_dish.products_id) if new_dish.products_id else None,
            'price': str(new_dish.price),
            'img': str(new_dish.img) if new_dish.img else None # Incluir img
        }
        
        return jsonify({
            "message": "Dish created successfully",
            "dish": created_dish_dict
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ==================== Dish PUT Controller ====================

def update_dish(dishes_id):
    """Actualizar un plato existente."""
    try:
        dish = Dish.query.get(dishes_id)
        if not dish:
            return jsonify({"error": "Dish not found"}), 404
            
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        # Actualizar campos si se proporcionan
        if 'name' in data:
            dish.name = data['name']
        if 'category_id' in data:
            dish.category_id = data['category_id']
        if 'products_id' in data:
            dish.products_id = data['products_id']
        if 'price' in data:
            dish.price = data['price']
        if 'img' in data:
            dish.img = data['img'] # Corregido: asignar a dish.img
            
        db.session.commit()
        
        # Construir respuesta manualmente
        updated_dish_dict = {
            'dishes_id': str(dish.dishes_id),
            'name': dish.name,
            'category_id': str(dish.category_id) if dish.category_id else None,
            'products_id': str(dish.products_id) if dish.products_id else None,
            'price': str(dish.price),
            'img': str(dish.img) if dish.img else None # Incluir img
        }
        
        return jsonify({
            "message": "Dish updated successfully",
            "dish": updated_dish_dict
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ==================== Dish DELETE Controller ====================

def delete_dish(dishes_id):
    """Eliminar un plato."""
    try:
        dish = Dish.query.get(dishes_id)
        if not dish:
            return jsonify({"error": "Dish not found"}), 404
            
        db.session.delete(dish)
        db.session.commit()
        
        return jsonify({
            "message": "Dish deleted successfully"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
