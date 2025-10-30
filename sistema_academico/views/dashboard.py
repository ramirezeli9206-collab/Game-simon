import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QGroupBox, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QColor, QBrush
from PyQt5.QtCore import QSize

class DashboardWindow(QWidget):
    """Ventana de dashboard inicial"""
    def __init__(self, sistema, parent=None):
        super().__init__(parent)
        self.sistema = sistema
        self.setup_ui()
        self.update_stats()
    
    def setup_ui(self):
        self.layout = QVBoxLayout()
        
        # Título
        title = QLabel("Dashboard - Sistema de Gestión Académica")
        title.setStyleSheet("""
            font-size: 24px; 
            font-weight: bold; 
            color: #2c3e50;
            padding: 10px;
        """)
        title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title)
        
        # Quick Actions
        quick_actions_group = QGroupBox("⚡ Acciones Rápidas")
        quick_actions_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
        """)
        
        quick_actions_layout = QHBoxLayout()
        
        # Botones de acción con iconos grandes
        self.add_student_btn = self.create_action_button("👤 Agregar Estudiante", "list-add-user", "#3498db")
        self.add_subject_btn = self.create_action_button("📖 Agregar Asignatura", "list-add", "#9b59b6")
        self.add_profesor_btn = self.create_action_button("👨‍🏫 Agregar Profesor", "list-add-user", "#8e44ad")
        self.add_note_btn = self.create_action_button("➕ Agregar Nota", "list-add-document", "#2ecc71")
        
        quick_actions_layout.addWidget(self.add_student_btn)
        quick_actions_layout.addWidget(self.add_subject_btn)
        quick_actions_layout.addWidget(self.add_profesor_btn)
        quick_actions_layout.addWidget(self.add_note_btn)
        
        quick_actions_group.setLayout(quick_actions_layout)
        self.layout.addWidget(quick_actions_group)
        
        # Quick Stats
        self.quick_stats_group = QGroupBox("📊 Estadísticas Generales")
        self.quick_stats_group.setStyleSheet(quick_actions_group.styleSheet())
        
        quick_stats_layout = QGridLayout()
        
        # Crear etiquetas de estadísticas con iconos
        self.total_estudiantes_label = self.create_stat_label("👨‍🎓 Estudiantes:")
        self.total_asignaturas_label = self.create_stat_label("📚 Asignaturas:")
        self.total_profesores_label = self.create_stat_label("👨‍🏫 Profesores:")
        self.total_notas_label = self.create_stat_label("📝 Notas:")
        self.promedio_general_label = self.create_stat_label("📈 Promedio General:")
        self.estudiantes_riesgo_label = self.create_stat_label("⚠️ Estudiantes en Riesgo:")
        self.mejor_estudiante_label = self.create_stat_label("🏆 Mejor Estudiante:")
        self.peor_estudiante_label = self.create_stat_label("🔻 Peor Estudiante:")
        self.mejor_asignatura_label = self.create_stat_label("🌟 Mejor Asignatura:")
        self.peor_asignatura_label = self.create_stat_label("💢 Peor Asignatura:")
        
        quick_stats_layout.addWidget(self.total_estudiantes_label, 0, 0)
        quick_stats_layout.addWidget(self.total_asignaturas_label, 1, 0)
        quick_stats_layout.addWidget(self.total_profesores_label , 2, 0)
        quick_stats_layout.addWidget(self.total_notas_label, 3, 0)
        quick_stats_layout.addWidget(self.promedio_general_label, 4, 0)
        quick_stats_layout.addWidget(self.estudiantes_riesgo_label, 0, 2)
        quick_stats_layout.addWidget(self.mejor_estudiante_label, 1, 2)
        quick_stats_layout.addWidget(self.peor_estudiante_label, 1, 2)
        quick_stats_layout.addWidget(self.mejor_asignatura_label, 3, 2)
        quick_stats_layout.addWidget(self.peor_asignatura_label, 4, 2)
        
        self.quick_stats_group.setLayout(quick_stats_layout)
        self.layout.addWidget(self.quick_stats_group)
        
        # Gráficos
        self.graphs_group = QGroupBox("📈 Visualización de Datos")
        self.graphs_group.setStyleSheet(quick_actions_group.styleSheet())
        
        graphs_layout = QHBoxLayout()
        
        # Gráfico 1: Distribución de notas
        self.figure1 = plt.figure(figsize=(6, 4))
        self.canvas1 = FigureCanvas(self.figure1)
        graphs_layout.addWidget(self.canvas1)
        
        # Gráfico 2: Estudiantes en riesgo
        self.figure2 = plt.figure(figsize=(6, 4))
        self.canvas2 = FigureCanvas(self.figure2)
        graphs_layout.addWidget(self.canvas2)
        
        self.graphs_group.setLayout(graphs_layout)
        self.layout.addWidget(self.graphs_group)
        
        # Botón para ver todo
        self.view_all_btn = self.create_action_button("👁️ Ver Todos los Datos", "document-preview", "#34495e")
        self.layout.addWidget(self.view_all_btn)
        
        self.setLayout(self.layout)
    
    def create_stat_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                padding: 5px;
            }
        """)
        return label
    
    def create_action_button(self, text, icon_name, color):
        button = QPushButton(text)
        button.setIcon(QIcon.fromTheme(icon_name))
        button.setIconSize(QSize(24, 24))
        button.setStyleSheet(f"""
            QPushButton {{
                padding: 12px;
                font-weight: bold;
                font-size: 14px;
                background-color: {color};
                color: white;
                border-radius: 5px;
                min-width: 180px;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(color)};
            }}
            QPushButton:pressed {{
                background-color: {self.darken_color(color, 20)};
            }}
        """)
        return button
    
    def darken_color(self, hex_color, percent=10):
        """Oscurece un color hexadecimal"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darkened = tuple(max(0, int(c * (100 - percent) / 100)) for c in rgb)
        return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"
    
    def update_stats(self):
        stats = self.sistema.obtener_estadisticas_generales()
        
        # Actualizar etiquetas con estilos
        self.update_stat_label(self.total_estudiantes_label, f"👨‍🎓 Estudiantes: {stats['total_estudiantes']}")
        self.update_stat_label(self.total_asignaturas_label, f"📚 Asignaturas: {stats['total_asignaturas']}")
        self.update_stat_label(self.total_profesores_label, f"👨‍🏫 Profesores: {len(self.sistema.profesores)}")
        self.update_stat_label(self.total_notas_label, f"📝 Notas: {stats['total_notas']}")
        self.update_stat_label(self.promedio_general_label, f"📈 Promedio General: {stats['promedio_general']:.2f}")
        
        # Color para estudiantes en riesgo
        riesgo_text = f"⚠️ Estudiantes en Riesgo: {stats['estudiantes_riesgo']}"
        self.estudiantes_riesgo_label.setText(riesgo_text)
        if stats['estudiantes_riesgo'] > 0:
            self.estudiantes_riesgo_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
        else:
            self.estudiantes_riesgo_label.setStyleSheet("color: black;")
        
        # Mejor y peor estudiante/asignatura
        self.update_stat_label(self.mejor_estudiante_label, f"🏆 Mejor Estudiante: {stats['mejor_estudiante'][0]} ({stats['mejor_estudiante'][1]:.2f})")
        self.update_stat_label(self.peor_estudiante_label, f"🔻 Peor Estudiante: {stats['peor_estudiante'][0]} ({stats['peor_estudiante'][1]:.2f})")
        self.update_stat_label(self.mejor_asignatura_label, f"🌟 Mejor Asignatura: {stats['mejor_asignatura'][0]} ({stats['mejor_asignatura'][1]:.2f})")
        self.update_stat_label(self.peor_asignatura_label, f"💢 Peor Asignatura: {stats['peor_asignatura'][0]} ({stats['peor_asignatura'][1]:.2f})")
        
        # Actualizar gráficos
        self.update_charts()
    
    def update_stat_label(self, label, text):
        label.setText(text)
        label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                padding: 5px;
            }
        """)
    
    def update_charts(self):
        # Gráfico 1: Distribución de notas
        self.figure1.clear()
        ax1 = self.figure1.add_subplot(111)
        
        notas = [n.calificacion for n in self.sistema.notas_heap]
        if notas:
            ax1.hist(notas, bins=10, color='#3498db', edgecolor='#2980b9')
            ax1.set_title('Distribución de Notas', fontweight='bold', color='#2c3e50')
            ax1.set_xlabel('Calificación', fontweight='bold', color='#2c3e50')
            ax1.set_ylabel('Cantidad', fontweight='bold', color='#2c3e50')
            ax1.set_xticks([0, 1, 2, 3, 4, 5])
            ax1.grid(True, linestyle='--', alpha=0.7)
            ax1.set_facecolor('#f5f5f5')
        
        # Gráfico 2: Estudiantes en riesgo vs aprobados
        self.figure2.clear()
        ax2 = self.figure2.add_subplot(111)
        
        estudiantes = [e.codigo for e in self.sistema.obtener_estudiantes()]
        aprobados = 0
        riesgo = 0
        
        for codigo in estudiantes:
            prom = self.sistema.calcular_promedio_estudiante(codigo)
            if prom < 3.0:
                riesgo += 1
            else:
                aprobados += 1
        
        if estudiantes:
            labels = ['Aprobados', 'En Riesgo']
            sizes = [aprobados, riesgo]
            colors = ['#2ecc71', '#e74c3c']
            explode = (0.05, 0)  # Resaltar la primera rebanada
            
            ax2.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                   startangle=90, shadow=True, explode=explode, 
                   textprops={'fontweight': 'bold', 'color': '#2c3e50'})
            ax2.axis('equal')
            ax2.set_title('Estudiantes Aprobados vs En Riesgo', fontweight='bold', color='#2c3e50')
            ax2.set_facecolor('#f5f5f5')
        
        self.canvas1.draw()
        self.canvas2.draw()