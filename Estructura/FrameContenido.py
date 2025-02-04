from PySide6.QtWidgets import QSizePolicy, QVBoxLayout, QTabWidget

from Estructura.TabsFrameContenido.Tab1Inicio import contenido_tab_inicio


def configurar_frame2(self):
    # Crear el QTabWid
    self.TabMenu = QTabWidget()
    self.TabMenu.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Ignored)

    # Crear los widgets de las pestañas
    tab_inicio = contenido_tab_inicio(self)
   

    # Agregar las pestañas al QTabWidget
    self.TabMenu.addTab(tab_inicio, "")
    

    # Crear un layout para frame2
    self.layout_frame2 = QVBoxLayout()

    # Agregar el QTabWidget al layout
    self.layout_frame2.addWidget(self.TabMenu)

    # Establecer el layout en frame2
    self.frame2.setLayout(self.layout_frame2)
    
    self.frame2.setStyleSheet("""
        QFrame {
        }
    """)