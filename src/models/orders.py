from src.db.connection import db
import uuid

class Orders(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)
    dishes_id = db.Column(db.UUID, db.ForeignKey('dishes.dishes_id'))
    user_id = db.Column(db.UUID, db.ForeignKey('users.user_id'))
    status_id = db.Column(db.UUID, db.ForeignKey('status.status_id'))
    
    dishes = db.relationship('Dish', back_populates='orders', lazy=True)
    user = db.relationship('User', back_populates='orders', lazy=True)
    status = db.relationship('Status', back_populates='orders', lazy=True)


    def __repr__(self):
        return f'<Order id={self.order_id}>'
    
    def to_dict(self):
       return {
            'order_id': str(self.order_id),
            'dishes_id': str(self.dishes_id),
            'user_id': str(self.user_id),
            'status_id': str(self.status_id)
        }

