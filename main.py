import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QFrame, QWidget, QStyleFactory)
from PySide6.QtGui import QIcon, QCursor, QMouseEvent
from PySide6.QtCore import QSize, Qt, QPoint, QRect

from Estructura.FrameEncabezado import *
from Estructura.FrameContenido import *
from Estructura.FramePiePagina import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PROGRAMA PRUEBA")
        self.resize(QSize(950, 640))
        self.setWindowIcon(QIcon("Estructura/Images/vertiv.ico"))
        self.setFusionStyle()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint | Qt.WindowTitleHint)

        self.raiz = QVBoxLayout()
        self.frame1 = QFrame()
        self.frame2 = QFrame()
        self.frame3 = QFrame()

        self.raiz.addWidget(self.frame1, 20)
        self.raiz.addWidget(self.frame2, 40)
        self.raiz.addWidget(self.frame3, 20)

        self.widget = QWidget()
        self.widget.setLayout(self.raiz)

        self.setCentralWidget(self.widget)
        configurar_frame1(self)
        configurar_frame2(self)
        configurar_frame3(self)

        # Variables para el movimiento y redimensionamiento
        self._is_moving = False
        self._move_start_pos = QPoint()
        self._resizing = False
        self._resize_start_pos = QPoint()
        self._resize_start_size = QSize()
        self._resize_margin = 10  # Margen para el redimensionamiento

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            if self._is_in_resize_zone(event.position().toPoint()):
                self._resizing = True
                self._resize_start_pos = event.globalPosition().toPoint()
                self._resize_start_size = self.size()
            else:
                self._is_moving = True
                self._move_start_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._is_moving:
            delta = event.globalPosition().toPoint() - self._move_start_pos
            self.move(self.pos() + delta)
            self._move_start_pos = event.globalPosition().toPoint()
        elif self._resizing:
            delta = event.globalPosition().toPoint() - self._resize_start_pos
            new_size = self._resize_start_size + QSize(delta.x(), delta.y())
            self.resize(new_size)
        else:
            cursor = Qt.ArrowCursor
            if self._is_in_resize_zone(event.position().toPoint()):
                cursor = Qt.SizeFDiagCursor
            self.setCursor(QCursor(cursor))

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            if self._resizing:
                self._resizing = False
            elif self._is_moving:
                self._is_moving = False

    def _is_in_resize_zone(self, pos: QPoint) -> bool:
        rect = QRect(self.width() - self._resize_margin, self.height() - self._resize_margin, 
                     self._resize_margin, self._resize_margin)
        return rect.contains(pos)

    def minimizar(self):
        self.showMinimized()

    def toggle_full_screen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def cerrar(self):
        self.close()

    def setFusionStyle(self):
        QApplication.setStyle(QStyleFactory.create("Fusion"))

        dark_palette = """
            QWidget {
                background-color: #2B2B2B;
                color: white;
            }
            QTabWidget::pane {
                background-color: #353535;
            }
            QTabBar::tab {
                background: #4A4A4A;
                border: 1px solid #2B2B2B;
                padding:5px 10px;
                color: #2B2B2B;
                font-size: 10px; 
                font-weight: bold; 
                text-align: center;
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #5A5A5A, stop: 1 #3A3A3A);
                min-width: 120px;
            }
            QTabBar::tab:selected {
                background: #2B2B2B;
                color: #2B2B2B;
            }
            QTabBar::tab:hover {
                background: #2B2B2B;
                color: #2B2B2B;
            }
            QHeaderView::section {
                background-color: #4A4A4A;
                color: #FFFFFF;
                padding: 4px;
                border: 1px solid #1A1A1A;
            }
            QTableWidget {
                border: 1px solid #353535;
                font-weight: bold; 
                border-radius: 20px;
            }
            QTableWidget::item {
                border-right: 1px solid transparent;
                border-bottom: 1px solid transparent;
            }
            QTableWidget QHeaderView::section {
                border: 1px solid #353535;
                font-weight: bold;
            }
            QTextEdit {
                background-color: #3C3C3C;
                color: #FFFFFF;
                border: 1px solid #4A4A4A;
            }
            QPushButton {
                background-color: #4A4A4A;
                color: #FFFFFF;
                border: 1px solid #4A4A4A;
                border-radius: 2px;
                padding: 5px 10px;
                font-size: 10px; 
                font-weight: bold; 
                text-align: center;
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #5A5A5A, stop: 1 #3A3A3A);
            }
            QPushButton:hover {
                background-color: #FBFF00;
                color: #000000;
                border: 1px solid #0078D7;
            }
            QLabel {
                background-color: transparent;
            }
            QLineEdit {
                background-color: #FFFFFF;
                color: #000000;
            }
            QComboBox {
                background-color: #FFFFFF;
                color: #000000;
            }
            QComboBox QAbstractItemView {
                background-color: #FFFFFF;
                color: #000000;
            }
            QTableWidget {
                background-color: #FFFFFF;
                color: #000000;
            }
            QTableWidget::item:selected {
                background-color: orange;
                color: black;
            }
        """
        self.setStyleSheet(dark_palette)

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
