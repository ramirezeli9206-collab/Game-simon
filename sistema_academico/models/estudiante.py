class Estudiante:
    """Clase que representa un estudiante"""
    def __init__(self, codigo, nombre, programa, email="", telefono=""):
        self.codigo = codigo
        self.nombre = nombre
        self.programa = programa
        self.email = email
        self.telefono = telefono
    
    def to_dict(self):
        return {
            'codigo': self.codigo,
            'nombre': self.nombre,
            'programa': self.programa,
            'email': self.email,
            'telefono': self.telefono
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['codigo'],
            data['nombre'],
            data['programa'],
            data.get('email', ""),
            data.get('telefono', "")
        )