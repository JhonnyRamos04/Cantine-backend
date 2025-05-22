from flask import jsonify, request
from src.models.provider import Provider, db
from src.models.product_detail import ProductDetail
from src.models.material_detail import MaterialDetail
import uuid

def get_providers():
    """Get all providers"""
    try:
        # Cargar proveedores sin usar joinedload para evitar problemas con relaciones circulares
        all_providers = Provider.query.all()
        
        # Construir respuesta manualmente
        providers_list = []
        for provider in all_providers:
            # Contar productos y materiales relacionados usando modelos SQLAlchemy
            product_details_count = ProductDetail.query.filter_by(provided_id=provider.provider_id).count()
            material_details_count = MaterialDetail.query.filter_by(provided_id=provider.provider_id).count()
            
            # Calcular valores totales
            total_product_value = 0
            total_material_value = 0
            
            # Consultar detalles de productos usando modelos SQLAlchemy
            product_details = ProductDetail.query.filter_by(provided_id=provider.provider_id).all()
            for detail in product_details:
                if detail.price and detail.quantity:
                    total_product_value += float(detail.price) * detail.quantity
            
            # Consultar detalles de materiales usando modelos SQLAlchemy
            material_details = MaterialDetail.query.filter_by(provided_id=provider.provider_id).all()
            for detail in material_details:
                if detail.price and detail.quantity:
                    total_material_value += float(detail.price) * detail.quantity
            
            provider_dict = {
                'provider_id': str(provider.provider_id),
                'name': provider.name,
                'direction': provider.direction,
                'phone': provider.phone,
                'product_details_count': product_details_count,
                'material_details_count': material_details_count,
                'total_product_value': total_product_value,
                'total_material_value': total_material_value,
                'total_value': total_product_value + total_material_value
            }
            
            providers_list.append(provider_dict)
        
        return jsonify(providers_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_provider_by_id(provider_id):
    """Get a provider by ID"""
    try:
        provider = Provider.query.get(provider_id)
        if not provider:
            return jsonify({"message": "Provider not found"}), 404
        
        # Contar productos y materiales relacionados usando modelos SQLAlchemy
        product_details_count = ProductDetail.query.filter_by(provided_id=provider.provider_id).count()
        material_details_count = MaterialDetail.query.filter_by(provided_id=provider.provider_id).count()
        
        # Calcular valores totales
        total_product_value = 0
        total_material_value = 0
        
        # Consultar detalles de productos usando modelos SQLAlchemy
        product_details = ProductDetail.query.filter_by(provided_id=provider.provider_id).all()
        for detail in product_details:
            if detail.price and detail.quantity:
                total_product_value += float(detail.price) * detail.quantity
        
        # Consultar detalles de materiales usando modelos SQLAlchemy
        material_details = MaterialDetail.query.filter_by(provided_id=provider.provider_id).all()
        for detail in material_details:
            if detail.price and detail.quantity:
                total_material_value += float(detail.price) * detail.quantity
        
        provider_dict = {
            'provider_id': str(provider.provider_id),
            'name': provider.name,
            'direction': provider.direction,
            'phone': provider.phone,
            'product_details_count': product_details_count,
            'material_details_count': material_details_count,
            'total_product_value': total_product_value,
            'total_material_value': total_material_value,
            'total_value': total_product_value + total_material_value
        }
        
        return jsonify(provider_dict)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== Provider POST Controller ====================

def create_provider():
    """Create a new provider"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'name' not in data:
            return jsonify({"error": "Name is required"}), 400
            
        # Create new provider
        new_provider = Provider(
            provider_id=uuid.uuid4(),
            name=data['name'],
            direction=data.get('direction'),
            phone=data.get('phone')
        )
        
        # Add to database
        db.session.add(new_provider)
        db.session.commit()
        
        provider_dict = {
            'provider_id': str(new_provider.provider_id),
            'name': new_provider.name,
            'direction': new_provider.direction,
            'phone': new_provider.phone,
            'product_details_count': 0,
            'material_details_count': 0,
            'total_product_value': 0,
            'total_material_value': 0,
            'total_value': 0
        }
        
        return jsonify({
            "message": "Provider created successfully",
            "provider": provider_dict
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ==================== Provider PUT Controller ====================

def update_provider(provider_id):
    """Update an existing provider"""
    try:
        provider = Provider.query.get(provider_id)
        if not provider:
            return jsonify({"error": "Provider not found"}), 404
            
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        # Update fields if provided
        if 'name' in data:
            provider.name = data['name']
        if 'direction' in data:
            provider.direction = data['direction']
        if 'phone' in data:
            provider.phone = data['phone']
            
        db.session.commit()
        
        provider_dict = {
            'provider_id': str(provider.provider_id),
            'name': provider.name,
            'direction': provider.direction,
            'phone': provider.phone
        }
        
        return jsonify({
            "message": "Provider updated successfully",
            "provider": provider_dict
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ==================== Provider DELETE Controller ====================

def delete_provider(provider_id):
    """Delete a provider"""
    try:
        provider = Provider.query.get(provider_id)
        if not provider:
            return jsonify({"error": "Provider not found"}), 404
            
        # Verificar si el proveedor está siendo utilizado usando modelos SQLAlchemy
        product_details_count = ProductDetail.query.filter_by(provided_id=provider.provider_id).count()
        material_details_count = MaterialDetail.query.filter_by(provided_id=provider.provider_id).count()
        
        if product_details_count > 0 or material_details_count > 0:
            return jsonify({"error": "Cannot delete provider that is in use"}), 400
            
        db.session.delete(provider)
        db.session.commit()
        
        return jsonify({
            "message": "Provider deleted successfully"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
