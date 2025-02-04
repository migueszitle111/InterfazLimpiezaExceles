import json
from PySide6.QtCharts import (QBarCategoryAxis, QBarSeries, QBarSet, QChart,
                              QChartView, QValueAxis, QLineSeries, QScatterSeries)
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QGraphicsSimpleTextItem, QInputDialog)
from PySide6.QtGui import QPainter, QPen, QColor, QPixmap, QFont
from PySide6.QtCore import Qt, QPointF, QTimer, Signal, Slot
from datetime import datetime
import pandas as pd
import locale

# Configurar la localización en español
locale.setlocale(locale.LC_TIME, 'es_ES')

class TabHoraWidget(QWidget):
    pointEdited = Signal(int, float)  # Señal que indica que un punto ha sido editado

    def __init__(self, parent=None):
        super().__init__(parent)
        self.line_data = self.load_line_data()  # Cargar datos de línea desde el archivo JSON
        self.setupUi()

    def setupUi(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 10, 0, 0) 

        # Crear el QLabel para la imagen
        self.image_label = QLabel()
        self.image_label.setPixmap(QPixmap().scaled(500, 300, Qt.KeepAspectRatio))

        # Crear el gráfico combinado
        self.chart = QChart()

        # Configuración del gráfico de barras
        self.bar_set = QBarSet("IPs Por Hora")
        self.bar_series = QBarSeries()
        self.bar_series.append(self.bar_set)
        self.bar_series.setLabelsVisible(True)

        # Configuración del gráfico de líneas
        self.line_series = QLineSeries()
        self.line_series.setName("Estandar por hora")  # Agregar nombre a la serie de líneas
        for i, value in enumerate(self.line_data):
            self.line_series.append(i, value)
        self.line_series.setPen(QPen(Qt.blue, 4))

        # Configuración del gráfico de dispersión
        self.scatter_series = QScatterSeries()
        self.scatter_series.setName("Meta")  # Agregar nombre a la serie de líneas
        self.scatter_series.setMarkerSize(10)
        self.scatter_series.setColor(QColor("red"))

        # Añadir eventos de clic a la serie de dispersión
        self.scatter_series.clicked.connect(self.on_scatter_clicked)

        current_date = datetime.now().strftime('%A, %d de %B de %Y')  # Formato de fecha en letra y en español
        self.chart.setTitle(f"Escaneos por semana - Fecha: {current_date}")

        # Añadir series al gráfico
        self.chart.addSeries(self.bar_series)
        self.chart.addSeries(self.line_series)
        self.chart.addSeries(self.scatter_series)

        # Configuración de los ejes
        self.axis_x = QBarCategoryAxis()
        self.categories = ["6:00am-7:00am", "7:00am-8:00am", "8:00am-9:00am", "9:00am-10:00am", "10:00am-11:00am", 
                           "11:00am-12:00am", "12:00am-1:00pm", "1:00pm-2:00pm", "2:00pm-3:00pm", "3:00pm-4:00pm", 
                           "4:00pm-5:00pm", "5:00pm-6:00pm", "6:00pm-7:00pm", "7:00pm-8:00pm", "8:00pm-9:00pm", 
                           "9:00pm-10:00pm", "10:00pm-10:30pm"]
        self.axis_x.append(self.categories)
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.bar_series.attachAxis(self.axis_x)
        self.line_series.attachAxis(self.axis_x)
        self.scatter_series.attachAxis(self.axis_x)

        self.axis_y = QValueAxis()
        self.axis_y.setRange(0, max(self.line_data) + 10)  # Inicializar con un rango mayor para la visibilidad
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.bar_series.attachAxis(self.axis_y)
        self.line_series.attachAxis(self.axis_y)
        self.scatter_series.attachAxis(self.axis_y)

        # Configuración del título del gráfico
        self.chart.setTitle("Gráfico Combinado")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_font.setFamily("Javanese Text")
        self.chart.setTitleFont(title_font)
        self.chart.setAnimationOptions(QChart.SeriesAnimations)

        # Crear el QChartView y añadirlo al layout
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view.setRenderHint(QPainter.SmoothPixmapTransform)
        self.chart_view.setMinimumSize(800, 400)

        self.layout.addWidget(self.chart_view)

        # Ajustar el tamaño de las etiquetas para mejorar la visibilidad
        font = QFont()
        font.setPointSize(7.5)  # Ajusta el tamaño de la fuente según tus necesidades
        font.setBold(True)    # Configura el texto en negrita
        self.axis_x.setLabelsFont(font)
        self.axis_x.setLabelsAngle(-45)

        # Datos iniciales para el gráfico de líneas
        self.data = [(i, value) for i, value in enumerate(self.line_data)]
        self.index = 0
        self.labels = {}

        # Configurar el temporizador para la animación del gráfico de líneas
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_chart)
        self.timer.start(600)

        # Conectar el redimensionamiento del gráfico a un método
        self.chart_view.chart().resizeEvent = self.on_resize

    def on_resize(self, event):
        self.update_labels()

    def update_chart(self):
        if self.index < len(self.data):
            point = self.data[self.index]
            self.scatter_series.append(QPointF(point[0], point[1]))

            # Actualizar etiquetas
            self.update_labels()

            self.index += 1
        else:
            # Asegurarse de que la última etiqueta se añada
            self.update_labels()
            self.timer.stop()

    def update_labels(self):
        # Limpiar etiquetas anteriores
        for label in self.labels.values():
            self.chart.scene().removeItem(label)
        self.labels.clear()

        for point in self.scatter_series.points():
            x, y = int(point.x()), point.y()
            position = self.chart.mapToPosition(QPointF(x, y))
            label = QGraphicsSimpleTextItem(f"{y}")
            label.setBrush(Qt.black)
            label.setFont(QFont("Arial", 13))
            label.setPos(position + QPointF(2, -15))  # Ajustar posición de la etiqueta
            self.chart.scene().addItem(label)
            self.labels[(x, y)] = label

    def on_scatter_clicked(self, point):
        x = int(point.x())
        y = point.y()
        
        # Solicitar al usuario el nuevo valor para el punto
        new_value, ok = QInputDialog.getDouble(self, "Editar valor", f"Nuevo valor para el punto {x}:", y)
        
        if ok:
            self.scatter_series.remove(point)
            self.scatter_series.append(QPointF(x, new_value))
            
            # Actualizar el gráfico de líneas
            for i, p in enumerate(self.line_series.points()):
                if int(p.x()) == x:
                    self.line_series.replace(p, QPointF(x, new_value))
                    self.line_data[x] = new_value  # Actualizar la lista de datos de línea
                    break

            # Guardar los datos actualizados en el archivo JSON
            self.save_line_data()

            # Actualizar las etiquetas
            self.update_labels()
            
            # Actualizar el eje Y
            self.update_y_axis(new_value)

    def update_y_axis(self, new_value):
        # Actualizar el rango del eje Y para incluir el nuevo valor
        max_y = max(self.line_data + [new_value]) + 30  # Añadir un margen para la visibilidad
        self.axis_y.setRange(0, max_y)

    def actualizar_maquina(self, nombre_maquina):
        current_date = datetime.now().strftime('%A, %d de %B de %Y')  # Formato de fecha en letra y en español
        self.chart.setTitle(f"IPs Procesadas Por Hora Para La Maquina: {nombre_maquina} - Fecha: {current_date}")
        # Actualiza los datos del conjunto de barras
        self.procesar_dataframe()

    def procesar_dataframe(self):
        # Definir los rangos horarios
        rangos_horarios = {
            "6:00am-7:00am": (6, 7),
            "7:00am-8:00am": (7, 8),
            "8:00am-9:00am": (8, 9),
            "9:00am-10:00am": (9, 10),
            "10:00am-11:00am": (10, 11),
            "11:00am-12:00am": (11, 12),
            "12:00am-1:00pm": (12, 13),
            "1:00pm-2:00pm": (13, 14),
            "2:00pm-3:00pm": (14, 15),
            "3:00pm-4:00pm": (15, 16),
            "4:00pm-5:00pm": (16, 17),
            "5:00pm-6:00pm": (17, 18),
            "6:00pm-7:00pm": (18, 19),
            "7:00pm-8:00pm": (19, 20),
            "8:00pm-9:00pm": (20, 21),
            "9:00pm-10:00pm": (21, 22),
            "10:00pm-10:30pm": (22, 23)
        }

        # Convertir la columna de fecha y hora al formato de datetime
        self.dataframe['Date Time'] = pd.to_datetime(self.dataframe['Date Time'])
        grouped_df = self.dataframe.groupby(['Part Number','Job','Unit','Component']).size().reset_index(name='Count')
        print(self.dataframe)

        # Extraer la hora en formato de 24 horas
        self.dataframe['Date Time'] = self.dataframe['Date Time'].dt.hour + self.dataframe['Date Time'].dt.minute / 60

        # Agrupar por renglones iguales y sumar las cantidades
        #grouped_df = self.dataframe.groupby(['Hour']).size().reset_index(name='Count')

        # Contar filas en cada rango horario
        conteo_por_rango = {rango: 0 for rango in rangos_horarios}
        for _, row in grouped_df.iterrows():
            for rango, (hora_inicio, hora_fin) in rangos_horarios.items():
                if hora_inicio <= row['Date Time'] < hora_fin:
                    conteo_por_rango[rango] += row['Count']
                    break

        # Imprimir los conteos
        print("Conteo de filas por rango horario:")
        for rango, conteo in conteo_por_rango.items():
            print(f"{rango}: {conteo} Ips")

        # Actualizar el gráfico de barras
        self.bar_series.remove(self.bar_set)  # Eliminar el QBarSet actual
        self.bar_set = QBarSet("IPs Por Hora")  # Crear un nuevo QBarSet
        self.bar_set.append(list(conteo_por_rango.values()))  # Añadir los datos actualizados
        self.bar_set.setColor(QColor("DarkOrange"))

        self.bar_series.append(self.bar_set)  # Añadir el nuevo QBarSet a la serie


    def handle_data_frame_ready(self, dataframe: pd.DataFrame):
        # Almacenar el DataFrame para uso posterior
        self.dataframe = dataframe
        self.procesar_dataframe()

    def save_line_data(self):
        # Guardar la lista de datos en un archivo JSON
        with open('line_data.json', 'w') as file:
            json.dump(self.line_data, file)

    def load_line_data(self):
        # Cargar la lista de datos desde un archivo JSON, si existe
        try:
            with open('line_data.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
