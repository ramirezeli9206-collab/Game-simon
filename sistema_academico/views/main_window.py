from PyQt5.QtWidgets import (QMainWindow, QStackedWidget, QTabWidget, QToolBar, 
                            QAction, QMessageBox, QMenuBar, QMenu, QStatusBar,QDialog)
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtCore import Qt, QSize
from models.sistema_notas import SistemaNotas
from .dashboard import DashboardWindow
from .tabs.estudiantes import StudentsTab
from .tabs.asignaturas import SubjectsTab
from .tabs.notas import NotesTab
from .tabs.estadisticas import StatsTab
from .tabs.profesores import ProfesoresTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sistema = SistemaNotas()
        self.setWindowTitle("Sistema de Gestión Académica")
        self.setGeometry(100, 100, 1200, 800)
        
        self.setup_ui()
        self.setup_theme()
        self.create_menu_bar()
        self.create_toolbar()
        
        self.statusBar().showMessage("Sistema listo")
    
    def setup_ui(self):
        # Configurar ventana principal con stacked widget
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        
        # Crear dashboard
        self.dashboard = DashboardWindow(self.sistema, self)
        self.dashboard.add_student_btn.clicked.connect(self.show_add_student_dialog)
        self.dashboard.add_subject_btn.clicked.connect(self.show_add_subject_dialog)
        self.dashboard.add_profesor_btn.clicked.connect(self.show_add_profesor_dialog)
        self.dashboard.add_note_btn.clicked.connect(self.show_add_note_dialog)
        self.dashboard.view_all_btn.clicked.connect(self.show_main_tabs)
        
        # Crear ventana principal con pestañas
        self.main_tabs = QTabWidget()
        self.students_tab = StudentsTab(self.sistema, self)
        self.subjects_tab = SubjectsTab(self.sistema, self)
        self.profesores_tab = ProfesoresTab(self.sistema, self)
        self.notes_tab = NotesTab(self.sistema, self)
        self.stats_tab = StatsTab(self.sistema, self)
        
        self.main_tabs.addTab(self.students_tab, "👥 Estudiantes")
        self.main_tabs.addTab(self.subjects_tab, "📚 Asignaturas")
        self.main_tabs.addTab(self.profesores_tab, "👨‍🏫 Profesores")
        self.main_tabs.addTab(self.notes_tab, "📝 Notas")
        self.main_tabs.addTab(self.stats_tab, "📊 Estadísticas")
        
        # Agregar widgets al stacked widget
        self.central_widget.addWidget(self.dashboard)
        self.central_widget.addWidget(self.main_tabs)
        
        # Mostrar dashboard primero
        self.central_widget.setCurrentIndex(0)
    
    def setup_theme(self):
        """Configura un tema oscuro para la aplicación"""
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        
        self.setPalette(palette)
        self.setStyleSheet("""
            QToolTip {
                color: #ffffff;
                background-color: #2a82da;
                border: 1px solid white;
            }
            QTabWidget::pane {
                border: 1px solid #444;
                top: -1px;
            }
            QTabBar::tab {
                background: #353535;
                color: white;
                padding: 8px;
                border: 1px solid #444;
                border-bottom: none;
            }
            QTabBar::tab:selected {
                background: #2a82da;
                color: black;
            }
            QTableWidget {
                gridline-color: #444;
            }
            QHeaderView::section {
                background-color: #353535;
                color: white;
                padding: 4px;
                border: 1px solid #444;
            }
        """)
    
    def create_menu_bar(self):
        """Crea la barra de menú"""
        menu_bar = self.menuBar()
        
        # Menú Archivo
        file_menu = menu_bar.addMenu("📁 Archivo")
        
        dashboard_action = QAction("🏠 Dashboard", self)
        dashboard_action.triggered.connect(self.show_dashboard)
        file_menu.addAction(dashboard_action)
        
        export_action = QAction("📤 Exportar CSV", self)
        export_action.triggered.connect(self.export_data)
        file_menu.addAction(export_action)
        
        import_action = QAction("📥 Importar CSV", self)
        import_action.triggered.connect(self.import_data)
        file_menu.addAction(import_action)
        
        exit_action = QAction("🚪 Salir", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Menú Editar
        edit_menu = menu_bar.addMenu("✏️ Editar")
        
        add_student_action = QAction("👤 Agregar Estudiante", self)
        add_student_action.triggered.connect(self.show_add_student_dialog)
        edit_menu.addAction(add_student_action)
        
        add_subject_action = QAction("📖 Agregar Asignatura", self)
        add_subject_action.triggered.connect(self.show_add_subject_dialog)
        edit_menu.addAction(add_subject_action)
        
        add_profesor_action = QAction("👨‍🏫 Agregar Profesor", self)
        add_profesor_action.triggered.connect(self.show_add_profesor_dialog)
        edit_menu.addAction(add_profesor_action)
        
        add_note_action = QAction("➕ Agregar Nota", self)
        add_note_action.triggered.connect(self.show_add_note_dialog)
        edit_menu.addAction(add_note_action)
        
        # Menú Ver
        view_menu = menu_bar.addMenu("👁️ Ver")
        
        view_students_action = QAction("👥 Estudiantes", self)
        view_students_action.triggered.connect(lambda: self.show_main_tab(0))
        view_menu.addAction(view_students_action)
        
        view_subjects_action = QAction("📚 Asignaturas", self)
        view_subjects_action.triggered.connect(lambda: self.show_main_tab(1))
        view_menu.addAction(view_subjects_action)
        
        view_profesor_action = QAction("👨‍🏫 Profesor", self)
        view_profesor_action.triggered.connect(lambda: self.show_main_tab(2))
        edit_menu.addAction(view_profesor_action)
        
        view_notes_action = QAction("📝 Notas", self)
        view_notes_action.triggered.connect(lambda: self.show_main_tab(3))
        view_menu.addAction(view_notes_action)
        
        view_stats_action = QAction("📊 Estadísticas", self)
        view_stats_action.triggered.connect(lambda: self.show_main_tab(4))
        view_menu.addAction(view_stats_action)
    
    def create_toolbar(self):
        """Crea la barra de herramientas"""
        toolbar = QToolBar("Barra de herramientas")
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(toolbar)
        
        # Botón para volver al dashboard
        dashboard_action = QAction(QIcon.fromTheme("go-home"), "Dashboard", self)
        dashboard_action.triggered.connect(self.show_dashboard)
        toolbar.addAction(dashboard_action)
        
        toolbar.addSeparator()
        
        # Botón para agregar estudiante
        add_student_action = QAction(QIcon.fromTheme("list-add-user"), "Agregar Estudiante", self)
        add_student_action.triggered.connect(self.show_add_student_dialog)
        toolbar.addAction(add_student_action)
        
        # Botón para agregar asignatura
        add_subject_action = QAction(QIcon.fromTheme("list-add"), "Agregar Asignatura", self)
        add_subject_action.triggered.connect(self.show_add_subject_dialog)
        toolbar.addAction(add_subject_action)
        
        
        # Boton para agregar profesor
        add_profesor_action = QAction(QIcon.fromTheme("list-add"), "Agregar Profesor", self)
        add_profesor_action.triggered.connect(self.show_add_profesor_dialog)
        toolbar.addAction(add_profesor_action)
        
        # Botón para agregar nota
        add_note_action = QAction(QIcon.fromTheme("list-add-document"), "Agregar Nota", self)
        add_note_action.triggered.connect(self.show_add_note_dialog)
        toolbar.addAction(add_note_action)
        
        toolbar.addSeparator()
        
        # Botón para exportar
        export_action = QAction(QIcon.fromTheme("document-export"), "Exportar", self)
        export_action.triggered.connect(self.export_data)
        toolbar.addAction(export_action)
        
        # Botón para importar
        import_action = QAction(QIcon.fromTheme("document-import"), "Importar", self)
        import_action.triggered.connect(self.import_data)
        toolbar.addAction(import_action)
    
    # Métodos para mostrar diálogos
    def show_add_student_dialog(self):
        """Muestra el diálogo para agregar un nuevo estudiante"""
        from .dialogs.estudiante import StudentDialog
        dialog = StudentDialog(parent=self)
        if dialog.exec_() == QDialog.Accepted:
            from models.estudiante import Estudiante
            data = dialog.get_data()
            
            # Validar campos obligatorios
            if not data['codigo'] or not data['nombre'] or not data['programa']:
                QMessageBox.warning(self, "Error", "Código, nombre y programa son campos obligatorios")
                return
                
            # Agregar nuevo estudiante
            nuevo_estudiante = Estudiante(
                data['codigo'],
                data['nombre'],
                data['programa'],
                data['email'],
                data['telefono']
            )
            if self.sistema.agregar_estudiante(nuevo_estudiante):
                QMessageBox.information(self, "Éxito", "Estudiante agregado correctamente")
                self.students_tab.update_table()
                self.stats_tab.update_student_combo()
                self.dashboard.update_stats()
                # Mostrar automáticamente la pestaña de estudiantes
                self.show_main_tab(0)
            else:
                QMessageBox.warning(self, "Error", "El código de estudiante ya existe")
    
    def show_edit_student_dialog(self, estudiante):
        """Muestra el diálogo para editar un estudiante existente"""
        from .dialogs.estudiante import StudentDialog
        dialog = StudentDialog(estudiante, self)
        if dialog.exec_() == QDialog.Accepted:
            from models.estudiante import Estudiante
            data = dialog.get_data()
            
            # Validar campos obligatorios
            if not data['codigo'] or not data['nombre'] or not data['programa']:
                QMessageBox.warning(self, "Error", "Código, nombre y programa son campos obligatorios")
                return
                
            # Editar estudiante existente
            nuevo_estudiante = Estudiante(
                data['codigo'],
                data['nombre'],
                data['programa'],
                data['email'],
                data['telefono']
            )
            if self.sistema.editar_estudiante(data['codigo'], nuevo_estudiante):
                QMessageBox.information(self, "Éxito", "Estudiante actualizado correctamente")
                self.students_tab.update_table()
                self.stats_tab.update_student_combo()
                self.dashboard.update_stats()
            else:
                QMessageBox.warning(self, "Error", "No se pudo actualizar el estudiante")
    
    def show_add_subject_dialog(self):
        """Muestra el diálogo para agregar una nueva asignatura"""
        from .dialogs.asignatura import SubjectDialog
        dialog = SubjectDialog(parent=self)
        if dialog.exec_() == QDialog.Accepted:
            from models.asignatura import Asignatura
            data = dialog.get_data()
            
            # Validar campos obligatorios
            if not data['codigo'] or not data['nombre']:
                QMessageBox.warning(self, "Error", "Código y nombre son campos obligatorios")
                return
                
            # Agregar nueva asignatura
            nueva_asignatura = Asignatura(
                data['codigo'],
                data['nombre'],
                data['creditos'],
                data['profesor']
            )
            if self.sistema.agregar_asignatura(nueva_asignatura):
                QMessageBox.information(self, "Éxito", "Asignatura agregada correctamente")
                self.subjects_tab.update_table()
                self.stats_tab.update_subject_combo()
                self.dashboard.update_stats()
                # Mostrar automáticamente la pestaña de asignaturas
                self.show_main_tab(1)
            else:
                QMessageBox.warning(self, "Error", "El código de asignatura ya existe")
    
    def show_edit_subject_dialog(self, asignatura):
        """Muestra el diálogo para editar una asignatura existente"""
        from .dialogs.asignatura import SubjectDialog
        dialog = SubjectDialog(asignatura, self)
        if dialog.exec_() == QDialog.Accepted:
            from models.asignatura import Asignatura
            data = dialog.get_data()
            
            # Validar campos obligatorios
            if not data['codigo'] or not data['nombre']:
                QMessageBox.warning(self, "Error", "Código y nombre son campos obligatorios")
                return
                
            # Editar asignatura existente
            nueva_asignatura = Asignatura(
                data['codigo'],
                data['nombre'],
                data['creditos'],
                data['profesor']
            )
            if self.sistema.editar_asignatura(data['codigo'], nueva_asignatura):
                QMessageBox.information(self, "Éxito", "Asignatura actualizada correctamente")
                self.subjects_tab.update_table()
                self.stats_tab.update_subject_combo()
                self.dashboard.update_stats()
            else:
                QMessageBox.warning(self, "Error", "No se pudo actualizar la asignatura")
    
    # Agrega métodos para profesores en MainWindow:
    def show_add_profesor_dialog(self):
        from .dialogs.profesor import ProfesorDialog
        dialog = ProfesorDialog(parent=self)
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
                self.profesores_tab.update_table()
                # Actualizar combos en otras pestañas si es necesario
            else:
                QMessageBox.warning(self, "Error", "El ID de profesor ya existe")
    
    def show_add_note_dialog(self):
        """Muestra el diálogo para agregar una nueva nota"""
        # Verificar que hay estudiantes y asignaturas creadas
        if not self.sistema.estudiantes:
            QMessageBox.warning(self, "Error", "No hay estudiantes registrados. Registre al menos un estudiante primero.")
            return
            
        if not self.sistema.asignaturas:
            QMessageBox.warning(self, "Error", "No hay asignaturas registradas. Registre al menos una asignatura primero.")
            return
            
        from .dialogs.nota import NoteDialog
        dialog = NoteDialog(self.sistema, parent=self)
        if dialog.exec_() == QDialog.Accepted:
            from models.nota import Nota
            data = dialog.get_data()
            
            # Validar campos obligatorios
            if not data['estudiante'] or not data['asignatura']:
                QMessageBox.warning(self, "Error", "Debe seleccionar un estudiante y una asignatura")
                return
                
            nueva_nota = Nota(
                data['estudiante'],
                data['asignatura'],
                data['calificacion'],
                data['fecha'],
                data['peso'],
                data['descripcion']
            )
            
            # Agregar nueva nota
            if self.sistema.agregar_nota(nueva_nota):
                QMessageBox.information(self, "Éxito", "Nota agregada correctamente")
                self.notes_tab.update_table()
                self.dashboard.update_stats()
                # Mostrar automáticamente la pestaña de notas
                self.show_main_tab(2)
            else:
                QMessageBox.warning(self, "Error", "No se pudo agregar la nota (verifique estudiante y asignatura)")
    
    def show_edit_note_dialog(self, nota):
        """Muestra el diálogo para editar una nota existente"""
        from .dialogs.nota import NoteDialog
        dialog = NoteDialog(self.sistema, nota, self)
        if dialog.exec_() == QDialog.Accepted:
            from models.nota import Nota
            data = dialog.get_data()
            
            # Validar campos obligatorios
            if not data['estudiante'] or not data['asignatura']:
                QMessageBox.warning(self, "Error", "Debe seleccionar un estudiante y una asignatura")
                return
                
            nueva_nota = Nota(
                data['estudiante'],
                data['asignatura'],
                data['calificacion'],
                data['fecha'],
                data['peso'],
                data['descripcion']
            )
            
            # Editar nota existente
            indice = self.notes_tab.table.currentRow()
            if self.sistema.editar_nota(indice, nueva_nota):
                QMessageBox.information(self, "Éxito", "Nota actualizada correctamente")
                self.notes_tab.update_table()
                self.dashboard.update_stats()
            else:
                QMessageBox.warning(self, "Error", "No se pudo actualizar la nota")
    
    # Métodos de navegación
    def show_dashboard(self):
        self.central_widget.setCurrentIndex(0)
        self.dashboard.update_stats()
    
    def show_main_tabs(self):
        self.central_widget.setCurrentIndex(1)
        self.main_tabs.setCurrentIndex(0)  # Mostrar pestaña de estudiantes
    
    def show_main_tab(self, index):
        self.central_widget.setCurrentIndex(1)
        self.main_tabs.setCurrentIndex(index)
        
        # Actualizar la pestaña seleccionada
        if index == 0:  # Estudiantes
            self.students_tab.update_table()
        elif index == 1:  # Asignaturas
            self.subjects_tab.update_table()
        elif index == 2:  # Notas
            self.notes_tab.update_table()
        elif index == 3:  # Estadísticas
            self.stats_tab.update_student_combo()
            self.stats_tab.update_subject_combo()
            self.stats_tab.update_ranking()
            self.stats_tab.update_risk_students()
    
    # Métodos de importación/exportación
    def export_data(self):
        from PyQt5.QtWidgets import QFileDialog
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, 
            "Exportar Notas a CSV", 
            "notas_exportadas.csv", 
            "CSV Files (*.csv)", 
            options=options
        )
        
        if file_name:
            if not file_name.endswith('.csv'):
                file_name += '.csv'
            
            success = self.sistema.exportar_csv(file_name)
            if success:
                QMessageBox.information(self, "Éxito", f"Datos exportados correctamente a {file_name}")
                self.statusBar().showMessage(f"Datos exportados a {file_name}", 3000)
            else:
                QMessageBox.warning(self, "Error", "No se pudo exportar los datos")
    
    def import_data(self):
        from PyQt5.QtWidgets import QFileDialog
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self, 
            "Importar Notas desde CSV", 
            "", 
            "CSV Files (*.csv)", 
            options=options
        )
        
        if file_name:
            success, message = self.sistema.importar_csv(file_name)
            if success:
                QMessageBox.information(self, "Éxito", message)
                self.update_all_tables()
                self.dashboard.update_stats()
                self.statusBar().showMessage(message, 3000)
            else:
                QMessageBox.warning(self, "Error", message)
    
    def update_all_tables(self):
        """Actualiza todas las tablas del sistema"""
        self.students_tab.update_table()
        self.subjects_tab.update_table()
        self.notes_tab.update_table()
        self.stats_tab.update_student_combo()
        self.stats_tab.update_subject_combo()
        self.stats_tab.update_ranking()
        self.stats_tab.update_risk_students()
    
    def closeEvent(self, event):
        """Evento al cerrar la ventana"""
        self.sistema.guardar_datos()
        event.accept()