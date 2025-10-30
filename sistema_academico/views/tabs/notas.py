from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QColor, QBrush
from models.estudiante import Estudiante
from models.asignatura import Asignatura
from models.nota import Nota
from models.sistema_notas import SistemaNotas

class NotesTab(QWidget):
    """Pestaña de gestión de notas"""
    def __init__(self, sistema, parent=None):
        super().__init__(parent)
        self.sistema = sistema
        self.parent = parent
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Barra de herramientas
        toolbar = QHBoxLayout()
        
        self.add_note_btn = QPushButton("Agregar Nota")
        self.add_note_btn.setIcon(QIcon.fromTheme("list-add-document"))
        self.add_note_btn.clicked.connect(self.parent.show_add_note_dialog)
        
        self.edit_note_btn = QPushButton("Editar Nota")
        self.edit_note_btn.setIcon(QIcon.fromTheme("document-edit"))
        self.edit_note_btn.clicked.connect(self.edit_note)
        
        self.delete_note_btn = QPushButton("Eliminar Nota")
        self.delete_note_btn.setIcon(QIcon.fromTheme("list-remove-document"))
        self.delete_note_btn.clicked.connect(self.delete_note)
        
        self.refresh_btn = QPushButton("Actualizar")
        self.refresh_btn.setIcon(QIcon.fromTheme("view-refresh"))
        self.refresh_btn.clicked.connect(self.update_table)
        
        toolbar.addWidget(self.add_note_btn)
        toolbar.addWidget(self.edit_note_btn)
        toolbar.addWidget(self.delete_note_btn)
        toolbar.addStretch()
        toolbar.addWidget(self.refresh_btn)
        
        # Tabla de notas
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Estudiante", "Asignatura", "Calificación", "Fecha", "Peso", "Descripción"])
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
        
        # Ordenar notas por estudiante y asignatura
        notas_ordenadas = sorted(self.sistema.notas_heap, key=lambda x: (
            self.sistema.estudiantes.get(x.estudiante, Estudiante("", x.estudiante, "")).nombre,
            self.sistema.asignaturas.get(x.asignatura, Asignatura("", x.asignatura)).nombre
        ))
        
        for nota in notas_ordenadas:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # Obtener nombres de estudiante y asignatura
            estudiante = self.sistema.estudiantes.get(nota.estudiante, None)
            nombre_estudiante = estudiante.nombre if estudiante else nota.estudiante
            
            asignatura = self.sistema.asignaturas.get(nota.asignatura, None)
            nombre_asignatura = asignatura.nombre if asignatura else nota.asignatura
            
            # Crear items para la tabla
            items = [
                QTableWidgetItem(nombre_estudiante),
                QTableWidgetItem(nombre_asignatura),
                QTableWidgetItem(f"{nota.calificacion:.2f}"),
                QTableWidgetItem(nota.fecha.strftime('%d/%m/%Y')),
                QTableWidgetItem(f"{nota.peso:.2f}"),
                QTableWidgetItem(nota.descripcion)
            ]
            
            # Aplicar colores según la calificación
            if nota.calificacion < 3.0:
                items[2].setForeground(QBrush(QColor(231, 76, 60)))  # Rojo
            elif nota.calificacion >= 4.0:
                items[2].setForeground(QBrush(QColor(46, 204, 113)))  # Verde
            else:
                items[2].setForeground(QBrush(QColor(241, 196, 15)))  # Amarillo
            
            # Hacer celdas no editables
            for col, item in enumerate(items):
                self.table.setItem(row, col, item)
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
    
    def edit_note(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Error", "Seleccione una nota para editar")
            return
        
        nota = self.sistema.notas_heap[selected]
        self.parent.show_edit_note_dialog(nota)
    
    def delete_note(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Error", "Seleccione una nota para eliminar")
            return
        
        reply = QMessageBox.question(
            self, "Confirmar", 
            "¿Está seguro que desea eliminar esta nota?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.sistema.eliminar_nota(selected):
                QMessageBox.information(self, "Éxito", "Nota eliminada correctamente")
                self.update_table()
            else:
                QMessageBox.warning(self, "Error", "No se pudo eliminar la nota")