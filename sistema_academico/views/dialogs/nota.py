from PyQt5.QtWidgets import (QDialog, QFormLayout, QComboBox, QDoubleSpinBox, 
                            QDateEdit, QTextEdit, QPushButton, QHBoxLayout, 
                            QLabel, QLineEdit)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon

class NoteDialog(QDialog):
    """Diálogo para agregar/editar notas con información de profesor"""
    def __init__(self, sistema, nota=None, parent=None):
        super().__init__(parent)
        self.sistema = sistema
        self.setWindowTitle("Agregar Nota" if nota is None else "Editar Nota")
        self.setModal(True)
        self.setup_ui(nota)
    
    def setup_ui(self, nota):
        layout = QFormLayout()
        
        # Sección Estudiante
        self.student_combo = QComboBox()
        self.student_combo.setPlaceholderText("Seleccione un estudiante...")
        self.cargar_estudiantes()
        
        # Sección Asignatura
        self.subject_combo = QComboBox()
        self.subject_combo.setPlaceholderText("Seleccione una asignatura...")
        self.subject_combo.currentIndexChanged.connect(self.actualizar_info_profesor)
        self.cargar_asignaturas()
        
        # Información del Profesor (solo lectura)
        self.profesor_label = QLineEdit()
        self.profesor_label.setReadOnly(True)
        self.profesor_label.setStyleSheet("background: #f0f0f0;")
        
        # Campos de la nota
        self.grade_input = QDoubleSpinBox()
        self.grade_input.setRange(0, 5)
        self.grade_input.setSingleStep(0.1)
        self.grade_input.setDecimals(2)
        self.grade_input.setValue(3.0)  # Valor por defecto
        
        self.weight_input = QDoubleSpinBox()
        self.weight_input.setRange(0.1, 5)
        self.weight_input.setSingleStep(0.1)
        self.weight_input.setDecimals(2)
        self.weight_input.setValue(1.0)
        
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("dd/MM/yyyy")
        
        self.description_input = QTextEdit()
        self.description_input.setMaximumHeight(100)
        
        # Si estamos editando una nota existente
        if nota:
            self.cargar_datos_nota(nota)
        
        # Botones
        buttons = QHBoxLayout()
        save_btn = QPushButton("Guardar")
        save_btn.setIcon(QIcon.fromTheme("document-save"))
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.setIcon(QIcon.fromTheme("dialog-cancel"))
        buttons.addWidget(save_btn)
        buttons.addWidget(cancel_btn)
        
        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        
        # Organización del layout
        layout.addRow("Estudiante*:", self.student_combo)
        layout.addRow("Asignatura*:", self.subject_combo)
        layout.addRow("Profesor:", self.profesor_label)
        layout.addRow("Calificación (0-5)*:", self.grade_input)
        layout.addRow("Peso:", self.weight_input)
        layout.addRow("Fecha:", self.date_input)
        layout.addRow("Descripción:", self.description_input)
        layout.addRow(buttons)
        
        # Nota sobre campos obligatorios
        note_label = QLabel("* Campos obligatorios")
        note_label.setStyleSheet("color: #7f8c8d; font-style: italic;")
        layout.addRow(note_label)
        
        self.setLayout(layout)
        self.actualizar_info_profesor()  # Actualizar info profesor inicial
    
    def cargar_estudiantes(self):
        """Carga los estudiantes en el ComboBox"""
        self.student_combo.clear()
        estudiantes = sorted(self.sistema.obtener_estudiantes(), key=lambda x: x.nombre)
        for est in estudiantes:
            self.student_combo.addItem(f"{est.nombre} ({est.codigo})", est.codigo)
    
    def cargar_asignaturas(self):
        """Carga las asignaturas en el ComboBox"""
        self.subject_combo.clear()
        asignaturas = sorted(self.sistema.obtener_asignaturas(), key=lambda x: x.nombre)
        for asig in asignaturas:
            self.subject_combo.addItem(f"{asig.nombre} ({asig.codigo})", asig.codigo)
    
    def actualizar_info_profesor(self):
        """Actualiza la información del profesor cuando cambia la asignatura"""
        codigo_asignatura = self.subject_combo.currentData()
        if codigo_asignatura:
            asignatura = self.sistema.asignaturas.get(codigo_asignatura)
            if asignatura and asignatura.profesor:
                profesor = self.sistema.profesores.get(asignatura.profesor)
                if profesor:
                    self.profesor_label.setText(f"{profesor.nombre} ({profesor.id_profesor})")
                    return
        
        self.profesor_label.setText("No asignado")
    
    def cargar_datos_nota(self, nota):
        """Carga los datos de una nota existente para edición"""
        # Estudiante
        index = self.student_combo.findData(nota.estudiante)
        if index >= 0:
            self.student_combo.setCurrentIndex(index)
        
        # Asignatura
        index = self.subject_combo.findData(nota.asignatura)
        if index >= 0:
            self.subject_combo.setCurrentIndex(index)
        
        # Resto de campos
        self.grade_input.setValue(nota.calificacion)
        self.weight_input.setValue(nota.peso)
        self.date_input.setDate(QDate(nota.fecha.year, nota.fecha.month, nota.fecha.day))
        self.description_input.setPlainText(nota.descripcion)
        
        # Forzar actualización de profesor
        self.actualizar_info_profesor()
    
    def get_data(self):
        """Obtiene los datos del formulario"""
        estudiante = self.student_combo.currentData()
        asignatura = self.subject_combo.currentData()
        
        # Validación básica
        if not estudiante or not asignatura:
            raise ValueError("Debe seleccionar un estudiante y una asignatura")
        
        return {
            'estudiante': estudiante,
            'asignatura': asignatura,
            'calificacion': self.grade_input.value(),
            'fecha': self.date_input.date().toPyDate(),
            'peso': self.weight_input.value(),
            'descripcion': self.description_input.toPlainText().strip(),
            'profesor': self.get_profesor_asignatura(asignatura)
        }
    
    def get_profesor_asignatura(self, codigo_asignatura):
        """Obtiene el ID del profesor asignado a la asignatura"""
        asignatura = self.sistema.asignaturas.get(codigo_asignatura)
        return asignatura.profesor if asignatura else None