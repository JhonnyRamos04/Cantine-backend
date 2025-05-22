from flask import jsonify, request
from src.models.product import Product, db
from src.models.product_detail import ProductDetail
from src.models.provider import Provider
import uuid

def get_products():
    """Get all products"""
    try:
        # Cargar productos con sus relaciones de manera segura
        all_products = Product.query.options(
            db.joinedload(Product.product_detail),
            db.joinedload(Product.category)
        ).all()
        
        # Convertir a diccionario manualmente para evitar problemas con relaciones anidadas
        products_list = []
        for product in all_products:
            product_dict = {
                'products_id': str(product.products_id),
                'name': product.name,
                'products_details_id': str(product.products_details_id) if product.products_details_id else None,
                'category_id': str(product.category_id) if product.category_id else None,
                'product_detail': None,
                'category': None,
                'dishes': [],
                'dishes_count': 0
            }
            
            # Añadir información de product_detail si existe
            if product.product_detail:
                detail = product.product_detail
                provider_info = None
                
                # Obtener información del proveedor si existe
                if detail.provided_id:
                    provider = Provider.query.get(detail.provided_id)
                    if provider:
                        provider_info = {
                            'provider_id': str(provider.provider_id),
                            'name': provider.name
                        }
                
                product_dict['product_detail'] = {
                    'products_details_id': str(detail.products_details_id),
                    'description': detail.description,
                    'quantity': detail.quantity,
                    'price': float(detail.price) if detail.price else None,
                    'provider': provider_info
                }
            
            # Añadir información de categoría si existe
            if product.category:
                product_dict['category'] = {
                    'category_id': str(product.category.category_id),
                    'name': product.category.name,
                    'description': product.category.description
                }
            
            # Añadir información de platos si existen
            if product.dishes:
                dishes_list = []
                for dish in product.dishes:
                    dishes_list.append({
                        'dishes_id': str(dish.dishes_id),
                        'name': dish.name,
                        'status_id': str(dish.status_id) if dish.status_id else None
                    })
                product_dict['dishes'] = dishes_list
                product_dict['dishes_count'] = len(dishes_list)
            
            products_list.append(product_dict)
        
        return jsonify(products_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_product_by_id(products_id):
    """Get a product by ID"""
    try:
        # Cargar producto con sus relaciones
        product = Product.query.options(
            db.joinedload(Product.product_detail),
            db.joinedload(Product.category)
        ).get(products_id)
        
        if not product:
            return jsonify({"message": "Product not found"}), 404
        
        # Construir respuesta manualmente para evitar problemas con relaciones anidadas
        product_dict = {
            'products_id': str(product.products_id),
            'name': product.name,
            'products_details_id': str(product.products_details_id) if product.products_details_id else None,
            'category_id': str(product.category_id) if product.category_id else None,
            'product_detail': None,
            'category': None,
            'dishes': [],
            'dishes_count': 0
        }
        
        # Añadir información de product_detail si existe
        if product.product_detail:
            detail = product.product_detail
            provider_info = None
            
            # Obtener información del proveedor si existe
            if detail.provided_id:
                provider = Provider.query.get(detail.provided_id)
                if provider:
                    provider_info = {
                        'provider_id': str(provider.provider_id),
                        'name': provider.name
                    }
            
            product_dict['product_detail'] = {
                'products_details_id': str(detail.products_details_id),
                'description': detail.description,
                'quantity': detail.quantity,
                'price': float(detail.price) if detail.price else None,
                'provider': provider_info
            }
        
        # Añadir información de categoría si existe
        if product.category:
            product_dict['category'] = {
                'category_id': str(product.category.category_id),
                'name': product.category.name,
                'description': product.category.description
            }
        
        # Añadir información de platos si existen
        if product.dishes:
            dishes_list = []
            for dish in product.dishes:
                dishes_list.append({
                    'dishes_id': str(dish.dishes_id),
                    'name': dish.name,
                    'status_id': str(dish.status_id) if dish.status_id else None
                })
            product_dict['dishes'] = dishes_list
            product_dict['dishes_count'] = len(dishes_list)
        
        return jsonify(product_dict)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_products_by_category(category_id):
    """Get products by category ID"""
    try:
        products = Product.query.filter_by(category_id=category_id).all()
        products_list = []
        
        for product in products:
            product_dict = {
                'products_id': str(product.products_id),
                'name': product.name,
                'products_details_id': str(product.products_details_id) if product.products_details_id else None,
                'category_id': str(product.category_id) if product.category_id else None
            }
            products_list.append(product_dict)
            
        return jsonify(products_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== Product POST Controller ====================

def create_product():
    """Create a new product"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'name' not in data:
            return jsonify({"error": "Name is required"}), 400
                
        # Create new product
        new_product = Product(
            products_id=uuid.uuid4(),
            name=data['name'],
            products_details_id=data.get('products_details_id'),
            category_id=data.get('category_id')
        )
        
        # Add to database
        db.session.add(new_product)
        db.session.commit()
        
        # Construir respuesta manualmente
        product_dict = {
            'products_id': str(new_product.products_id),
            'name': new_product.name,
            'products_details_id': str(new_product.products_details_id) if new_product.products_details_id else None,
            'category_id': str(new_product.category_id) if new_product.category_id else None
        }
        
        return jsonify({
            "message": "Product created successfully",
            "product": product_dict
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ==================== Product PUT Controller ====================

def update_product(products_id):
    """Update an existing product"""
    try:
        product = Product.query.get(products_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404
            
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        # Update fields if provided
        if 'name' in data:
            product.name = data['name']
        if 'products_details_id' in data:
            product.products_details_id = data['products_details_id']
        if 'category_id' in data:
            product.category_id = data['category_id']
            
        db.session.commit()
        
        # Construir respuesta manualmente
        product_dict = {
            'products_id': str(product.products_id),
            'name': product.name,
            'products_details_id': str(product.products_details_id) if product.products_details_id else None,
            'category_id': str(product.category_id) if product.category_id else None
        }
        
        return jsonify({
            "message": "Product updated successfully",
            "product": product_dict
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ==================== Product DELETE Controller ====================

def delete_product(products_id):
    """Delete a product"""
    try:
        product = Product.query.get(products_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404
            
        # Check if product is being used
        if product.dishes:
            return jsonify({"error": "Cannot delete product that is in use"}), 400
            
        db.session.delete(product)
        db.session.commit()
        
        return jsonify({
            "message": "Product deleted successfully"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
