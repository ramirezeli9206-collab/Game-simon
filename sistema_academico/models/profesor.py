class Profesor:
    """Clase que representa un profesor"""
    def __init__(self, id_profesor, nombre, email="", telefono="", especialidad=""):
        self.id_profesor = id_profesor
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.especialidad = especialidad
    
    def to_dict(self):
        return {
            'id_profesor': self.id_profesor,
            'nombre': self.nombre,
            'email': self.email,
            'telefono': self.telefono,
            'especialidad': self.especialidad
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['id_profesor'],
            data['nombre'],
            data.get('email', ""),
            data.get('telefono', ""),
            data.get('especialidad', "")
        )