import pandas as pd
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QInputDialog, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QFormLayout, QDateEdit, QMessageBox, QDialog, QHBoxLayout, QHeaderView
from PyQt6.QtCore import Qt, QDate
import sys
from PyQt6.QtWidgets import QApplication
import re

def aplicar_estilos(app):
    try:
        with open("estilos.qss", "r") as file:
            styles = file.read()
            app.setStyleSheet(styles)
            print("✅ Estilos aplicados correctamente")
    except Exception as e:
        print(f"⚠️ Error al aplicar estilos: {e}")

class VentanaAdmin(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Administracion")
        self.setGeometry(100, 100, 1280, 720)  # Establecer el tamaño de la ventana a 1280x720

        layout = QVBoxLayout()

        # Título de la ventana
        self.titulo_label = QLabel("Área de Administración - Hocicones")
        self.titulo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titulo_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(self.titulo_label)

        # Cargar la base de datos (productos) desde el archivo Excel
        self.df_productos = pd.read_excel("BD.xlsx", sheet_name="Sheet1")
        self.df_productos.columns = self.df_productos.columns.str.strip()  # Eliminar posibles espacios en los nombres de las columnas

        # Crear una tabla para mostrar los productos
        self.tabla_productos = QTableWidget(self)
        self.tabla_productos.setColumnCount(5)  # 5 columnas: ID, Nombre, Precio Compra, Precio Venta, Stock
        self.tabla_productos.setHorizontalHeaderLabels(["ID", "Nombre", "Precio Compra", "Precio Venta", "Stock"])

        self.tabla_productos.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.tabla_productos.setRowCount(0)  # Inicialmente sin filas
        layout.addWidget(self.tabla_productos)
        self.tabla_productos.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        # Layout horizontal para los botones (uno al lado de otro)
        boton_layout = QHBoxLayout()

        self.btn_agregar_producto = QPushButton("Agregar Producto", self)
        self.btn_agregar_producto.clicked.connect(self.mostrar_formulario_agregar_producto)
        boton_layout.addWidget(self.btn_agregar_producto)

        self.btn_eliminar_producto = QPushButton("Eliminar Producto", self)
        self.btn_eliminar_producto.clicked.connect(self.eliminar_producto)
        boton_layout.addWidget(self.btn_eliminar_producto)

        self.btn_editar_producto = QPushButton("Editar Producto", self)
        self.btn_editar_producto.clicked.connect(self.editar_producto)
        boton_layout.addWidget(self.btn_editar_producto)

        self.btn_bajo_stock = QPushButton("Consultar Productos con Bajo Stock", self)
        self.btn_bajo_stock.clicked.connect(self.consultar_bajo_stock)
        boton_layout.addWidget(self.btn_bajo_stock)

        layout.addLayout(boton_layout)  # Agregar el layout de botones al layout principal

        # Crear un QLineEdit para el buscador
        self.busqueda_input = QLineEdit(self)
        self.busqueda_input.setPlaceholderText("Buscar producto por nombre...")
        self.busqueda_input.textChanged.connect(self.filtrar_tabla)
        layout.addWidget(self.busqueda_input)  # Agregar el campo de búsqueda

        # Establecemos el layout para la ventana
        self.setLayout(layout)

        # Llamar a la función para actualizar la tabla con los productos
        self.actualizar_tabla()

    def consultar_bajo_stock(self):
        """Consulta productos con stock menor a 10"""
        
        # Asegurarse de que la columna 'Stock' sea numérica, y convertir los valores no numéricos a NaN
        self.df_productos['Stock'] = pd.to_numeric(self.df_productos['Stock'], errors='coerce')

        # Filtrar los productos con stock menor a 10
        productos_bajo_stock = self.df_productos[self.df_productos["Stock"] < 10]

        # Comprobar si el DataFrame de productos con bajo stock está vacío
        if productos_bajo_stock.empty:
            QMessageBox.information(self, "Consulta Baja de Stock", "No hay productos con bajo stock.")
            return

        # Limpiar la tabla actual
        self.tabla_productos.setRowCount(0)  # Limpiamos las filas anteriores

        # Establecer el número de filas en la tabla
        self.tabla_productos.setRowCount(len(productos_bajo_stock))

        # Llenar la tabla con los productos de bajo stock
        for i, row in productos_bajo_stock.iterrows():
            self.tabla_productos.setItem(i, 0, QTableWidgetItem(str(row['ID'])))
            self.tabla_productos.setItem(i, 1, QTableWidgetItem(str(row['Producto'])))
            self.tabla_productos.setItem(i, 2, QTableWidgetItem(str(row['P_Compra'])))
            self.tabla_productos.setItem(i, 3, QTableWidgetItem(str(row['P_Venta'])))
            self.tabla_productos.setItem(i, 4, QTableWidgetItem(str(row['Stock'])))


    def eliminar_producto(self):
        """Función para eliminar un producto seleccionado"""
        row = self.tabla_productos.currentRow()

        if row == -1:
            QMessageBox.warning(self, "Error", "Debe seleccionar un producto para eliminar.")
            return

        # Obtener el ID del producto seleccionado
        producto_id = self.tabla_productos.item(row, 0).text()

        # Eliminar el producto del DataFrame
        self.df_productos = self.df_productos[self.df_productos["ID"] != int(producto_id)]

        # Guardar el DataFrame actualizado en el archivo Excel
        try:
            self.df_productos.to_excel("BD.xlsx", sheet_name="Sheet1", index=False)
            QMessageBox.information(self, "Éxito", "Producto eliminado correctamente.")
            self.actualizar_tabla()  # Actualizar la tabla de productos
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al guardar en el archivo Excel: {e}")

    def mostrar_formulario_agregar_producto(self):
        """Muestra el formulario para agregar un producto"""
        self.formulario_dialog = QDialog(self)
        self.formulario_dialog.setWindowTitle("Agregar Nuevo Producto")

        formulario_layout = QFormLayout()

        self.nombre_input = QLineEdit(self.formulario_dialog)
        self.precio_compra_input = QLineEdit(self.formulario_dialog)
        self.precio_venta_input = QLineEdit(self.formulario_dialog)
        self.stock_input = QLineEdit(self.formulario_dialog)
        self.fecha_entrada_input = QDateEdit(self.formulario_dialog)
        self.fecha_entrada_input.setDate(QDate.currentDate())  # Establece la fecha actual

        formulario_layout.addRow("Nombre del Producto:", self.nombre_input)
        formulario_layout.addRow("Precio de Compra:", self.precio_compra_input)
        formulario_layout.addRow("Precio de Venta:", self.precio_venta_input)
        formulario_layout.addRow("Stock Inicial:", self.stock_input)
        formulario_layout.addRow("Fecha de Entrada:", self.fecha_entrada_input)

        # Botón para confirmar la adición
        self.btn_confirmar = QPushButton("Confirmar", self.formulario_dialog)
        self.btn_confirmar.clicked.connect(self.agregar_producto)
        formulario_layout.addWidget(self.btn_confirmar)

        self.formulario_dialog.setLayout(formulario_layout)
        self.formulario_dialog.exec()  # Mostrar el diálogo para agregar el producto

    def editar_producto(self):
        """Función para editar un producto seleccionado"""
        row = self.tabla_productos.currentRow()

        if row == -1:
            QMessageBox.warning(self, "Error", "Debe seleccionar un producto para editar.")
            return

        # Obtener los valores actuales del producto seleccionado
        nombre = self.tabla_productos.item(row, 1).text()
        precio_compra = self.tabla_productos.item(row, 2).text()
        precio_venta = self.tabla_productos.item(row, 3).text()
        stock = self.tabla_productos.item(row, 4).text()

        # Mostrar el formulario con los valores actuales del producto
        self.formulario_dialog = QDialog(self)
        self.formulario_dialog.setWindowTitle("Editar Producto")
        formulario_layout = QFormLayout()

        # Crear los campos para editar
        self.nombre_input = QLineEdit(self.formulario_dialog)
        self.nombre_input.setText(nombre)
        self.precio_compra_input = QLineEdit(self.formulario_dialog)
        self.precio_compra_input.setText(precio_compra)
        self.precio_venta_input = QLineEdit(self.formulario_dialog)
        self.precio_venta_input.setText(precio_venta)
        self.stock_input = QLineEdit(self.formulario_dialog)
        self.stock_input.setText(stock)
        self.fecha_entrada_input = QDateEdit(self.formulario_dialog)
        self.fecha_entrada_input.setDate(QDate.currentDate())  # Establece la fecha actual

        formulario_layout.addRow("Nombre del Producto:", self.nombre_input)
        formulario_layout.addRow("Precio de Compra:", self.precio_compra_input)
        formulario_layout.addRow("Precio de Venta:", self.precio_venta_input)
        formulario_layout.addRow("Stock Inicial:", self.stock_input)
        formulario_layout.addRow("Fecha de Entrada:", self.fecha_entrada_input)

        # Botón para confirmar la edición
        self.btn_confirmar = QPushButton("Confirmar", self.formulario_dialog)
        self.btn_confirmar.clicked.connect(lambda: self.confirmar_edicion(row))
        formulario_layout.addWidget(self.btn_confirmar)

        self.formulario_dialog.setLayout(formulario_layout)
        self.formulario_dialog.exec()  # Mostrar el diálogo para editar el producto

    def confirmar_edicion(self, row):
        """Confirmar la edición de un producto"""
        # Obtener los datos editados del formulario
        nombre = self.nombre_input.text()
        precio_compra = self.precio_compra_input.text()
        precio_venta = self.precio_venta_input.text()
        stock = self.stock_input.text()

        # Verificación de campos vacíos
        if not nombre or not precio_compra or not precio_venta or not stock:
            QMessageBox.warning(self, "Error", "Todos los campos deben estar completos.")
            return

        # Validar que los valores sean numéricos
        try:
            precio_compra = float(precio_compra)  # Convertir a float
            precio_venta = float(precio_venta)  # Convertir a float
            stock = int(stock)  # Convertir a int
        except ValueError:
            QMessageBox.warning(self, "Error", "Precio de compra, precio de venta y stock deben ser numéricos.")
            return

        # Actualizar el producto en el DataFrame
        producto_id = int(self.tabla_productos.item(row, 0).text())  # Obtener el ID del producto
        self.df_productos.loc[self.df_productos["ID"] == producto_id, "Producto"] = nombre
        self.df_productos.loc[self.df_productos["ID"] == producto_id, "P_Compra"] = precio_compra
        self.df_productos.loc[self.df_productos["ID"] == producto_id, "P_Venta"] = precio_venta
        self.df_productos.loc[self.df_productos["ID"] == producto_id, "Stock"] = stock

        # Guardar el DataFrame actualizado en el archivo Excel
        try:
            self.df_productos.to_excel("BD.xlsx", sheet_name="Sheet1", index=False)
            QMessageBox.information(self, "Éxito", "Producto editado correctamente.")
            self.actualizar_tabla()  # Actualizar la tabla de productos
            self.formulario_dialog.accept()  # Cerrar el formulario de edición
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al guardar en el archivo Excel: {e}")


    def agregar_producto(self):
        """Función para agregar un nuevo producto con todos los detalles"""
        # Obtener los datos del formulario
        nombre = self.nombre_input.text()
        precio_compra = self.precio_compra_input.text()
        precio_venta = self.precio_venta_input.text()
        stock = self.stock_input.text()

        # Verificación de campos vacíos
        if not nombre or not precio_compra or not precio_venta or not stock:
            QMessageBox.warning(self, "Error", "Todos los campos deben estar completos.")
            return

        # Validar que los valores sean numéricos
        try:
            precio_compra = float(precio_compra)  # Convertir a float
            precio_venta = float(precio_venta)  # Convertir a float
            stock = int(stock)  # Convertir a int
        except ValueError:
            QMessageBox.warning(self, "Error", "Precio de compra, precio de venta y stock deben ser numéricos.")
            return

        # Crear el nuevo producto
        nuevo_id = len(self.df_productos) + 1  # Asignar un nuevo ID
        nuevo_producto = {
            "ID": nuevo_id,
            "Producto": nombre,
            "Stock": stock,
            "P_Compra": precio_compra,
            "P_Venta": precio_venta
        }

        # Convertir el nuevo producto a un DataFrame
        nuevo_producto_df = pd.DataFrame([nuevo_producto])

        # Concatenar el nuevo producto con el DataFrame original
        self.df_productos = pd.concat([self.df_productos, nuevo_producto_df], ignore_index=True)

        # Guardar los cambios en el archivo Excel
        try:
            self.df_productos.to_excel("BD.xlsx", sheet_name="Sheet1", index=False)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al guardar en el archivo Excel: {e}")
            return

        # Actualizar la tabla de productos
        self.actualizar_tabla()

        # Cerrar el formulario
        self.formulario_dialog.accept()

    def actualizar_tabla(self):
        self.tabla_productos.setRowCount(len(self.df_productos))  

       
        for i, row in self.df_productos.iterrows():
            self.tabla_productos.setItem(i, 0, QTableWidgetItem(str(row['ID'])))
            self.tabla_productos.setItem(i, 1, QTableWidgetItem(str(row['Producto'])))
            self.tabla_productos.setItem(i, 2, QTableWidgetItem(str(row['P_Compra'])))
            self.tabla_productos.setItem(i, 3, QTableWidgetItem(str(row['P_Venta'])))
            self.tabla_productos.setItem(i, 4, QTableWidgetItem(str(row['Stock'])))



    def filtrar_tabla(self):
        """Filtra la tabla en tiempo real mientras se escribe en el buscador"""
        filtro = self.busqueda_input.text().strip().lower()  # Limpiar el texto y convertir a minúsculas

        if filtro:  # Si hay texto en el buscador
            # Filtrar productos que contienen la palabra exacta en la columna 'Producto'
            productos_filtrados = self.df_productos[self.df_productos['Producto'].str.contains(filtro, case=False, na=False)]
        else:
            # Si no hay texto en el buscador, mostrar todos los productos
            productos_filtrados = self.df_productos

        self.tabla_productos.setRowCount(len(productos_filtrados))  # Actualiza el número de filas

        # Llenamos la tabla con los productos filtrados (o todos si no hay filtro)
        for i, row in productos_filtrados.iterrows():
            self.tabla_productos.setItem(i, 0, QTableWidgetItem(str(row['ID'])))
            self.tabla_productos.setItem(i, 1, QTableWidgetItem(str(row['Producto'])))
            self.tabla_productos.setItem(i, 2, QTableWidgetItem(str(row['P_Compra'])))
            self.tabla_productos.setItem(i, 3, QTableWidgetItem(str(row['P_Venta'])))
            self.tabla_productos.setItem(i, 4, QTableWidgetItem(str(row['Stock'])))


if __name__ == '__main__':
    app = QApplication(sys.argv)  # Crear QApplication primero
    aplicar_estilos(app)
    ventana_admin = VentanaAdmin()  # Crear la instancia de la ventana de admin
    ventana_admin.show()  # Mostrar la ventana de admin
    sys.exit(app.exec())  # Iniciar el ciclo de eventos de la aplicación
