from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class SubjectsTab(QWidget):
    """Pestaña de gestión de asignaturas"""
    def __init__(self, sistema, parent=None):
        super().__init__(parent)
        self.sistema = sistema
        self.parent = parent
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Barra de herramientas
        toolbar = QHBoxLayout()
        
        self.add_subject_btn = QPushButton("Agregar Asignatura")
        self.add_subject_btn.setIcon(QIcon.fromTheme("list-add"))
        self.add_subject_btn.clicked.connect(self.parent.show_add_subject_dialog)
        
        self.edit_subject_btn = QPushButton("Editar Asignatura")
        self.edit_subject_btn.setIcon(QIcon.fromTheme("document-edit"))
        self.edit_subject_btn.clicked.connect(self.edit_subject)
        
        self.delete_subject_btn = QPushButton("Eliminar Asignatura")
        self.delete_subject_btn.setIcon(QIcon.fromTheme("list-remove"))
        self.delete_subject_btn.clicked.connect(self.delete_subject)
        
        self.refresh_btn = QPushButton("Actualizar")
        self.refresh_btn.setIcon(QIcon.fromTheme("view-refresh"))
        self.refresh_btn.clicked.connect(self.update_table)
        
        toolbar.addWidget(self.add_subject_btn)
        toolbar.addWidget(self.edit_subject_btn)
        toolbar.addWidget(self.delete_subject_btn)
        toolbar.addStretch()
        toolbar.addWidget(self.refresh_btn)
        
        # Tabla de asignaturas
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Código", "Nombre", "Créditos", "Profesor"])
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
        asignaturas = sorted(self.sistema.obtener_asignaturas(), key=lambda x: x.nombre)
        
        for asignatura in asignaturas:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            items = [
                QTableWidgetItem(asignatura.codigo),
                QTableWidgetItem(asignatura.nombre),
                QTableWidgetItem(str(asignatura.creditos)),
                QTableWidgetItem(asignatura.profesor)
            ]
            
            for col, item in enumerate(items):
                self.table.setItem(row, col, item)
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
    
    def edit_subject(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Error", "Seleccione una asignatura para editar")
            return
        
        codigo = self.table.item(selected, 0).text()
        asignatura = self.sistema.asignaturas.get(codigo)
        if asignatura:
            self.parent.show_edit_subject_dialog(asignatura)
    
    def delete_subject(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Error", "Seleccione una asignatura para eliminar")
            return
        
        codigo = self.table.item(selected, 0).text()
        asignatura = self.sistema.asignaturas.get(codigo)
        
        if asignatura:
            reply = QMessageBox.question(
                self, "Confirmar", 
                f"¿Está seguro que desea eliminar la asignatura {asignatura.nombre}?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                if self.sistema.eliminar_asignatura(codigo):
                    QMessageBox.information(self, "Éxito", "Asignatura eliminada correctamente")
                    self.update_table()
                else:
                    QMessageBox.warning(self, "Error", "No se pudo eliminar la asignatura")