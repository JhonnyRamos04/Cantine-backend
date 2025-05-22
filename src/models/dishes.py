from src.db.connection import db
import uuid

class Dish(db.Model):
    __tablename__ = 'dishes'
    dishes_id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)
    name = db.Column(db.Text, nullable=False)
    status_id = db.Column(db.UUID, db.ForeignKey('status.status_id'))
    category_id = db.Column(db.UUID, db.ForeignKey('category.category_id'))
    products_id = db.Column(db.UUID, db.ForeignKey('products.products_id'))
    
    # Relaciones
    status = db.relationship('Status', back_populates='dishes', lazy=True)
    category = db.relationship('Category', back_populates='dishes', lazy=True)
    product = db.relationship('Product', back_populates='dishes', lazy=True)
    
    def __repr__(self):
        return f'<Dish id={self.dishes_id}, name={self.name}>'
    
    def to_dict(self):
        return {
            'dishes_id': str(self.dishes_id),
            'name': self.name,
            'status_id': str(self.status_id) if self.status_id else None,
            'category_id': str(self.category_id) if self.category_id else None,
            'products_id': str(self.products_id) if self.products_id else None
        }
