import heapq
import datetime
import os
import pickle
import csv
from .estudiante import Estudiante
from .asignatura import Asignatura
from .nota import Nota
from .profesor import Profesor

class SistemaNotas:
    """Sistema de gestión de notas, estudiantes y asignaturas"""
    def __init__(self):
        self.notas_heap = []
        self.notas_por_estudiante = {}
        self.notas_por_asignatura = {}
        self.estudiantes = {}  # {codigo: Estudiante}
        self.asignaturas = {}   # {codigo: Asignatura}
        self.profesores = {}
        self.archivo_datos = "sistema_notas.dat"
        self.cargar_datos()
    
    # Métodos para estudiantes
    def agregar_estudiante(self, estudiante):
        if estudiante.codigo in self.estudiantes:
            return False
        self.estudiantes[estudiante.codigo] = estudiante
        self.guardar_datos()
        return True
    
    def editar_estudiante(self, codigo, nuevo_estudiante):
        if codigo not in self.estudiantes:
            return False
        self.estudiantes[codigo] = nuevo_estudiante
        self.guardar_datos()
        return True
    
    def eliminar_estudiante(self, codigo):
        if codigo not in self.estudiantes:
            return False
        del self.estudiantes[codigo]
        
        # Eliminar notas asociadas al estudiante
        notas_a_eliminar = [n for n in self.notas_heap if n.estudiante == codigo]
        for nota in notas_a_eliminar:
            self.notas_heap.remove(nota)
            if codigo in self.notas_por_estudiante:
                self.notas_por_estudiante[codigo].remove(nota)
            if nota.asignatura in self.notas_por_asignatura:
                self.notas_por_asignatura[nota.asignatura].remove(nota)
        
        if codigo in self.notas_por_estudiante:
            del self.notas_por_estudiante[codigo]
        
        self.guardar_datos()
        return True
    
    def obtener_estudiantes(self):
        return list(self.estudiantes.values())
    
    # Métodos para asignaturas
    def agregar_asignatura(self, asignatura):
        if asignatura.codigo in self.asignaturas:
            return False
        self.asignaturas[asignatura.codigo] = asignatura
        self.guardar_datos()
        return True
    
    def editar_asignatura(self, codigo, nueva_asignatura):
        if codigo not in self.asignaturas:
            return False
        self.asignaturas[codigo] = nueva_asignatura
        self.guardar_datos()
        return True
    
    def eliminar_asignatura(self, codigo):
        if codigo not in self.asignaturas:
            return False
        del self.asignaturas[codigo]
        
        # Eliminar notas asociadas a la asignatura
        notas_a_eliminar = [n for n in self.notas_heap if n.asignatura == codigo]
        for nota in notas_a_eliminar:
            self.notas_heap.remove(nota)
            if nota.estudiante in self.notas_por_estudiante:
                self.notas_por_estudiante[nota.estudiante].remove(nota)
            if codigo in self.notas_por_asignatura:
                self.notas_por_asignatura[codigo].remove(nota)
        
        if codigo in self.notas_por_asignatura:
            del self.notas_por_asignatura[codigo]
        
        self.guardar_datos()
        return True
    
    def obtener_asignaturas(self):
        return list(self.asignaturas.values())
    
    # Métodos para notas
    def agregar_nota(self, nota):
        # Verificar que existan el estudiante y la asignatura
        if nota.estudiante not in self.estudiantes or nota.asignatura not in self.asignaturas:
            return False
        
        # Agregar al heap
        heapq.heappush(self.notas_heap, nota)
        
        # Agregar al diccionario de estudiantes
        if nota.estudiante not in self.notas_por_estudiante:
            self.notas_por_estudiante[nota.estudiante] = []
        self.notas_por_estudiante[nota.estudiante].append(nota)
        
        # Agregar al diccionario de asignaturas
        if nota.asignatura not in self.notas_por_asignatura:
            self.notas_por_asignatura[nota.asignatura] = []
        self.notas_por_asignatura[nota.asignatura].append(nota)
        
        self.guardar_datos()
        return True
    
    def editar_nota(self, indice, nueva_nota):
        if indice < 0 or indice >= len(self.notas_heap):
            return False
        
        # Obtener la nota original
        nota_original = self.notas_heap[indice]
        
        # Actualizar en todas las estructuras
        self.notas_heap[indice] = nueva_nota
        if nota_original.estudiante in self.notas_por_estudiante:
            idx = self.notas_por_estudiante[nota_original.estudiante].index(nota_original)
            self.notas_por_estudiante[nota_original.estudiante][idx] = nueva_nota
        
        if nota_original.asignatura in self.notas_por_asignatura:
            idx = self.notas_por_asignatura[nota_original.asignatura].index(nota_original)
            self.notas_por_asignatura[nota_original.asignatura][idx] = nueva_nota
        
        self.guardar_datos()
        return True
    
    def eliminar_nota(self, indice):
        if indice < 0 or indice >= len(self.notas_heap):
            return False
        
        nota = self.notas_heap.pop(indice)
        if nota.estudiante in self.notas_por_estudiante and nota in self.notas_por_estudiante[nota.estudiante]:
            self.notas_por_estudiante[nota.estudiante].remove(nota)
        
        if nota.asignatura in self.notas_por_asignatura and nota in self.notas_por_asignatura[nota.asignatura]:
            self.notas_por_asignatura[nota.asignatura].remove(nota)
        
        self.guardar_datos()
        return True
    
    # Métodos para profesores
    def agregar_profesor(self, profesor):
        if profesor.id_profesor in self.profesores:
            return False
        self.profesores[profesor.id_profesor] = profesor
        self.guardar_datos()
        return True
    
    def editar_profesor(self, id_profesor, nuevo_profesor):
        if id_profesor not in self.profesores:
            return False
        self.profesores[id_profesor] = nuevo_profesor
        self.guardar_datos()
        return True
    
    def eliminar_profesor(self, id_profesor):
        if id_profesor not in self.profesores:
            return False
        
        # Verificar si el profesor está asignado a alguna asignatura
        for asignatura in self.asignaturas.values():
            if asignatura.profesor == id_profesor:
                return False  # No se puede eliminar si está asignado
        
        del self.profesores[id_profesor]
        self.guardar_datos()
        return True
    
    def obtener_profesores(self):
        return list(self.profesores.values())
    
    # Métodos de consulta
    def obtener_notas_estudiante(self, codigo_estudiante):
        return self.notas_por_estudiante.get(codigo_estudiante, [])
    
    def obtener_notas_asignatura(self, codigo_asignatura):
        return self.notas_por_asignatura.get(codigo_asignatura, [])
    
    def obtener_notas_mas_bajas(self, n=5):
        if not self.notas_heap:
            return []
        
        heap_temp = self.notas_heap.copy()
        notas_bajas = []
        
        for _ in range(min(n, len(heap_temp))):
            if heap_temp:
                notas_bajas.append(heapq.heappop(heap_temp))
                
        return notas_bajas
    
    # Métodos de cálculo
    def calcular_promedio_estudiante(self, codigo_estudiante):
        notas = self.obtener_notas_estudiante(codigo_estudiante)
        if not notas:
            return 0
        return sum(n.calificacion for n in notas) / len(notas)
    
    def calcular_promedio_ponderado_estudiante(self, codigo_estudiante):
        notas = self.obtener_notas_estudiante(codigo_estudiante)
        if not notas:
            return 0
        
        suma_ponderada = sum(n.calificacion * n.peso for n in notas)
        suma_pesos = sum(n.peso for n in notas)
        
        return suma_ponderada / suma_pesos if suma_pesos != 0 else 0
    
    def calcular_promedio_asignatura(self, codigo_asignatura):
        notas = self.obtener_notas_asignatura(codigo_asignatura)
        if not notas:
            return 0
        return sum(n.calificacion for n in notas) / len(notas)
    
    def calcular_promedio_general(self):
        if not self.notas_heap:
            return 0
        return sum(n.calificacion for n in self.notas_heap) / len(self.notas_heap)
    
    def estudiantes_en_riesgo(self, umbral=3.0):
        estudiantes_riesgo = []
        for codigo in self.estudiantes:
            promedio = self.calcular_promedio_estudiante(codigo)
            if promedio < umbral:
                estudiantes_riesgo.append((codigo, promedio))
        return sorted(estudiantes_riesgo, key=lambda x: x[1])
    
    def ranking_estudiantes(self):
        ranking = []
        for codigo in self.estudiantes:
            promedio = self.calcular_promedio_estudiante(codigo)
            ranking.append((codigo, promedio))
        return sorted(ranking, key=lambda x: x[1], reverse=True)
    
    def obtener_estadisticas_generales(self):
        stats = {
            'total_estudiantes': len(self.estudiantes),
            'total_asignaturas': len(self.asignaturas),
            'total_notas': len(self.notas_heap),
            'promedio_general': self.calcular_promedio_general(),
            'estudiantes_riesgo': len(self.estudiantes_en_riesgo()),
            'mejor_estudiante': self.obtener_mejor_estudiante(),
            'peor_estudiante': self.obtener_peor_estudiante(),
            'mejor_asignatura': self.obtener_mejor_asignatura(),
            'peor_asignatura': self.obtener_peor_asignatura()
        }
        return stats
    
    def obtener_mejor_estudiante(self):
        ranking = self.ranking_estudiantes()
        if not ranking:
            return ("N/A", 0)
        mejor_codigo, mejor_prom = ranking[0]
        nombre = self.estudiantes[mejor_codigo].nombre if mejor_codigo in self.estudiantes else "N/A"
        return (nombre, mejor_prom)
    
    def obtener_peor_estudiante(self):
        ranking = self.ranking_estudiantes()
        if not ranking:
            return ("N/A", 0)
        peor_codigo, peor_prom = ranking[-1]
        nombre = self.estudiantes[peor_codigo].nombre if peor_codigo in self.estudiantes else "N/A"
        return (nombre, peor_prom)
    
    def obtener_mejor_asignatura(self):
        asignaturas = [(asig.codigo, self.calcular_promedio_asignatura(asig.codigo)) 
                      for asig in self.asignaturas.values()]
        if not asignaturas:
            return ("N/A", 0)
        mejor_codigo, mejor_prom = max(asignaturas, key=lambda x: x[1])
        nombre = self.asignaturas[mejor_codigo].nombre if mejor_codigo in self.asignaturas else "N/A"
        return (nombre, mejor_prom)
    
    def obtener_peor_asignatura(self):
        asignaturas = [(asig.codigo, self.calcular_promedio_asignatura(asig.codigo)) 
                      for asig in self.asignaturas.values()]
        if not asignaturas:
            return ("N/A", 0)
        peor_codigo, peor_prom = min(asignaturas, key=lambda x: x[1])
        nombre = self.asignaturas[peor_codigo].nombre if peor_codigo in self.asignaturas else "N/A"
        return (nombre, peor_prom)
    
    # Persistencia de datos
    def guardar_datos(self):
        data = {
            'estudiantes': {codigo: est.to_dict() for codigo, est in self.estudiantes.items()},
            'asignaturas': {codigo: asig.to_dict() for codigo, asig in self.asignaturas.items()},
            'profesores': {id: prof.to_dict() for id, prof in self.profesores.items()},
            'notas': [nota.to_dict() for nota in self.notas_heap],
            'notas_por_estudiante': {codigo: [nota.to_dict() for nota in notas] 
                                    for codigo, notas in self.notas_por_estudiante.items()},
            'notas_por_asignatura': {codigo: [nota.to_dict() for nota in notas] 
                                    for codigo, notas in self.notas_por_asignatura.items()}
        }
        try:
            with open(self.archivo_datos, 'wb') as f:
                pickle.dump(data, f)
            return True
        except Exception as e:
            print(f"Error al guardar datos: {e}")
            return False
    
    def cargar_datos(self):
        try:
            if os.path.exists(self.archivo_datos):
                with open(self.archivo_datos, 'rb') as f:
                    data = pickle.load(f)
                    
                    # Cargar estudiantes
                    self.estudiantes = {codigo: Estudiante.from_dict(est_data) 
                                      for codigo, est_data in data.get('estudiantes', {}).items()}
                    
                    # Cargar asignaturas
                    self.asignaturas = {codigo: Asignatura.from_dict(asig_data) 
                                     for codigo, asig_data in data.get('asignaturas', {}).items()}
                    
                    # Cargar profesores
                    self.profesores = {id: Profesor.from_dict(prof_data) 
                                    for id, prof_data in data.get('profesores', {}).items()}
                    
                    # Cargar notas
                    self.notas_heap = [Nota.from_dict(nota_data) for nota_data in data.get('notas', [])]
                    
                    # Reconstruir diccionarios de notas por estudiante y asignatura
                    self.notas_por_estudiante = {}
                    for nota in self.notas_heap:
                        if nota.estudiante not in self.notas_por_estudiante:
                            self.notas_por_estudiante[nota.estudiante] = []
                        self.notas_por_estudiante[nota.estudiante].append(nota)
                    
                    self.notas_por_asignatura = {}
                    for nota in self.notas_heap:
                        if nota.asignatura not in self.notas_por_asignatura:
                            self.notas_por_asignatura[nota.asignatura] = []
                        self.notas_por_asignatura[nota.asignatura].append(nota)
                    
            return True
        except Exception as e:
            print(f"Error al cargar datos: {e}")
            # Si hay error, inicializar estructuras vacías
            self.notas_heap = []
            self.notas_por_estudiante = {}
            self.notas_por_asignatura = {}
            self.estudiantes = {}
            self.asignaturas = {}
            return False
    
    def exportar_csv(self, nombre_archivo="notas_exportadas.csv"):
        try:
            with open(nombre_archivo, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Estudiante', 'Asignatura', 'Calificación', 'Fecha', 'Peso', 'Descripción'])
                for nota in self.notas_heap:
                    writer.writerow([
                        nota.estudiante,
                        nota.asignatura,
                        nota.calificacion,
                        nota.fecha.strftime('%d/%m/%Y'),
                        nota.peso,
                        nota.descripcion
                    ])
            return True
        except Exception as e:
            print(f"Error al exportar datos: {e}")
            return False
    
    def importar_csv(self, nombre_archivo):
        try:
            if not os.path.exists(nombre_archivo):
                return False, "El archivo no existe"
            
            with open(nombre_archivo, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # Saltar encabezado
                
                contador = 0
                for fila in reader:
                    if len(fila) >= 6:
                        estudiante, asignatura, calificacion, fecha_str, peso, descripcion = fila
                        try:
                            fecha = datetime.datetime.strptime(fecha_str, '%d/%m/%Y')
                            nota = Nota(
                                estudiante=estudiante,
                                asignatura=asignatura,
                                calificacion=float(calificacion),
                                fecha=fecha,
                                peso=float(peso),
                                descripcion=descripcion
                            )
                            if self.agregar_nota(nota):
                                contador += 1
                        except Exception as e:
                            print(f"Error al procesar fila {fila}: {e}")
                
            return True, f"Se importaron {contador} notas"
        except Exception as e:
            print(f"Error al importar datos: {e}")
            return False, str(e)