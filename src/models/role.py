from src.db.connection import db
import uuid

class Role(db.Model):
    __tablename__ = 'roles'
    roles_id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    
    # Relaciones
    users = db.relationship('User', backref='role', lazy='joined')

    def __repr__(self):
        return f'<Role id={self.roles_id}, name={self.name}>'
    
    def to_dict(self):
        return {
            'roles_id': str(self.roles_id),
            'name': self.name,
            'description': self.description,
            'users_count': len(self.users) if self.users else 0
        }
