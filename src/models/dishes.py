from src.db.connection import db
import uuid

class Dish(db.Model):
    __tablename__ = 'dishes'
    dishes_id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)
    name = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.UUID, db.ForeignKey('category.category_id'))
    products_id = db.Column(db.UUID, db.ForeignKey('products.products_id'))
    price = db.Column(db.Text)
    img = db.Column(db.Text) # Nuevo campo img
    
    # Relaciones
    
    category = db.relationship('Category', back_populates='dishes', lazy=True)
    product = db.relationship('Product', back_populates='dishes', lazy=True)
    orders = db.relationship('Orders', back_populates='dishes', lazy=True)
    
    def __repr__(self):
        return f'<Dish id={self.dishes_id}, name={self.name}>'
    
    def to_dict(self):
        return {
            'dishes_id': str(self.dishes_id),
            'name': self.name,
            'category_id': str(self.category_id) if self.category_id else None,
            'products_id': str(self.products_id) if self.products_id else None,
            'price': self.price,
            'img': self.img # Incluir img en la representación del diccionario
        }