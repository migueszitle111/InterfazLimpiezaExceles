from PySide6.QtWidgets import (QLabel, QWidget, QVBoxLayout, QHBoxLayout, QTableWidgetItem,
                               QHeaderView, QTableWidget)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QTimer
from datetime import datetime
from DataBase.Conection import get_db_connection
import pandas as pd


class TabTableHoraWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        main_layout = QHBoxLayout()
        tabla_layout = QVBoxLayout()
        tabla_layout.setContentsMargins(0, 10, 0, 0)
        
        
        
        label_escaneados = QLabel("DOBLADO POR OPERADOR", alignment=Qt.AlignmentFlag.AlignCenter)
        label_escaneados.setStyleSheet("""
        QLabel {
            font-family: "ADLaM Display";
            font-weight: bold; 
            font-size: 23px;  
            color: White;  
        }
        """)
        
        tabla_layout.addWidget(label_escaneados)
        
        self.table_widget = QTableWidget(20, 4)
        column_names = [
            "Operator", "Qty", "Objetivo", "Porcentaje"
        ]
        self.table_widget.setHorizontalHeaderLabels(column_names)
        tabla_layout.addWidget(self.table_widget)
        
        tabla_layout.setStretch(1, 1)
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        
        # Configurar la tabla para que no sea editable
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
       
        self.image_label = QLabel()
        self.image_label.setPixmap(QPixmap().scaled(500, 300, Qt.KeepAspectRatio))
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_maquina = QLabel("Machine: ")
        self.label_maquina.setFixedSize(380, 50)
        self.label_maquina.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_maquina.setStyleSheet("""
           QLabel {
                font-family: "ADLaM Display";
                font-weight: bold;
                font-size:18px;
                color: Black;
                background-color:white;
                border-radius: 3px;
            }
        """)

        self.label_fecha = QLabel(f"Fecha: {datetime.now().strftime('%Y-%m-%d')}")
        self.label_fecha.setFixedSize(380, 50)
        self.label_fecha.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_fecha.setStyleSheet("""
           QLabel {
                font-family: "ADLaM Display";
                font-weight: bold;
                font-size:18px;
                color: Black;
                background-color:white;
                border-radius: 3px;
            }
        """)

        self.label_ips = QLabel("IPS: 0")
        self.label_ips.setFixedSize(380, 50)
        self.label_ips.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_ips.setStyleSheet("""
           QLabel {
                font-family: "ADLaM Display";
                font-weight: bold;
                font-size:18px;
                color: Black;
                background-color:white;
                border-radius: 3px;
            }
        """)
        
        image_layout = QVBoxLayout()
        image_layout.setContentsMargins(0, 50, 0, 0)
        image_layout.addWidget(self.label_maquina)
        image_layout.addWidget(self.label_fecha)
        image_layout.addWidget(self.label_ips)
        image_layout.addWidget(self.image_label)
        
        main_layout.addLayout(image_layout)
        main_layout.addLayout(tabla_layout)
        self.setLayout(main_layout)
        
    def load_data_from_db(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT Operator, Qty, Objetivo, Hora, Porcentaje
                FROM Operators
            """)
            
            rows = cursor.fetchall()
            
            # Clear existing table content if any
            self.table_widget.setRowCount(0)
            
            # Update table with new data
            for row_data in rows:
                row_number = self.table_widget.rowCount()
                self.table_widget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.table_widget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                    
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"Error loading data from database: {e}")
                    
    def actualizar_maquina(self, nombre_maquina):
        self.label_maquina.setText(f"Machine: {nombre_maquina}")
        image_path = f"Estructura/Images/{nombre_maquina.replace(' ', '')}.png"
        self.image_label.setPixmap(QPixmap(image_path).scaled(450, 250, Qt.KeepAspectRatio))
