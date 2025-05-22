from src.db.connection import db
import uuid

class ProductDetail(db.Model):
    __tablename__ = 'products_details'
    products_details_id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)
    description = db.Column(db.Text)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Numeric(10, 2))
    provided_id = db.Column(db.UUID, db.ForeignKey('providers.provider_id'))
    
    # Relaciones
    products = db.relationship('Product', back_populates='product_detail', lazy=True)
    provider = db.relationship('Provider', back_populates='product_details', lazy=True)

    def __repr__(self):
        return f'<ProductDetail id={self.products_details_id}, price={self.price}>'
    
    def to_dict(self):
        return {
            'products_details_id': str(self.products_details_id),
            'description': self.description,
            'quantity': self.quantity,
            'price': float(self.price) if self.price else None,
            'provided_id': str(self.provided_id) if self.provided_id else None
        }
