from src.db.connection import db
import uuid

class Status(db.Model):
    __tablename__ = 'status'
    status_id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    
    # Relaciones
    dishes = db.relationship('Dish', back_populates='status', lazy=True)

    def __repr__(self):
        return f'<Status id={self.status_id}, name={self.name}>'
    
    def to_dict(self):
        return {
            'status_id': str(self.status_id),
            'name': self.name,
            'description': self.description
        }
