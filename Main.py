import sys
from PyQt6.QtWidgets import QApplication
from Login import VentanaLogin  # Asegúrate de que esté correctamente importado
from VentanaPrincipal import VentanaPrincipal  # Importa la ventana principal
from VentanaAdmin import VentanaAdmin  # Importa la ventana de admin

def aplicar_estilos(app):
    try:
        with open("estilos.qss", "r") as file:
            styles = file.read()
            app.setStyleSheet(styles)
            print("✅ Estilos aplicados correctamente")
    except Exception as e:
        print(f"⚠️ Error al aplicar estilos: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)  # Crear QApplication primero
    aplicar_estilos(app)
    # Crear la ventana de login
    login_window = VentanaLogin()  # Crear la instancia de la ventana de login
    login_window.show()  # Mostrar la ventana de login
    
    # Ejecutar el ciclo de eventos
    sys.exit(app.exec())  # Iniciar el ciclo de eventos de la aplicación
