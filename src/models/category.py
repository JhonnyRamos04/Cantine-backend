from src.db.connection import db
import uuid

class Category(db.Model):
    __tablename__ = 'category'
    category_id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    
    # Relaciones
    products = db.relationship('Product', back_populates='category', lazy=True)
    dishes = db.relationship('Dish', back_populates='category', lazy=True)

    def __repr__(self):
        return f'<Category id={self.category_id}, name={self.name}>'
    
    def to_dict(self):
        return {
            'category_id': str(self.category_id),
            'name': self.name,
            'description': self.description
        }
