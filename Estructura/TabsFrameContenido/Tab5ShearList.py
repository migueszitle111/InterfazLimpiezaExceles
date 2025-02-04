import sys
from PySide6.QtCharts import (QBarCategoryAxis, QBarSeries, QBarSet, QChart,
                              QChartView, QValueAxis, QPieSeries)
from PySide6.QtWidgets import (QApplication, QMainWindow,QPushButton,
                               QLabel,QStyleFactory,QGridLayout,
                               QWidget,QSizePolicy,QVBoxLayout,QFrame,QHBoxLayout,QTabWidget,
                               QHeaderView,QTableWidget,QTextEdit, QComboBox,QLineEdit,QFileDialog, QMessageBox,QTableWidgetItem)
from PySide6.QtGui import QPainter, QPen, QIcon,QColor
from PySide6.QtCore import Qt, QSize
from pathlib import Path
import pandas as pd 
import pyarrow as pa


def contenido_busqueda_shearList(self):
        self.tab_shearlist = QWidget()
        # Crear etiquetas y elementos existentes
        self.label_Job = QLabel("JOB: ", alignment=Qt.AlignmentFlag.AlignCenter)
        self.label_Job.setStyleSheet("""
            QLabel {
                font-family: "Javanese Text";
                font-size: 18px; 
                color: Yellow;  
                margin-top: 6px;
            }
        """)
    
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Ingrese un job")
        
        self.label_Tag = QLabel("TAG: ", alignment=Qt.AlignmentFlag.AlignCenter)
        self.label_Tag.setStyleSheet("""
            QLabel {
                font-family: "Javanese Text";
                font-size: 18px; 
                color: Yellow;  
                margin-top: 6px;
            }
        """)
        
        self.combo_box = QComboBox()
        self.combo_box.addItems(["", "Opción 1", "Opción 2"])
        
        self.button1 = QPushButton("Cargar Shear List")
       # self.button1.clicked.connect(self.cargarshearlist)
        self.button2 = QPushButton("Buscar")
        self.button3 = QPushButton("Eliminar")
        self.button4 = QPushButton("Excel")
        
        # Crear layout horizontal para organizar elementos
        self.shearlist_layout = QHBoxLayout()
        self.shearlist_layout.addWidget(self.label_Job)
        self.shearlist_layout.addWidget(self.line_edit)
        self.shearlist_layout.addWidget(self.label_Tag)
        self.shearlist_layout.addWidget(self.combo_box)
        self.shearlist_layout.addWidget(self.button1)
        self.shearlist_layout.addWidget(self.button2)
        self.shearlist_layout.addWidget(self.button3)
        self.shearlist_layout.addWidget(self.button4)
        self.shearlist_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Crear un layout principal vertical
        self.layout_principal_shearlist = QVBoxLayout()
        self.layout_principal_shearlist.addLayout(self.shearlist_layout)
        
        # Crear la tabla debajo de los elementos existentes
        self.table_widget_shearlist = QTableWidget()
        self.table_widget_shearlist.setColumnCount(20)
        self.table_widget_shearlist.setRowCount(20)
        
        # Configurar el ajuste de las secciones de la tabla
        self.table_widget_shearlist.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget_shearlist.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Añadir la tabla al layout principal
        self.layout_principal_shearlist.addWidget(self.table_widget_shearlist)
        
        # Establecer el layout principal en el widget de la pestaña "Shear List"
        self.tab_shearlist.setLayout(self.layout_principal_shearlist)
        
        return self.tab_shearlist
    
      