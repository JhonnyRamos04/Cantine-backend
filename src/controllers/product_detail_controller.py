from flask import jsonify, request
from src.models.product_detail import ProductDetail, db
import uuid

def get_product_details():
    """Get all product details"""
    try:
        # Usar opciones de carga para cargar relaciones
        all_details = ProductDetail.query.options(
            db.joinedload(ProductDetail.provider)
        ).all()
        details_list = [d.to_dict() for d in all_details]
        return jsonify(details_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_product_detail_by_id(products_details_id):
    """Get a product detail by ID"""
    try:
        # Usar opciones de carga para cargar relaciones
        detail = ProductDetail.query.options(
            db.joinedload(ProductDetail.provider)
        ).get(products_details_id)
        if detail:
            return jsonify(detail.to_dict())
        return jsonify({"message": "Product detail not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_product_details_by_provider(provided_id):
    """Get product details for a specific provider"""
    try:
        details = ProductDetail.query.filter_by(provided_id=provided_id).all()
        details_list = [d.to_dict() for d in details]
        return jsonify(details_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== Product Detail POST Controller ====================
def create_product_detail():
    """Create a new product detail"""
    try:
        data = request.get_json()
        
        # Create new product detail
        new_detail = ProductDetail(
            products_details_id=uuid.uuid4(),
            description=data.get('description'),
            quantity=data.get('quantity'),
            price=data.get('price'),
            provided_id=data.get('provided_id')
        )
        
        # Add to database
        db.session.add(new_detail)
        db.session.commit()
        
        return jsonify({
            "message": "Product detail created successfully",
            "product_detail": new_detail.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ==================== Product Detail PUT Controller ====================

def update_product_detail(products_details_id):
    """Update an existing product detail"""
    try:
        detail = ProductDetail.query.get(products_details_id)
        if not detail:
            return jsonify({"error": "Product detail not found"}), 404
            
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        # Update fields if provided
        if 'description' in data:
            detail.description = data['description']
        if 'quantity' in data:
            detail.quantity = data['quantity']
        if 'price' in data:
            detail.price = data['price']
        if 'provided_id' in data:
            detail.provided_id = data['provided_id']
            
        db.session.commit()
        
        return jsonify({
            "message": "Product detail updated successfully",
            "product_detail": detail.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ==================== Product Detail DELETE Controller ====================

def delete_product_detail(products_details_id):
    """Delete a product detail"""
    try:
        detail = ProductDetail.query.get(products_details_id)
        if not detail:
            return jsonify({"error": "Product detail not found"}), 404
            
        # Check if product detail is being used
        if detail.products:
            return jsonify({"error": "Cannot delete product detail that is in use"}), 400
            
        db.session.delete(detail)
        db.session.commit()
        
        return jsonify({
            "message": "Product detail deleted successfully"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
