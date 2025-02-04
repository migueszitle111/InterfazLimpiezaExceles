from PySide6.QtWidgets import (QLabel, QWidget, QVBoxLayout, QHBoxLayout, QTableWidgetItem,
                               QHeaderView, QTableWidget, QPushButton)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QTimer, Signal
from datetime import datetime, timedelta
import pandas as pd
from DataBase.Conection import get_db_connection

from Estructura.TabsFrameContenido.Tab1Inicio import VibratingButton

class TabTableWidget(QWidget):
    dataFrameReady = Signal(pd.DataFrame)  # Define la señal que emite un DataFrame

    def __init__(self):
        super().__init__()
        self.current_date = datetime.now().date()  # Fecha actual por defecto
        self.setup_ui()
        self.setup_timer()

    def setup_ui(self):
        main_layout = QHBoxLayout()
        tabla_layout = QVBoxLayout()
        tabla_layout.setContentsMargins(0, 10, 0, 0)
        
        label_escaneados = QLabel("DOBLADO POR HORA", alignment=Qt.AlignmentFlag.AlignCenter)
        label_escaneados.setStyleSheet("""
        QLabel {
            font-family: "ADLaM Display";
            font-weight: bold; 
            font-size: 23px;  
            color: White;  
        }
        """)
        
        tabla_layout.addWidget(label_escaneados)
        
        self.table_widget = QTableWidget(20, 9)
        column_names = [
            "Part Number", "Job", "Unit", "Component", "Date Time", "User Name",
            "Nesting Qty", "Unfold Size", "Folio Text"
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

        self.label_fecha = QLabel(f"Fecha: {self.current_date.strftime('%Y-%m-%d')}")
        self.label_fecha.setFixedSize(280, 50)
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

        # Botones de navegación de fechas usando VibratingButton
        self.btn_prev_date = VibratingButton("<")
        self.btn_prev_date.setFixedSize(40, 60)
        self.btn_next_date = VibratingButton(">")
        self.btn_next_date.setFixedSize(40,60)

        date_layout = QHBoxLayout()
        date_layout.addWidget(self.btn_prev_date)
        date_layout.addWidget(self.label_fecha)
        date_layout.addWidget(self.btn_next_date)

        image_layout = QVBoxLayout()
        image_layout.setContentsMargins(0, 50, 0, 0)
        image_layout.addWidget(self.label_maquina)
        image_layout.addLayout(date_layout)
        image_layout.addWidget(self.label_ips)
        image_layout.addWidget(self.image_label)
        
        main_layout.addLayout(image_layout)
        main_layout.addLayout(tabla_layout)
        self.setLayout(main_layout)
        
        self.load_data_from_db()
        self.table_to_dataframe()

        self.btn_prev_date.clicked.connect(self.decrement_date)
        self.btn_next_date.clicked.connect(self.increment_date)

    def setup_timer(self):
        self.timer = QTimer()
        self.timer.setInterval(10000)  # 10 segundos de refresh
        self.timer.timeout.connect(self.load_data_from_db)
        self.timer.start()

    def convert_machine_name(self, name):
        # Reemplaza los espacios y el carácter '#' con un formato adecuado para la base de datos
        name = name.replace(" ", "_")  # Reemplaza espacios con guiones bajos
        name = name.split("#")[-1]  # Obtiene el último número después del '#'
        return f"DOBLADORA_{name}"

    def load_data_from_db(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Obtener el nombre de la máquina desde el texto de la etiqueta
            nombre_maquina = self.label_maquina.text().replace("Machine: ", "").strip()
            nombre_maquina_db = self.convert_machine_name(nombre_maquina)
            
            cursor.execute("""
                SELECT part_number, job, unit, component, date_time, user_name,
                       nesting_qty, unfold_size, folio_text
                FROM IPsDoblado_DB
                WHERE user_name = ?
            """, (nombre_maquina_db,))
            
            rows = cursor.fetchall()

            # Clear existing table content if any
            self.table_widget.setRowCount(0)
            
            # Set the row count and populate the table
            filtered_rows = [row for row in rows if row[4].date() == self.current_date]
            self.table_widget.setRowCount(len(filtered_rows))
            
            total_nesting_qty = 0  # Variable para almacenar la suma de NestingQty
            
            for row_idx, row_data in enumerate(filtered_rows):
                for col_idx, col_data in enumerate(row_data):
                    if col_idx == 4:  # Date Time column
                        if col_data:
                            hour = col_data.strftime('%I:%M:%S')
                            period = 'AM' if col_data.hour < 12 else 'PM'
                            if col_data.hour == 0:
                                hour = hour.replace('12', '12')
                            elif col_data.hour == 12:
                                hour = hour.replace('12', '12')
                            else:
                                hour = hour.replace(f'{col_data.hour % 12}', f'{col_data.hour % 12}')
                            formatted_time = f"{hour} {period}"
                        else:
                            formatted_time = ""
                        item = QTableWidgetItem(formatted_time)
                    else:
                        item = QTableWidgetItem(str(col_data))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.table_widget.setItem(row_idx, col_idx, item)

                # Sumar el valor de NestingQty
                nesting_qty = int(row_data[6]) if str(row_data[6]).isdigit() else 0
                total_nesting_qty += nesting_qty
            
            self.table_widget.resizeColumnsToContents()
            self.table_widget.resizeRowsToContents()
            
            header = self.table_widget.horizontalHeader()
            for col in range(header.count()):
                header.setSectionResizeMode(col, QHeaderView.ResizeToContents)
            
            # Actualizar la etiqueta IPS con la suma de NestingQty
            self.label_ips.setText(f"IPS: {self.table_widget.rowCount()}")
            
            cursor.close()
            conn.close()
            
            # Emitir la señal con el DataFrame
            df = self.table_to_dataframe()
            self.dataFrameReady.emit(df)
            
        except Exception as e:
            print(f"Error loading data from database: {e}")

    def table_to_dataframe(self):
        # Obtén el número de filas y columnas
        row_count = self.table_widget.rowCount()
        column_count = self.table_widget.columnCount()

        # Crear una lista de listas para almacenar los datos
        data = []
        for row in range(row_count):
            row_data = []
            for col in range(column_count):
                item = self.table_widget.item(row, col)
                row_data.append(item.text() if item else "")
            # Obtener el valor de NestingQty y duplicar la fila según ese valor
            nesting_qty = int(row_data[6]) if row_data[6].isdigit() else 1
            for _ in range(nesting_qty):
                data.append(row_data.copy())

        # Crear un DataFrame de pandas con los datos y las cabeceras
        column_names = [
            "Part Number", "Job", "Unit", "Component", "Date Time", "User Name",
            "Nesting Qty", "Unfold Size", "Folio Text"
        ]
        df = pd.DataFrame(data, columns=column_names)

        return df

    def decrement_date(self):
        self.current_date -= timedelta(days=1)
        self.label_fecha.setText(f"Fecha: {self.current_date.strftime('%Y-%m-%d')}")
        self.load_data_from_db()
        
    def actualizar_maquina(self, nombre_maquina):
        self.label_maquina.setText(f"Machine: {nombre_maquina}")
        image_path = f"Estructura/Images/{nombre_maquina.replace(' ', '')}.png"
        self.image_label.setPixmap(QPixmap(image_path).scaled(450, 250, Qt.KeepAspectRatio))

    def increment_date(self):
        self.current_date += timedelta(days=1)
        self.label_fecha.setText(f"Fecha: {self.current_date.strftime('%Y-%m-%d')}")
        self.load_data_from_db()
