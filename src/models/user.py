from werkzeug.security import generate_password_hash, check_password_hash
from src.db.connection import db
import uuid

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    roles_id = db.Column(db.UUID, db.ForeignKey('roles.roles_id'), nullable=False)
    
    def __repr__(self):
        return f'<User id={self.user_id}, name={self.name}, email={self.email}>'
    
    def set_password(self, password):
        """Establece la contraseña hasheada para el usuario"""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica si la contraseña proporcionada coincide con la almacenada"""
        return check_password_hash(self.password, password)
    
    def to_dict(self):
        role_info = None
        
        if self.roles_id:
            rol = self.role
            if rol:
                role_info = {
                    'roles_id': str(rol.roles_id),
                    'name': rol.name,
                    'description': rol.description
                }
        
        return {
            'user_id': str(self.user_id),
            'name': self.name,
            'email': self.email,
            'roles_id': str(self.roles_id),
            'role': role_info
        }
