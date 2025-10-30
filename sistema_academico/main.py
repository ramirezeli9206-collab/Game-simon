import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont

# Añade esta línea para asegurar que Python encuentre los módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from views.main_window import MainWindow
from utils.styles import setup_dark_theme

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    setup_dark_theme(app)
    
    font = QFont()
    font.setFamily("Arial")
    font.setPointSize(10)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()