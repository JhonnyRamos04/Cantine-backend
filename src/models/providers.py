from src.db.connection import db
import uuid

class Provider(db.Model):
    __tablename__ = 'providers'
    provider_id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)
    name = db.Column(db.Text, nullable=False)
    direction = db.Column(db.Text)
    phone = db.Column(db.Text)
    
    # Relaciones
    product_details = db.relationship('ProductDetail', backref='provider', lazy=True)
    material_details = db.relationship('MaterialDetail', backref='provider', lazy=True)

    def __repr__(self):
        return f'<Provider id={self.provider_id}, name={self.name}>'
    
    def to_dict(self):
        return {
            'provider_id': str(self.provider_id),
            'name': self.name,
            'direction': self.direction,
            'phone': self.phone
        }
