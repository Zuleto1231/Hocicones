import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QStackedWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer
from VentanaPrincipal import VentanaPrincipal  # Asegúrate de que esté en el mismo directorio
from VentanaAdmin import VentanaAdmin

class VentanaLogin(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("SVH - Gestor de Ventas de Hocicones")
        self.setGeometry(100, 100, 800, 600)  # Tamaño ajustado a 800x600
        
        layout = QVBoxLayout()
        
        # Mensaje de bienvenida
        self.label_bienvenida = QLabel("¡Bienvenido al Gestor de Ventas de Hocicones!")
        self.label_bienvenida.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_bienvenida.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(self.label_bienvenida)
        
        # Carrusel de imágenes
        self.carrusel = QStackedWidget(self)
        import os
        ruta_base = os.path.dirname(os.path.abspath(__file__))
        self.imagenes = [os.path.join(ruta_base, "imagenes", f"imagen{i}.jpg") for i in range(1, 7)]  # Agrega las rutas de tus imágenes
        self.pixmaps = []
        for img in self.imagenes:
            pixmap = QPixmap(img)
            if pixmap.isNull():
                print(f"⚠️ No se pudo cargar la imagen: {img}")
            else:
                self.pixmaps.append(pixmap)
        
        for pixmap in self.pixmaps:
            label = QLabel(self)
            label.setPixmap(pixmap.scaled(600, 250, Qt.AspectRatioMode.KeepAspectRatio))
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.carrusel.addWidget(label) 
            if pixmap.isNull():
                print(f"⚠️ No se pudo cargar la imagen: {img}")
            else:
                label.setPixmap(pixmap.scaled(600, 250, Qt.AspectRatioMode.KeepAspectRatio))
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.carrusel.addWidget(label)
        
        layout.addWidget(self.carrusel)
        self.indice_imagen = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.cambiar_imagen)
        self.timer.start(400)  # Cambia la imagen cada 3 segundos
        
        # Campo de usuario
        self.label_usuario = QLabel("Usuario:")
        layout.addWidget(self.label_usuario)
        self.input_usuario = QLineEdit(self)
        self.input_usuario.setPlaceholderText("Ingrese su usuario")
        layout.addWidget(self.input_usuario)
        
        # Campo de contraseña
        self.label_contrasena = QLabel("Contraseña:")
        layout.addWidget(self.label_contrasena)
        self.input_contrasena = QLineEdit(self)
        self.input_contrasena.setPlaceholderText("Ingrese su contraseña")
        self.input_contrasena.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.input_contrasena)
        
        # Botón de login
        self.btn_login = QPushButton("Iniciar sesión", self)
        self.btn_login.clicked.connect(self.iniciar_sesion)
        layout.addWidget(self.btn_login)
        
        self.setLayout(layout)
    
    def cambiar_imagen(self):
        """Cambia la imagen del carrusel automáticamente."""
        self.indice_imagen = (self.indice_imagen + 1) % len(self.imagenes)
        self.carrusel.setCurrentIndex(self.indice_imagen)
    
    def iniciar_sesion(self):
        """Verifica las credenciales y abre la ventana principal si son correctas."""
        usuario = self.input_usuario.text()
        contrasena = self.input_contrasena.text()
        
        if usuario == "caja" and contrasena == "1234":  # Esto es solo un ejemplo
            self.accept_login()
        elif usuario == "admin" and contrasena == "4567":
            self.accept_admin_login()
        else:
            self.mostrar_error()
    
    def accept_login(self):
        """Abre la ventana principal si las credenciales son correctas."""
        self.ventana_ventas = VentanaPrincipal()
        self.ventana_ventas.show()
        self.close()
    
    def accept_admin_login(self):
        """Abre la ventana de administración si las credenciales son correctas."""
        self.ventana_admin = VentanaAdmin()  # Ventana para el administrador
        self.ventana_admin.show()
        self.close()
    
    def mostrar_error(self):
        """Muestra un mensaje de error si las credenciales son incorrectas."""
        QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos.")
