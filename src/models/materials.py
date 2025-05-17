from src.db.connection import db
import uuid

class Material(db.Model):
    __tablename__ = 'materials'
    materials_id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)
    name = db.Column(db.Text, nullable=False)
    type_id = db.Column(db.Integer)
    materials_details_id = db.Column(db.UUID, db.ForeignKey('materials_details.materials_details_id'))
    
    def __repr__(self):
        return f'<Material id={self.materials_id}, name={self.name}>'
    
    def to_dict(self):
        return {
            'materials_id': str(self.materials_id),
            'name': self.name,
            'type_id': self.type_id,
            'materials_details_id': str(self.materials_details_id) if self.materials_details_id else None
        }
