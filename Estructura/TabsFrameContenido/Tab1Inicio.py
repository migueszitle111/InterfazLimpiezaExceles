import sys
import pandas as pd
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QFileDialog, QApplication, QMessageBox, QProgressBar)
from PySide6.QtCore import Qt, QThread, Signal

class ExcelProcessor(QThread):
    progress = Signal(int)  # Señal para actualizar el progreso
    finished = Signal(str)  # Señal para indicar la finalización del procesamiento

    def __init__(self, archivo_excel):
        super().__init__()
        self.archivo_excel = archivo_excel

    def run(self):
        
            # Cargar el archivo Excel
            df = pd.read_excel(self.archivo_excel)

            # Procesar y limpiar los datos
            total_filas = len(df)
            for i, _ in enumerate(df['Item']):
                # Verificar si los valores son cadenas y eliminar espacios o guiones al inicio
                df.at[i, 'Item'] = df.at[i, 'Item'].lstrip(' -') if isinstance(df.at[i, 'Item'], str) else df.at[i, 'Item']
                # Emitir la señal de progreso
                progreso = int((i + 1) / total_filas * 100)
                self.progress.emit(progreso)

            # Guardar el archivo actualizado
            archivo_guardado = self.archivo_excel.replace('.xlsx', '-Copy.xlsx')
            df.to_excel(archivo_guardado, index=False)

            # Emitir la señal de finalización con la ruta del archivo guardado
            self.finished.emit(archivo_guardado)
       

class ExampleWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Crear el layout, el botón y la barra de progreso
        layout = QVBoxLayout()
        self.btn_cargar_excel = QPushButton("CARGAR EXCEL")
        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setValue(0)  # Iniciar con la barra en 0%

        # Estilo del botón
        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #5A5A5A, stop: 1 #3A3A3A);
                border-radius: 5px;
                font-family: "Javanese Text";
                font-size: 20px;
                color: white;
            }
            QPushButton:hover {
                background-color: orange;
                color: black;
            }
        """)

        # Conectar la señal del botón
        self.btn_cargar_excel.clicked.connect(self.cargar_y_limpiar_excel)

        # Añadir widgets al layout
        layout.addWidget(self.btn_cargar_excel)
        layout.addWidget(self.progress_bar)

        # Configurar el layout para el widget
        self.setLayout(layout)

    def cargar_y_limpiar_excel(self):
        # Abrir un cuadro de diálogo para seleccionar el archivo Excel
        archivo_excel, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo Excel", "", "Archivos Excel (*.xlsx *.xls)")

        if archivo_excel:
            # Iniciar el procesamiento en un hilo separado
            self.processor = ExcelProcessor(archivo_excel)
            self.processor.progress.connect(self.actualizar_progreso)
            self.processor.finished.connect(self.procesamiento_terminado)
            self.processor.start()

    def actualizar_progreso(self, progreso):
        # Actualizar el valor de la barra de progreso
        self.progress_bar.setValue(progreso)

    def procesamiento_terminado(self, resultado):
        # Mostrar un mensaje de finalización o error
        if resultado.startswith("Error"):
            QMessageBox.critical(self, "Error", resultado)
        else:
            QMessageBox.information(self, "Éxito", f"El archivo ha sido guardado como: {resultado}")
        # Restablecer la barra de progreso
        self.progress_bar.setValue(0)
        
        

def contenido_tab_inicio(self):
    self.tab_inicio = ExampleWidget()
    return self.tab_inicio
