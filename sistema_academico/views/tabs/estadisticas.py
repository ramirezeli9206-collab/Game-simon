from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTabWidget, QComboBox, 
                            QTableWidget, QLabel, QHBoxLayout, QDoubleSpinBox, 
                            QPushButton,QHeaderView,QTableWidgetItem)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush

class StatsTab(QWidget):
    """Pestaña de estadísticas"""
    def __init__(self, sistema, parent=None):
        super().__init__(parent)
        self.sistema = sistema
        self.parent = parent
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Pestañas internas para diferentes estadísticas
        stats_tabs = QTabWidget()
        
        # Estadísticas de estudiantes
        student_stats_tab = QWidget()
        student_stats_layout = QVBoxLayout()
        
        self.student_combo = QComboBox()
        self.student_combo.currentTextChanged.connect(self.update_student_stats)
        
        self.student_notes_table = QTableWidget()
        self.student_notes_table.setColumnCount(4)
        self.student_notes_table.setHorizontalHeaderLabels(["Asignatura", "Calificación", "Peso", "Fecha"])
        self.student_notes_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.student_notes_table.verticalHeader().setVisible(False)
        
        self.student_avg_label = QLabel("Promedio simple: -")
        self.student_weighted_avg_label = QLabel("Promedio ponderado: -")
        self.student_status_label = QLabel("Estado académico: -")
        
        stats_layout = QHBoxLayout()
        stats_layout.addWidget(self.student_avg_label)
        stats_layout.addWidget(self.student_weighted_avg_label)
        stats_layout.addWidget(self.student_status_label)
        
        student_stats_layout.addWidget(QLabel("Seleccionar Estudiante:"))
        student_stats_layout.addWidget(self.student_combo)
        student_stats_layout.addWidget(self.student_notes_table)
        student_stats_layout.addLayout(stats_layout)
        
        student_stats_tab.setLayout(student_stats_layout)
        stats_tabs.addTab(student_stats_tab, "Estudiantes")
        
        # Estadísticas de asignaturas
        subject_stats_tab = QWidget()
        subject_stats_layout = QVBoxLayout()
        
        self.subject_combo = QComboBox()
        self.subject_combo.currentTextChanged.connect(self.update_subject_stats)
        
        self.subject_notes_table = QTableWidget()
        self.subject_notes_table.setColumnCount(4)
        self.subject_notes_table.setHorizontalHeaderLabels(["Estudiante", "Calificación", "Peso", "Fecha"])
        self.subject_notes_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.subject_notes_table.verticalHeader().setVisible(False)
        
        self.subject_avg_label = QLabel("Promedio de la asignatura: -")
        self.subject_status_label = QLabel("Estado de la asignatura: -")
        
        subject_stats_layout.addWidget(QLabel("Seleccionar Asignatura:"))
        subject_stats_layout.addWidget(self.subject_combo)
        subject_stats_layout.addWidget(self.subject_notes_table)
        subject_stats_layout.addWidget(self.subject_avg_label)
        subject_stats_layout.addWidget(self.subject_status_label)
        
        subject_stats_tab.setLayout(subject_stats_layout)
        stats_tabs.addTab(subject_stats_tab, "Asignaturas")
        
        # Ranking de estudiantes
        ranking_tab = QWidget()
        ranking_layout = QVBoxLayout()
        
        self.ranking_table = QTableWidget()
        self.ranking_table.setColumnCount(3)
        self.ranking_table.setHorizontalHeaderLabels(["Posición", "Estudiante", "Promedio"])
        self.ranking_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ranking_table.verticalHeader().setVisible(False)
        
        ranking_layout.addWidget(self.ranking_table)
        ranking_tab.setLayout(ranking_layout)
        stats_tabs.addTab(ranking_tab, "Ranking")
        
        # Estudiantes en riesgo
        risk_tab = QWidget()
        risk_layout = QVBoxLayout()
        
        self.threshold_input = QDoubleSpinBox()
        self.threshold_input.setRange(1.0, 5.0)
        self.threshold_input.setSingleStep(0.1)
        self.threshold_input.setDecimals(2)
        self.threshold_input.setValue(3.0)
        
        threshold_layout = QHBoxLayout()
        threshold_layout.addWidget(QLabel("Umbral de riesgo:"))
        threshold_layout.addWidget(self.threshold_input)
        
        update_btn = QPushButton("Actualizar")
        update_btn.clicked.connect(self.update_risk_students)
        
        self.risk_students_table = QTableWidget()
        self.risk_students_table.setColumnCount(2)
        self.risk_students_table.setHorizontalHeaderLabels(["Estudiante", "Promedio"])
        self.risk_students_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.risk_students_table.verticalHeader().setVisible(False)
        
        risk_layout.addLayout(threshold_layout)
        risk_layout.addWidget(update_btn)
        risk_layout.addWidget(self.risk_students_table)
        
        risk_tab.setLayout(risk_layout)
        stats_tabs.addTab(risk_tab, "Estudiantes en Riesgo")
        
        # Botón para volver al dashboard
        back_btn = QPushButton("Volver al Dashboard")
        back_btn.setIcon(QIcon.fromTheme("go-home"))
        back_btn.clicked.connect(self.parent.show_dashboard)
        
        layout.addWidget(stats_tabs)
        layout.addWidget(back_btn)
        
        self.setLayout(layout)
        
        # Actualizar datos iniciales
        self.update_student_combo()
        self.update_subject_combo()
        self.update_ranking()
        self.update_risk_students()
    
    def update_student_combo(self):
        self.student_combo.clear()
        estudiantes = sorted(self.sistema.obtener_estudiantes(), key=lambda x: x.nombre)
        for est in estudiantes:
            self.student_combo.addItem(f"{est.nombre} ({est.codigo})", est.codigo)
        
        if estudiantes:
            self.update_student_stats()
    
    def update_subject_combo(self):
        self.subject_combo.clear()
        asignaturas = sorted(self.sistema.obtener_asignaturas(), key=lambda x: x.nombre)
        for asig in asignaturas:
            self.subject_combo.addItem(f"{asig.nombre} ({asig.codigo})", asig.codigo)
        
        if asignaturas:
            self.update_subject_stats()
    
    def update_student_stats(self):
        self.student_notes_table.setRowCount(0)
        
        codigo = self.student_combo.currentData()
        if not codigo:
            return
        
        notas = self.sistema.obtener_notas_estudiante(codigo)
        if not notas:
            return
        
        # Mostrar notas en la tabla
        for nota in sorted(notas, key=lambda x: x.asignatura):
            row = self.student_notes_table.rowCount()
            self.student_notes_table.insertRow(row)
            
            # Obtener nombre de asignatura
            asignatura = self.sistema.asignaturas.get(nota.asignatura, None)
            nombre_asignatura = asignatura.nombre if asignatura else nota.asignatura
            
            self.student_notes_table.setItem(row, 0, QTableWidgetItem(nombre_asignatura))
            
            # Celda de calificación con color
            grade_item = QTableWidgetItem(f"{nota.calificacion:.2f}")
            if nota.calificacion < 3.0:
                grade_item.setForeground(QBrush(QColor(231, 76, 60)))  # Rojo
            elif nota.calificacion >= 4.0:
                grade_item.setForeground(QBrush(QColor(46, 204, 113)))  # Verde
            else:
                grade_item.setForeground(QBrush(QColor(241, 196, 15)))  # Amarillo
            self.student_notes_table.setItem(row, 1, grade_item)
            
            self.student_notes_table.setItem(row, 2, QTableWidgetItem(f"{nota.peso:.2f}"))
            self.student_notes_table.setItem(row, 3, QTableWidgetItem(nota.fecha.strftime('%d/%m/%Y')))
        
        # Calcular promedios
        promedio = self.sistema.calcular_promedio_estudiante(codigo)
        promedio_ponderado = self.sistema.calcular_promedio_ponderado_estudiante(codigo)
        
        # Actualizar labels
        self.student_avg_label.setText(f"Promedio simple: {promedio:.2f}")
        self.student_weighted_avg_label.setText(f"Promedio ponderado: {promedio_ponderado:.2f}")
        
        # Estado académico
        if promedio_ponderado < 3.0:
            self.student_status_label.setText("Estado académico: En riesgo")
            self.student_status_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
        elif promedio_ponderado >= 4.0:
            self.student_status_label.setText("Estado académico: Excelente")
            self.student_status_label.setStyleSheet("color: #2ecc71; font-weight: bold;")
        else:
            self.student_status_label.setText("Estado académico: Regular")
            self.student_status_label.setStyleSheet("color: #f1c40f; font-weight: bold;")
    
    def update_subject_stats(self):
        self.subject_notes_table.setRowCount(0)
        
        codigo = self.subject_combo.currentData()
        if not codigo:
            return
        
        notas = self.sistema.obtener_notas_asignatura(codigo)
        if not notas:
            return
        
        # Mostrar notas en la tabla
        for nota in sorted(notas, key=lambda x: x.estudiante):
            row = self.subject_notes_table.rowCount()
            self.subject_notes_table.insertRow(row)
            
            # Obtener nombre de estudiante
            estudiante = self.sistema.estudiantes.get(nota.estudiante, None)
            nombre_estudiante = estudiante.nombre if estudiante else nota.estudiante
            
            self.subject_notes_table.setItem(row, 0, QTableWidgetItem(nombre_estudiante))
            
            # Celda de calificación con color
            grade_item = QTableWidgetItem(f"{nota.calificacion:.2f}")
            if nota.calificacion < 3.0:
                grade_item.setForeground(QBrush(QColor(231, 76, 60)))  # Rojo
            elif nota.calificacion >= 4.0:
                grade_item.setForeground(QBrush(QColor(46, 204, 113)))  # Verde
            else:
                grade_item.setForeground(QBrush(QColor(241, 196, 15)))  # Amarillo
            self.subject_notes_table.setItem(row, 1, grade_item)
            
            self.subject_notes_table.setItem(row, 2, QTableWidgetItem(f"{nota.peso:.2f}"))
            self.subject_notes_table.setItem(row, 3, QTableWidgetItem(nota.fecha.strftime('%d/%m/%Y')))
        
        # Calcular promedio
        promedio = self.sistema.calcular_promedio_asignatura(codigo)
        
        # Actualizar labels
        self.subject_avg_label.setText(f"Promedio de la asignatura: {promedio:.2f}")
        
        # Estado de la asignatura
        if promedio < 3.0:
            self.subject_status_label.setText("Estado de la asignatura: Desempeño bajo")
            self.subject_status_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
        elif promedio >= 4.0:
            self.subject_status_label.setText("Estado de la asignatura: Excelente desempeño")
            self.subject_status_label.setStyleSheet("color: #2ecc71; font-weight: bold;")
        else:
            self.subject_status_label.setText("Estado de la asignatura: Desempeño regular")
            self.subject_status_label.setStyleSheet("color: #f1c40f; font-weight: bold;")
    
    def update_ranking(self):
        self.ranking_table.setRowCount(0)
        
        ranking = self.sistema.ranking_estudiantes()
        
        if not ranking:
            return
        
        for i, (codigo, promedio) in enumerate(ranking, 1):
            row = self.ranking_table.rowCount()
            self.ranking_table.insertRow(row)
            
            # Obtener nombre de estudiante
            estudiante = self.sistema.estudiantes.get(codigo, None)
            nombre_estudiante = estudiante.nombre if estudiante else codigo
            
            self.ranking_table.setItem(row, 0, QTableWidgetItem(str(i)))
            self.ranking_table.setItem(row, 1, QTableWidgetItem(nombre_estudiante))
            
            # Celda de promedio con color según el valor
            avg_item = QTableWidgetItem(f"{promedio:.2f}")
            if promedio < 3.0:
                avg_item.setForeground(QBrush(QColor(231, 76, 60)))  # Rojo
            elif promedio >= 4.0:
                avg_item.setForeground(QBrush(QColor(46, 204, 113)))  # Verde
            else:
                avg_item.setForeground(QBrush(QColor(241, 196, 15)))  # Amarillo
            self.ranking_table.setItem(row, 2, avg_item)
    
    def update_risk_students(self):
        self.risk_students_table.setRowCount(0)
        
        umbral = self.threshold_input.value()
        estudiantes_riesgo = self.sistema.estudiantes_en_riesgo(umbral)
        
        if not estudiantes_riesgo:
            return
        
        for codigo, promedio in estudiantes_riesgo:
            row = self.risk_students_table.rowCount()
            self.risk_students_table.insertRow(row)
            
            # Obtener nombre de estudiante
            estudiante = self.sistema.estudiantes.get(codigo, None)
            nombre_estudiante = estudiante.nombre if estudiante else codigo
            
            self.risk_students_table.setItem(row, 0, QTableWidgetItem(nombre_estudiante))
            
            # Celda de promedio con color rojo
            avg_item = QTableWidgetItem(f"{promedio:.2f}")
            avg_item.setForeground(QBrush(QColor(231, 76, 60)))
            self.risk_students_table.setItem(row, 1, avg_item)