import os
import sys
from PySide6.QtWidgets import (QPushButton,
                               QLabel,QGridLayout,
                               QWidget,QVBoxLayout,QHBoxLayout)
from PySide6.QtCore import Qt, QSize

# Obtener la ruta base del directorio donde se encuentra el ejecutable
def resource_path(relative_path):
    # Si se ejecuta en un entorno empaquetado, buscar en sys._MEIPASS
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
   
def configurar_frame1(self):
        # Crear la etiqueta y configurar su fuente y alineación
        self.etiqueta = QLabel("MANUFACTURA")
        self.etiqueta.setAlignment(Qt.AlignmentFlag.AlignCenter )
         # Aplicar estilo en línea para sobrescribir el tema
        self.etiqueta.setStyleSheet("""
        QLabel {
            font-family: "Javanese Text";
            font-weight: bold; 
            font-size: 40px;  
            color: orange; 
        }
    """)
        # Crear un widget contenedor para la etiqueta
        self.widget_etiqueta = QWidget()
        self.widget_etiqueta.setAttribute(Qt.WA_TranslucentBackground)
        self.layout_etiqueta = QVBoxLayout(self.widget_etiqueta)
        self.layout_etiqueta.addWidget(self.etiqueta, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Crear los botones de la ventana
        self.boton_minimizar = QPushButton("-", self)
        self.boton_minimizar.setStyleSheet("""
          QPushButton {
                     min-width: 60px; 
        }
    """)
        self.boton_minimizar.clicked.connect(self.showMinimized)
        self.boton_pantalla_completa = QPushButton("[ ]", self)
        self.boton_pantalla_completa.setStyleSheet("""
          QPushButton {
                     min-width: 60px; 
        }
    """)
        self.boton_pantalla_completa.clicked.connect(self.toggle_full_screen)
        self.boton_cerrar = QPushButton("X", self)
        self.boton_cerrar.setStyleSheet("""
          QPushButton {
                     min-width: 60px; 
        }
    """)
        self.boton_cerrar.clicked.connect(self.close)
        # Configurar el tamaño de los botones
        button_size = QSize(50, 25)
        self.boton_minimizar.setFixedSize(button_size)
        self.boton_pantalla_completa.setFixedSize(button_size)
        self.boton_cerrar.setFixedSize(button_size)
        
        # Crear un layout horizontal y agregar los botones
        self.botones_frame1 = QHBoxLayout()
        self.botones_frame1.addWidget(self.boton_minimizar)
        self.botones_frame1.addWidget(self.boton_pantalla_completa)
        self.botones_frame1.addWidget(self.boton_cerrar)
        
        # Crear un widget contenedor para los botones y establecer el layout
        self.botones_widget = QWidget()
        #transparencia del widget
        self.botones_widget.setAttribute(Qt.WA_TranslucentBackground)
        self.botones_widget.setLayout(self.botones_frame1)
    
        # Crear un layout para frame1
        self.layout_frame1 = QGridLayout()
        # Agregar el widget de botones en la parte superior derecha
        self.layout_frame1.addWidget(self.botones_widget, 0, 1, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        # Agregar el widget contenedor de la etiqueta en el centro del layout
        self.layout_frame1.addWidget(self.widget_etiqueta, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)    
        # Establecer el layout en frame1
        self.frame1.setLayout(self.layout_frame1)

        
            # Obtener la ruta de la imagen
        imagen_ruta = os.path.normpath(resource_path('Images/vertiv2.png')).replace("\\", "/")
    
        # Aplicar hoja de estilo para la imagen de fondo
        self.frame1.setStyleSheet(f"""
            QFrame {{
                background-image: url({imagen_ruta});
                background-position: center;
                background-repeat: no-repeat;
            }}
        """)
        
    
        
