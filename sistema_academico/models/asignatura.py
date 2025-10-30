class Asignatura:
    """Clase que representa una asignatura"""
    def __init__(self, codigo, nombre, creditos=0, profesor=""):
        self.codigo = codigo
        self.nombre = nombre
        self.creditos = creditos
        self.profesor = profesor
    
    def to_dict(self):
        return {
            'codigo': self.codigo,
            'nombre': self.nombre,
            'creditos': self.creditos,
            'profesor': self.profesor
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['codigo'],
            data['nombre'],
            data['creditos'],
            data.get('profesor', "")
        )