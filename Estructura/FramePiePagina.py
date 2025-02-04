import sys
import os

# Obtener la ruta base del directorio donde se encuentra el ejecutable
def resource_path(relative_path):
    # Si se ejecuta en un entorno empaquetado, buscar en sys._MEIPASS
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def configurar_frame3(self):
        # Obtener la ruta de la imagen
    imagen_ruta = os.path.normpath(resource_path('Images/vertiv2.png')).replace("\\", "/")
    # Aplicar hoja de estilo para la imagen de fondo
    self.frame3.setStyleSheet(f"""
        QFrame {{
            background-image: url({imagen_ruta});
            background-position: center;
            background-repeat: no-repeat;
            background-size: cover;
        }}
    """)
    