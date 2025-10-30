from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class ProfesoresTab(QWidget):
    """Pestaña de gestión de profesores"""
    def __init__(self, sistema, parent=None):
        super().__init__(parent)
        self.sistema = sistema
        self.parent = parent
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Barra de herramientas
        toolbar = QHBoxLayout()
        
        self.add_btn = QPushButton("Agregar Profesor")
        self.add_btn.setIcon(QIcon.fromTheme("list-add-user"))
        self.add_btn.clicked.connect(self.show_add_dialog)
        
        self.edit_btn = QPushButton("Editar Profesor")
        self.edit_btn.setIcon(QIcon.fromTheme("document-edit"))
        self.edit_btn.clicked.connect(self.show_edit_dialog)
        
        self.delete_btn = QPushButton("Eliminar Profesor")
        self.delete_btn.setIcon(QIcon.fromTheme("list-remove-user"))
        self.delete_btn.clicked.connect(self.delete_profesor)
        
        self.refresh_btn = QPushButton("Actualizar")
        self.refresh_btn.setIcon(QIcon.fromTheme("view-refresh"))
        self.refresh_btn.clicked.connect(self.update_table)
        
        toolbar.addWidget(self.add_btn)
        toolbar.addWidget(self.edit_btn)
        toolbar.addWidget(self.delete_btn)
        toolbar.addStretch()
        toolbar.addWidget(self.refresh_btn)
        
        # Tabla de profesores
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Email", "Teléfono", "Especialidad"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        
        layout.addLayout(toolbar)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        self.update_table()
    
    def update_table(self):
        self.table.setRowCount(0)
        profesores = sorted(self.sistema.obtener_profesores(), key=lambda x: x.nombre)
        
        for profesor in profesores:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            items = [
                QTableWidgetItem(profesor.id_profesor),
                QTableWidgetItem(profesor.nombre),
                QTableWidgetItem(profesor.email),
                QTableWidgetItem(profesor.telefono),
                QTableWidgetItem(profesor.especialidad)
            ]
            
            for col, item in enumerate(items):
                self.table.setItem(row, col, item)
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
    
    def show_add_dialog(self):
        from ..dialogs.profesor import ProfesorDialog
        dialog = ProfesorDialog(parent=self.parent)
        if dialog.exec_() == QDialog.Accepted:
            from models.profesor import Profesor
            data = dialog.get_data()
            
            if not data['id_profesor'] or not data['nombre']:
                QMessageBox.warning(self, "Error", "ID y nombre son campos obligatorios")
                return
                
            nuevo_profesor = Profesor(
                data['id_profesor'],
                data['nombre'],
                data['email'],
                data['telefono'],
                data['especialidad']
            )
            
            if self.sistema.agregar_profesor(nuevo_profesor):
                QMessageBox.information(self, "Éxito", "Profesor agregado correctamente")
                self.update_table()
            else:
                QMessageBox.warning(self, "Error", "El ID de profesor ya existe")
    
    def show_edit_dialog(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Error", "Seleccione un profesor para editar")
            return
        
        id_profesor = self.table.item(selected, 0).text()
        profesor = self.sistema.profesores.get(id_profesor)
        
        if profesor:
            from ..dialogs.profesor import ProfesorDialog
            dialog = ProfesorDialog(profesor, self.parent)
            if dialog.exec_() == QDialog.Accepted:
                from models.profesor import Profesor
                data = dialog.get_data()
                
                if not data['id_profesor'] or not data['nombre']:
                    QMessageBox.warning(self, "Error", "ID y nombre son campos obligatorios")
                    return
                    
                profesor_editado = Profesor(
                    data['id_profesor'],
                    data['nombre'],
                    data['email'],
                    data['telefono'],
                    data['especialidad']
                )
                
                if self.sistema.editar_profesor(id_profesor, profesor_editado):
                    QMessageBox.information(self, "Éxito", "Profesor actualizado correctamente")
                    self.update_table()
                else:
                    QMessageBox.warning(self, "Error", "No se pudo actualizar el profesor")
    
    def delete_profesor(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Error", "Seleccione un profesor para eliminar")
            return
        
        id_profesor = self.table.item(selected, 0).text()
        profesor = self.sistema.profesores.get(id_profesor)
        
        if profesor:
            reply = QMessageBox.question(
                self, "Confirmar", 
                f"¿Está seguro que desea eliminar al profesor {profesor.nombre}?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                if self.sistema.eliminar_profesor(id_profesor):
                    QMessageBox.information(self, "Éxito", "Profesor eliminado correctamente")
                    self.update_table()
                else:
                    QMessageBox.warning(self, "Error", 
                        "No se pudo eliminar el profesor. Verifique que no esté asignado a ninguna asignatura.")