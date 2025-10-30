import datetime

class Nota:
    """Clase que representa una nota académica"""
    def __init__(self, estudiante, asignatura, calificacion, fecha=None, peso=1.0, descripcion=""):
        self.estudiante = estudiante
        self.asignatura = asignatura
        self.calificacion = float(calificacion)
        self.fecha = fecha if fecha else datetime.datetime.now()
        self.peso = float(peso)
        self.descripcion = descripcion
    
    def __lt__(self, other):
        return self.calificacion < other.calificacion
    
    def to_dict(self):
        return {
            'estudiante': self.estudiante,
            'asignatura': self.asignatura,
            'calificacion': self.calificacion,
            'fecha': self.fecha.strftime('%Y-%m-%d %H:%M:%S'),
            'peso': self.peso,
            'descripcion': self.descripcion
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['estudiante'],
            data['asignatura'],
            data['calificacion'],
            datetime.datetime.strptime(data['fecha'], '%Y-%m-%d %H:%M:%S'),
            data['peso'],
            data['descripcion']
        )