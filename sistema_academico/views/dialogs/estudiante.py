from PyQt5.QtWidgets import (QDialog, QFormLayout, QLineEdit, QPushButton, 
                            QHBoxLayout, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class StudentDialog(QDialog):
    """Diálogo para agregar/editar estudiantes"""
    def __init__(self, estudiante=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar Estudiante" if estudiante is None else "Editar Estudiante")
        self.setModal(True)
        self.setup_ui(estudiante)
    
    def setup_ui(self, estudiante):
        layout = QFormLayout()
        
        self.code_input = QLineEdit()
        self.name_input = QLineEdit()
        self.program_input = QLineEdit()
        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()
        
        if estudiante:
            self.code_input.setText(estudiante.codigo)
            self.code_input.setEnabled(False)  # No se puede editar el código
            self.name_input.setText(estudiante.nombre)
            self.program_input.setText(estudiante.programa)
            self.email_input.setText(estudiante.email)
            self.phone_input.setText(estudiante.telefono)
        
        buttons = QHBoxLayout()
        save_btn = QPushButton("Guardar")
        save_btn.setIcon(QIcon.fromTheme("document-save"))
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.setIcon(QIcon.fromTheme("dialog-cancel"))
        buttons.addWidget(save_btn)
        buttons.addWidget(cancel_btn)
        
        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        
        layout.addRow("Código de Estudiante*:", self.code_input)
        layout.addRow("Nombre Completo*:", self.name_input)
        layout.addRow("Programa Académico*:", self.program_input)
        layout.addRow("Correo Electrónico:", self.email_input)
        layout.addRow("Teléfono:", self.phone_input)
        layout.addRow(buttons)
        
        # Añadir nota sobre campos obligatorios
        note_label = QLabel("* Campos obligatorios")
        note_label.setStyleSheet("color: #7f8c8d; font-style: italic;")
        layout.addRow(note_label)
        
        self.setLayout(layout)
    
    def get_data(self):
        return {
            'codigo': self.code_input.text().strip(),
            'nombre': self.name_input.text().strip(),
            'programa': self.program_input.text().strip(),
            'email': self.email_input.text().strip(),
            'telefono': self.phone_input.text().strip()
        }