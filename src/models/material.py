from src.db.connection import db
import uuid

class Material(db.Model):
    __tablename__ = 'materials'
    materials_id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)
    name = db.Column(db.Text, nullable=False)
    type_id = db.Column(db.Integer)
    materials_details_id = db.Column(db.UUID, db.ForeignKey('materials_details.materials_details_id'))
    
    # Relaciones
    material_detail = db.relationship('MaterialDetail', back_populates='materials', lazy=True)

    def __repr__(self):
        return f'<Material id={self.materials_id}, name={self.name}>'
    
    def get_type_name(self):
        """Obtiene el nombre del tipo de material basado en el type_id"""
        # Puedes implementar una lógica más compleja aquí si tienes una tabla de tipos
        # Por ahora, usaremos un mapeo simple
        type_names = {
            1: "Materia Prima",
            2: "Herramienta",
            3: "Equipo",
            4: "Suministro",
            5: "Otro"
        }
        return type_names.get(self.type_id, "Desconocido")
    
    def to_dict(self):
        return {
            'materials_id': str(self.materials_id),
            'name': self.name,
            'type_id': self.type_id,
            'type_name': self.get_type_name(),
            'materials_details_id': str(self.materials_details_id) if self.materials_details_id else None
        }
