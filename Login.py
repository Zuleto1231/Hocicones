import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from VentanaPrincipal import VentanaPrincipal  # Asegúrate de que esté en el mismo directorio

class VentanaLogin(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SVH")
        self.setGeometry(100, 100, 100, 200)  # Ajustar tamaño de la ventana (más pequeña)

        layout = QVBoxLayout()

        # Etiqueta para indicar los campos
        self.label_usuario = QLabel("Usuario:")
        layout.addWidget(self.label_usuario)

        # Campo para el usuario
        self.input_usuario = QLineEdit(self)
        self.input_usuario.setPlaceholderText("Ingrese su usuario")
        self.input_usuario.setFixedWidth(200)  # Ajustamos el tamaño del campo
        layout.addWidget(self.input_usuario)

        # Etiqueta para la contraseña
        self.label_contrasena = QLabel("Contraseña:")
        layout.addWidget(self.label_contrasena)

        # Campo para la contraseña
        self.input_contrasena = QLineEdit(self)
        self.input_contrasena.setPlaceholderText("Ingrese su contraseña")
        self.input_contrasena.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_contrasena.setFixedWidth(200)  # Ajustamos el tamaño del campo
        layout.addWidget(self.input_contrasena)

        # Botón de login
        self.btn_login = QPushButton("Iniciar sesión", self)
        self.btn_login.setFixedWidth(200)  # Ajustamos el tamaño del botón
        self.btn_login.clicked.connect(self.iniciar_sesion)
        layout.addWidget(self.btn_login)

        # Establecer el layout de la ventana
        self.setLayout(layout)

    def iniciar_sesion(self):
        """Verifica las credenciales de login y abre la ventana principal si son correctas."""
        usuario = self.input_usuario.text()
        contrasena = self.input_contrasena.text()

        # Aquí debes validar el usuario y la contraseña (puedes hacerlo contra una base de datos o archivo)
        if usuario == "admin" and contrasena == "1234":  # Esto es solo un ejemplo simple
            self.accept_login()
        else:
            self.mostrar_error()

    def accept_login(self):
        """Abre la ventana principal de ventas si las credenciales son correctas."""
        self.ventana_ventas = VentanaPrincipal()
        self.ventana_ventas.show()
        self.close()  # Cierra la ventana de login

    def mostrar_error(self):
        """Muestra un mensaje de error si las credenciales son incorrectas."""
        QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = VentanaLogin()
    login.show()
    sys.exit(app.exec())
