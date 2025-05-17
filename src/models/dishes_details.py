from src.db.connection import db
import uuid

class DishDetail(db.Model):
    __tablename__ = 'dishes_details'
    dishes_details_id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2))
    
    # Relaciones
    dishes = db.relationship('Dish', backref='dish_detail', lazy=True)

    def __repr__(self):
        return f'<DishDetail id={self.dishes_details_id}, price={self.price}>'
    
    def to_dict(self):
        return {
            'dishes_details_id': str(self.dishes_details_id),
            'description': self.description,
            'price': float(self.price) if self.price else None
        }
