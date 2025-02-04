from PySide6.QtCharts import (QBarCategoryAxis, QBarSeries, QBarSet, QChart,
                              QChartView, QValueAxis, QPieSeries)
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel)
from PySide6.QtGui import QPainter, QPen, QColor, QPixmap
from PySide6.QtCore import Qt

class TabHoraWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()
    
    def setupUi(self):
        self.tab_charts_hbox = QHBoxLayout()
        self.tab_charts_hbox.setContentsMargins(0, 20, 0, 0)
        
        # Crear widgets de gráficos
        self.bar_chart_widget = self.BarChartWidget()
        #self.pie_chart_widget = self.PieChartWidget()
      
        # Crear el QLabel para la imagen
        self.image_label = QLabel()
        self.image_label.setPixmap(QPixmap().scaled(500, 300, Qt.KeepAspectRatio))
        
        self.tab_charts_hbox.addWidget(self.image_label)
        self.tab_charts_hbox.addWidget(self.bar_chart_widget)
        #self.tab_charts_hbox.addWidget(self.pie_chart_widget)
        
        self.setLayout(self.tab_charts_hbox)
    
    def actualizar_maquina(self, nombre_maquina):
        image_path = f"Estructura/Images/{nombre_maquina.replace(' ', '')}.png"
        self.image_label.setPixmap(QPixmap(image_path).scaled(490, 290, Qt.KeepAspectRatio))

    class BarChartWidget(QWidget):
        def __init__(self):
            super().__init__()
            self.setupUi()

        def setupUi(self):
            # Crear un conjunto de datos de barras para todos los meses
            self.bar_set = QBarSet("Escaneos por semana")

            # Rellenar el conjunto de datos con valores para cada mes
            # Aquí puedes añadir los valores que tienes para cada mes.
            # Por ejemplo, estos son valores de muestra.
            self.bar_set.append([100, 150, 120, 180, 130])
            self.bar_set.setColor(QColor("red"))

            # Crear la serie de barras y agregar el conjunto de datos
            self.series = QBarSeries()
            self.series.append(self.bar_set)

            # Crear el gráfico y configurar opciones
            self.chart = QChart()
            self.chart.addSeries(self.series)
            self.chart.setTitle("Escaneos por semana")
            self.chart.setAnimationOptions(QChart.SeriesAnimations)

            # Configurar el eje X (categorías)
            self.categories = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
            self.axis_x = QBarCategoryAxis()
            self.axis_x.append(self.categories)
            self.chart.addAxis(self.axis_x, Qt.AlignBottom)
            self.series.attachAxis(self.axis_x)

            # Configurar el eje Y (valores)
            self.axis_y = QValueAxis()
            self.axis_y.setRange(0, 400)  # Ajusta el rango según tus datos
            self.chart.addAxis(self.axis_y, Qt.AlignLeft)
            self.series.attachAxis(self.axis_y)

            # Crear la vista del gráfico y configurar opciones
            self.chart_view = QChartView(self.chart)
            self.chart_view.setRenderHint(QPainter.Antialiasing)

            # Configurar el diseño del widget
            layout = QVBoxLayout()
            layout.addWidget(self.chart_view)
            self.setLayout(layout)

    class PieChartWidget(QWidget):
        def __init__(self):
            super().__init__()
            self.setupUi()

        def setupUi(self):
            self.series = QPieSeries()

            self.series.append('Jane', 1)
            self.series.append('Joe', 2)
            self.series.append('Andy', 3)
            self.series.append('Barbara', 4)
            self.series.append('Axel', 5)

            self.slice = self.series.slices()[1]
            self.slice.setExploded()
            self.slice.setLabelVisible()
            self.slice.setPen(QPen(Qt.darkGreen, 2))
            self.slice.setBrush(Qt.green)

            self.chart = QChart()
            self.chart.addSeries(self.series)
            self.chart.setTitle('Simple piechart example')
            self.chart.setAnimationOptions(QChart.SeriesAnimations)
            self.chart.legend().hide()

            self._chart_view = QChartView(self.chart)
            self._chart_view.setRenderHint(QPainter.Antialiasing)

            layout = QVBoxLayout()
            layout.addWidget(self._chart_view)  
            self.setLayout(layout)

