from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

def setup_dark_theme(app):
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
    
    app.setPalette(palette)
    app.setStyleSheet("""
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