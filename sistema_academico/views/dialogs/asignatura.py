from PyQt5.QtWidgets import (QDialog, QFormLayout, QLineEdit, QPushButton, 
                            QHBoxLayout, QLabel, QSpinBox, QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class SubjectDialog(QDialog):
    """Diálogo para agregar/editar asignaturas con selección de profesor"""
    def __init__(self, sistema, asignatura=None, parent=None):
        super().__init__(parent)
        self.sistema = sistema
        self.setWindowTitle("Agregar Asignatura" if asignatura is None else "Editar Asignatura")
        self.setModal(True)
        self.setup_ui(asignatura)
    
    def setup_ui(self, asignatura):
        layout = QFormLayout()
        
        # Campos de la asignatura
        self.code_input = QLineEdit()
        self.name_input = QLineEdit()
        self.credits_input = QSpinBox()
        self.credits_input.setRange(0, 10)
        
        # ComboBox para selección de profesor
        self.profesor_combo = QComboBox()
        self.profesor_combo.setPlaceholderText("Seleccione un profesor...")
        
        # Llenar el combo de profesores
        self.cargar_profesores()
        
        if asignatura:
            self.code_input.setText(asignatura.codigo)
            self.code_input.setEnabled(False)  # No se puede editar el código
            self.name_input.setText(asignatura.nombre)
            self.credits_input.setValue(asignatura.creditos)
            
            # Seleccionar el profesor actual si existe
            if asignatura.profesor:
                index = self.profesor_combo.findData(asignatura.profesor)
                if index >= 0:
                    self.profesor_combo.setCurrentIndex(index)
        
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
        layout.addRow("Código de Asignatura*:", self.code_input)
        layout.addRow("Nombre*:", self.name_input)
        layout.addRow("Créditos:", self.credits_input)
        layout.addRow("Profesor*:", self.profesor_combo)
        layout.addRow(buttons)
        
        # Nota sobre campos obligatorios
        note_label = QLabel("* Campos obligatorios")
        note_label.setStyleSheet("color: #7f8c8d; font-style: italic;")
        layout.addRow(note_label)
        
        self.setLayout(layout)
    
    def cargar_profesores(self):
        """Carga los profesores disponibles en el ComboBox"""
        self.profesor_combo.clear()
        profesores = sorted(self.sistema.obtener_profesores(), key=lambda x: x.nombre)
        for profesor in profesores:
            self.profesor_combo.addItem(f"{profesor.nombre} ({profesor.id_profesor})", profesor.id_profesor)
        
        # Agregar opción vacía al inicio
        self.profesor_combo.insertItem(0, "No asignado", "")
        self.profesor_combo.setCurrentIndex(0)
    
    def get_data(self):
        """Obtiene los datos del formulario"""
        profesor_id = self.profesor_combo.currentData()
        
        # Validar que se haya seleccionado un profesor válido
        if profesor_id == "":
            profesor_id = None  # O podrías lanzar una excepción o mostrar un mensaje
        
        return {
            'codigo': self.code_input.text().strip(),
            'nombre': self.name_input.text().strip(),
            'creditos': self.credits_input.value(),
            'profesor': profesor_id
        }