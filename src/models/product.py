from src.db.connection import db
import uuid

class Product(db.Model):
    __tablename__ = 'products'
    products_id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)
    name = db.Column(db.Text, nullable=False)
    products_details_id = db.Column(db.UUID, db.ForeignKey('products_details.products_details_id'))
    category_id = db.Column(db.UUID, db.ForeignKey('category.category_id'))
    
    # Relaciones
    dishes = db.relationship('Dish', back_populates='product', lazy=True)
    product_detail = db.relationship('ProductDetail', back_populates='products', lazy=True)
    category = db.relationship('Category', back_populates='products', lazy=True)

    def __repr__(self):
        return f'<Product id={self.products_id}, name={self.name}>'
    
    def to_dict(self):
        return {
            'products_id': str(self.products_id),
            'name': self.name,
            'products_details_id': str(self.products_details_id) if self.products_details_id else None,
            'category_id': str(self.category_id) if self.category_id else None
        }
