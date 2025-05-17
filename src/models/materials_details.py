from src.db.connection import db
import uuid

class MaterialDetail(db.Model):
    __tablename__ = 'materials_details'
    materials_details_id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)
    description = db.Column(db.Text)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Numeric(10, 2))
    provided_id = db.Column(db.UUID, db.ForeignKey('providers.provider_id'))
    
    # Relaciones
    materials = db.relationship('Material', backref='material_detail', lazy=True)

    def __repr__(self):
        return f'<MaterialDetail id={self.materials_details_id}, price={self.price}>'
    
    def to_dict(self):
        return {
            'materials_details_id': str(self.materials_details_id),
            'description': self.description,
            'quantity': self.quantity,
            'price': float(self.price) if self.price else None,
            'provided_id': str(self.provided_id) if self.provided_id else None
        }
