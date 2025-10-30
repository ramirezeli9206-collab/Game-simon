from PyQt5.QtWidgets import (QDialog, QFormLayout, QLineEdit, QPushButton, 
                            QHBoxLayout, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class ProfesorDialog(QDialog):
    """Diálogo para agregar/editar profesores"""
    def __init__(self, profesor=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar Profesor" if profesor is None else "Editar Profesor")
        self.setModal(True)
        self.setup_ui(profesor)
    
    def setup_ui(self, profesor):
        layout = QFormLayout()
        
        self.id_input = QLineEdit()
        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.specialty_input = QLineEdit()
        
        if profesor:
            self.id_input.setText(profesor.id_profesor)
            self.id_input.setEnabled(False)
            self.name_input.setText(profesor.nombre)
            self.email_input.setText(profesor.email)
            self.phone_input.setText(profesor.telefono)
            self.specialty_input.setText(profesor.especialidad)
        
        buttons = QHBoxLayout()
        save_btn = QPushButton("Guardar")
        save_btn.setIcon(QIcon.fromTheme("document-save"))
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.setIcon(QIcon.fromTheme("dialog-cancel"))
        buttons.addWidget(save_btn)
        buttons.addWidget(cancel_btn)
        
        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        
        layout.addRow("ID Profesor*:", self.id_input)
        layout.addRow("Nombre Completo*:", self.name_input)
        layout.addRow("Correo Electrónico:", self.email_input)
        layout.addRow("Teléfono:", self.phone_input)
        layout.addRow("Especialidad:", self.specialty_input)
        layout.addRow(buttons)
        
        note_label = QLabel("* Campos obligatorios")
        note_label.setStyleSheet("color: #7f8c8d; font-style: italic;")
        layout.addRow(note_label)
        
        self.setLayout(layout)
    
    def get_data(self):
        return {
            'id_profesor': self.id_input.text().strip(),
            'nombre': self.name_input.text().strip(),
            'email': self.email_input.text().strip(),
            'telefono': self.phone_input.text().strip(),
            'especialidad': self.specialty_input.text().strip()
        }