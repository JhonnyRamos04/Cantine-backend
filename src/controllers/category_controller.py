from flask import jsonify, request
from src.models.category import Category, db
import uuid

def get_categories():
    """Get all categories"""
    try:
        all_categories = Category.query.all()
        categories_list = [c.to_dict() for c in all_categories]
        return jsonify(categories_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_category_by_id(category_id):
    """Get a category by ID"""
    try:
        category = Category.query.get(category_id)
        if category:
            return jsonify(category.to_dict())
        return jsonify({"message": "Category not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== Category POST Controller ====================
def create_category():
    """Create a new category"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'name' not in data:
            return jsonify({"error": "Name is required"}), 400
            
        # Create new category
        new_category = Category(
            category_id=uuid.uuid4(),
            name=data['name'],
            description=data.get('description')
        )
        
        # Add to database
        db.session.add(new_category)
        db.session.commit()
        
        return jsonify({
            "message": "Category created successfully",
            "category": new_category.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ==================== Category PUT Controller ====================

def update_category(category_id):
    """Update an existing category"""
    try:
        category = Category.query.get(category_id)
        if not category:
            return jsonify({"error": "Category not found"}), 404
            
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        # Update fields if provided
        if 'name' in data:
            category.name = data['name']
        if 'description' in data:
            category.description = data['description']
            
        db.session.commit()
        
        return jsonify({
            "message": "Category updated successfully",
            "category": category.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
# ==================== Category DELETE Controller ====================
def delete_category(category_id):
    """Delete a category"""
    try:
        category = Category.query.get(category_id)
        if not category:
            return jsonify({"error": "Category not found"}), 404
            
        # Check if category is being used
        if category.products or category.dishes:
            return jsonify({"error": "Cannot delete category that is in use"}), 400
            
        db.session.delete(category)
        db.session.commit()
        
        return jsonify({
            "message": "Category deleted successfully"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
