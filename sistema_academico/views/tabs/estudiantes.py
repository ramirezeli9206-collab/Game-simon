from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QTableWidget, QTableWidgetItem, QHeaderView,QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class StudentsTab(QWidget):
    """Pestaña de gestión de estudiantes"""
    def __init__(self, sistema, parent=None):
        super().__init__(parent)
        self.sistema = sistema
        self.parent = parent
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Barra de herramientas
        toolbar = QHBoxLayout()
        
        self.add_student_btn = QPushButton("Agregar Estudiante")
        self.add_student_btn.setIcon(QIcon.fromTheme("list-add-user"))
        self.add_student_btn.clicked.connect(self.parent.show_add_student_dialog)
        
        self.edit_student_btn = QPushButton("Editar Estudiante")
        self.edit_student_btn.setIcon(QIcon.fromTheme("document-edit"))
        self.edit_student_btn.clicked.connect(self.edit_student)
        
        self.delete_student_btn = QPushButton("Eliminar Estudiante")
        self.delete_student_btn.setIcon(QIcon.fromTheme("list-remove-user"))
        self.delete_student_btn.clicked.connect(self.delete_student)
        
        self.refresh_btn = QPushButton("Actualizar")
        self.refresh_btn.setIcon(QIcon.fromTheme("view-refresh"))
        self.refresh_btn.clicked.connect(self.update_table)
        
        toolbar.addWidget(self.add_student_btn)
        toolbar.addWidget(self.edit_student_btn)
        toolbar.addWidget(self.delete_student_btn)
        toolbar.addStretch()
        toolbar.addWidget(self.refresh_btn)
        
        # Tabla de estudiantes
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Código", "Nombre", "Programa", "Email", "Teléfono"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        
        # Botón para volver al dashboard
        back_btn = QPushButton("Volver al Dashboard")
        back_btn.setIcon(QIcon.fromTheme("go-home"))
        back_btn.clicked.connect(self.parent.show_dashboard)
        
        layout.addLayout(toolbar)
        layout.addWidget(self.table)
        layout.addWidget(back_btn)
        
        self.setLayout(layout)
        
        # Actualizar tabla
        self.update_table()
    
    def update_table(self):
        self.table.setRowCount(0)
        estudiantes = sorted(self.sistema.obtener_estudiantes(), key=lambda x: x.nombre)
        
        for estudiante in estudiantes:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            items = [
                QTableWidgetItem(estudiante.codigo),
                QTableWidgetItem(estudiante.nombre),
                QTableWidgetItem(estudiante.programa),
                QTableWidgetItem(estudiante.email),
                QTableWidgetItem(estudiante.telefono)
            ]
            
            for col, item in enumerate(items):
                self.table.setItem(row, col, item)
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
    
    def edit_student(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Error", "Seleccione un estudiante para editar")
            return
        
        codigo = self.table.item(selected, 0).text()
        estudiante = self.sistema.estudiantes.get(codigo)
        if estudiante:
            self.parent.show_edit_student_dialog(estudiante)
    
    def delete_student(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Error", "Seleccione un estudiante para eliminar")
            return
        
        codigo = self.table.item(selected, 0).text()
        estudiante = self.sistema.estudiantes.get(codigo)
        
        if estudiante:
            reply = QMessageBox.question(
                self, "Confirmar", 
                f"¿Está seguro que desea eliminar al estudiante {estudiante.nombre}?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                if self.sistema.eliminar_estudiante(codigo):
                    QMessageBox.information(self, "Éxito", "Estudiante eliminado correctamente")
                    self.update_table()
                else:
                    QMessageBox.warning(self, "Error", "No se pudo eliminar el estudiante")