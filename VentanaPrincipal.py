import sys
import os
import pandas as pd
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
                             QMessageBox, QInputDialog, QFileDialog, QHBoxLayout, QListWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtGui import QPixmap
from FacturaElectronica import generar_factura, enviar_factura
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox, QListWidget
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton
from Login import *
from GuardarVentas import *


class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.file_path = "BD.xlsx"
        self.df_inventario = pd.read_excel(self.file_path)
        self.df_inventario.columns = self.df_inventario.columns.str.strip()  # Eliminar espacios innecesarios       
        self.df_inventario['ID'] = pd.to_numeric(self.df_inventario['ID'], errors='coerce').astype('Int64')  # Asegurar tipo correcto       
        self.df_ventas = pd.DataFrame(columns=['Producto', 'Cantidad', 'Precio', 'Costo Total'])
        
        # Inicializamos la interfaz de usuario
        self.initUI()
    def initUI(self):
        self.setWindowTitle("Gestión de Ventas - Hocicones")
        self.setGeometry(100, 100, 1280, 720)  # Ajustamos el tamaño de la ventana
        layout = QVBoxLayout()
        font = QFont()
        font.setPointSize(18)  # Aumentamos el tamaño de la fuente
        self.label = QLabel("Ingrese ID del producto y cantidad a vender:")
        self.label.setFont(font)
        layout.addWidget(self.label)
    # Campo para ingresar ID de producto
        self.input_id = QLineEdit(self)
        self.input_id.setPlaceholderText("ID del Producto")
        self.input_id.setFont(font)
        self.input_id.setFixedWidth(600)  # Ajustamos el tamaño del campo
        layout.addWidget(self.input_id)
    # Campo para ingresar cantidad a vender
        self.input_cantidad = QLineEdit(self)
        self.input_cantidad.setPlaceholderText("Cantidad")
        self.input_cantidad.setFont(font)
        self.input_cantidad.setFixedWidth(600)  # Ajustamos el tamaño del campo
        layout.addWidget(self.input_cantidad)
    # Botón para agregar venta
        self.btn_agregar = QPushButton("Añadir a la lista de compras", self)
        self.btn_agregar.setFont(font)
        self.btn_agregar.setFixedWidth(600)  # Ajustamos el tamaño del botón
        self.btn_agregar.clicked.connect(self.agregar_venta)  # Conectamos la función agregar_venta
        layout.addWidget(self.btn_agregar)
    # Barra de búsqueda para filtrar productos por nombre
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Buscar producto por nombre...")
        self.search_bar.setFont(font)
        self.search_bar.setFixedWidth(600)  # Ajustamos el tamaño del campo
        self.search_bar.textChanged.connect(self.filtrar_productos)  # Conectamos la función filtrar_productos
        layout.addWidget(self.search_bar)
    # Lista para mostrar los productos filtrados
        self.lista_productos = QListWidget(self)
        self.lista_productos.setFont(font)
        self.lista_productos.setFixedHeight(250)  # Ajustamos la altura de la lista
        self.lista_productos.itemClicked.connect(self.seleccionar_producto)  # Conectamos la función seleccionar_producto
        layout.addWidget(self.lista_productos)
    # Tabla para mostrar los productos vendidos
        self.tabla = QTableWidget()
        self.tabla.setFont(font)
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["Producto", "Cantidad", "Precio", "Costo Total"])
        self.tabla.setRowCount(0)  # Inicialmente sin filas
        self.tabla.setFixedHeight(300)  # Ajustamos la altura de la tabla
        layout.addWidget(self.tabla)
        self.tabla.setColumnWidth(0, 500)  # Ajusta el ancho de la columna "Producto"
        self.tabla.setColumnWidth(1, 280)  # Ajusta el ancho de la columna "Cantidad"
        self.tabla.setColumnWidth(2, 250)  # Ajusta el ancho de la columna "Precio"
        self.tabla.setColumnWidth(3, 250)  # Ajusta el ancho de la columna "Costo Total"

    # Agregar un QLabel para mostrar el total a pagar
        self.total_label = QLabel("Total a Pagar: $0.00", self)
        self.total_label.setFont(font)
        layout.addWidget(self.total_label)

   # Botón para generar factura
        self.btn_generar_factura = QPushButton("Realizar venta", self)
        self.btn_generar_factura.setFont(font)
        self.btn_generar_factura.setFixedWidth(1280)  # Ajustamos el tamaño del botón
        self.btn_generar_factura.clicked.connect(self.generar_factura)  # Conectamos la función generar_factura
        layout.addWidget(self.btn_generar_factura)

#Botodon de devoluciones
        self.btn_devoluciones = QPushButton("Devoluciones", self)
        self.btn_devoluciones.setFont(font)
        self.btn_devoluciones.setFixedWidth(1280)
        self.btn_devoluciones.clicked.connect(self.abrir_ventana_devoluciones)
        layout.addWidget(self.btn_devoluciones)

    # Establecemos el layout de la ventana
        self.setLayout(layout)

    def abrir_ventana_devoluciones(self):
        # Obtener las ventas previas
        ventas = self.obtener_ventas()
        self.ventana_devoluciones = VentanaDevoluciones(ventas, self)
        self.ventana_devoluciones.show()

    def obtener_ventas(self):
        try:
            df_ventas = pd.read_excel("BD.xlsx", sheet_name="Ventas")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo cargar el archivo Excel: {e}")
            return []

        required_columns = ["ID", "Cliente", "Producto", "Cantidad", "Precio", "Costo Total"]
        for column in required_columns:
            if column not in df_ventas.columns:
                QMessageBox.warning(self, "Error", f"La columna {column} falta en el archivo Excel.")
                return []

        ventas_dict = {}

        for _, row in df_ventas.iterrows():
            venta_id = row["ID"]

            if venta_id not in ventas_dict:
                ventas_dict[venta_id] = {
                    "ID": venta_id,
                    "Cliente": row["Cliente"],
                    "productos": []  # Ahora sí creamos la lista de productos
                }

            ventas_dict[venta_id]["productos"].append({
                "producto": row["Producto"],
                "cantidad": row["Cantidad"],
                "precio": row["Precio"],
                "total": row["Costo Total"]
            })

        return list(ventas_dict.values())  # Convertimos el diccionario en una lista


    def actualizar_lista_productos(self):
        """Actualiza la lista de productos en la interfaz."""
        self.lista_productos.clear()
        for producto in self.df_inventario['Producto'].tolist():  # Uso de 'Producto' tal como está en Excel
            self.lista_productos.addItem(producto)

    def filtrar_productos(self):
        """Filtra los productos según el texto de búsqueda."""
        texto = self.search_bar.text().lower()
        self.lista_productos.clear()
        productos_filtrados = [p for p in self.df_inventario['Producto'].tolist() if texto in p.lower()]  # Uso de 'Producto'
        for producto in productos_filtrados:
            self.lista_productos.addItem(producto)

    def seleccionar_producto(self, item):
        """Rellena el campo de ID con el producto seleccionado de la lista."""
        producto_seleccionado = item.text()
        producto = self.df_inventario[self.df_inventario['Producto'] == producto_seleccionado]  # Uso de 'Producto'
        if not producto.empty:
            self.input_id.setText(str(producto.iloc[0]['ID']))

    def actualizar_total(self):
        total_a_pagar = self.df_ventas['Costo Total'].sum()   
        iva = total_a_pagar * 0.19   
        total_con_iva = total_a_pagar + iva
        self.total_label.setText(f"Total a Pagar: ${total_con_iva:.0f} (IVA incluido: ${iva:.0f})")



    def agregar_venta(self):
        try:
            producto_id = int(self.input_id.text())
            cantidad_vendida = int(self.input_cantidad.text())
            producto = self.df_inventario[self.df_inventario['ID'] == producto_id]
            if producto.empty:
                QMessageBox.warning(self, "Error", "ID de producto no encontrado.")
                return
            stock_disponible = producto.iloc[0]['Stock']
            precio_venta = producto.iloc[0]['P_Venta']
            if cantidad_vendida > stock_disponible:
                QMessageBox.warning(self, "Error", f"Stock insuficiente. Solo hay {stock_disponible} unidades disponibles.")
                return
            self.df_inventario.loc[self.df_inventario['ID'] == producto_id, 'Stock'] -= cantidad_vendida
            costo_total = cantidad_vendida * precio_venta
            IVA = costo_total * 0.19
            total = costo_total
            nueva_fila = pd.DataFrame([{
            'Producto': producto.iloc[0]['Producto'],
            'Cantidad': cantidad_vendida,
            'Precio': precio_venta,
            'Costo Total': total
            }])
            nueva_fila = nueva_fila.dropna(axis=1, how='all')
            self.df_ventas = pd.concat([self.df_ventas, nueva_fila], ignore_index=True)

            self.actualizar_tabla()
            self.actualizar_total()  # Llamamos a esta función para actualizar el total a pagar

        except ValueError:
            QMessageBox.warning(self, "Error", "Formato incorrecto. Use solo números.")


    def actualizar_tabla(self):
        """Actualiza la tabla de ventas."""
        self.tabla.setRowCount(len(self.df_ventas))
        for i, row in self.df_ventas.iterrows():
            self.tabla.setItem(i, 0, QTableWidgetItem(str(row['Producto'])))
            self.tabla.setItem(i, 1, QTableWidgetItem(str(row['Cantidad'])))
            self.tabla.setItem(i, 2, QTableWidgetItem(f"${row['Precio']:.0f}"))
            self.tabla.setItem(i, 3, QTableWidgetItem(f"${row['Costo Total']:.0f}"))
    
    def realizar_compra(self):
        if self.df_ventas.empty:
            QMessageBox.warning(self, "Error", "No hay productos en la compra.")
            return
    
    # Mostrar el resumen de la compra
        resumen = ""
        total_compra = 0
        for _, row in self.df_ventas.iterrows():
            resumen += f"Producto: {row['Producto']}\nCantidad: {row['Cantidad']}\nPrecio: ${row['Precio']:.2f}\n\n"
            total_compra += row['Costo Total']    
        resumen += f"\nTotal a pagar: ${total_compra:.2f}"
        QMessageBox.information(self, "Resumen de Compra", resumen)
        self.generar_factura()
    

    def crear_venta(self, nombre_cliente):
        venta_id = random.randint(100000, 999999)  # Un solo ID de venta para toda la compra
        total = 0
        productos_venta = []

    # Recorrer los productos vendidos y calcular el total
        for _, row in self.df_ventas.iterrows():
            producto = row['Producto']
            cantidad = row['Cantidad']
            precio = row['Precio']
            costo_total = row['Costo Total']
            total += costo_total  # Sumar el total

        # Crear el diccionario del producto con las claves correctas
            productos_venta.append({
                "Producto": producto,
                "Cantidad": cantidad,
                "Precio": precio,
                "Costo Total": costo_total
            })

    # Mostrar los datos antes de guardarlos para asegurarse que todo está bien
        print(f"Venta Creada: {venta_id} {productos_venta} {total}")
        return [venta_id, nombre_cliente, productos_venta, total]  # Devolvemos el ID, el nombre del cliente, productos y total
    
    def guardar_venta_en_excel(self, venta_data):
        try:
            workbook = openpyxl.load_workbook("BD.xlsx")
            if "Ventas" not in workbook.sheetnames:
                sheet = workbook.create_sheet("Ventas")
            else:
                sheet = workbook["Ventas"]
        except FileNotFoundError:
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.title = "Ventas"
        # Escribimos los encabezados si el archivo está vacío
            sheet.append(["ID", "Cliente", "Producto", "Cantidad", "Precio", "Costo Total", "Total Venta"])

    # Guardar la venta con todos los productos, incluido el nombre del cliente
        for producto in venta_data[2]:  # venta_data[2] es la lista de productos
            sheet.append([venta_data[0], venta_data[1], producto["Producto"], producto["Cantidad"], producto["Precio"], producto["Costo Total"], venta_data[3]])

    # Guardar el archivo
        workbook.save("BD.xlsx")
        print(f"Venta Guardada: {venta_data}")  # Asegúrate de que los datos se guardan correctamente

##############################################################################################################
    def generar_factura(self):
        if self.df_ventas.empty:
            QMessageBox.warning(self, "Error", "No hay productos vendidos.")
            return

    # Crear un cuadro de diálogo para pedir el nombre y el correo en una sola ventana
        dialog = QDialog(self)
        dialog.setWindowTitle("Datos del Cliente")
        layout = QVBoxLayout()

    # Etiqueta y campo para el nombre
        self.nombre_label = QLabel("Ingrese el nombre del cliente:")
        self.nombre_input = QLineEdit(dialog)
        layout.addWidget(self.nombre_label)
        layout.addWidget(self.nombre_input)

    # Etiqueta y campo para el correo
        self.correo_label = QLabel("Ingrese el correo del cliente:")
        self.correo_input = QLineEdit(dialog)
        layout.addWidget(self.correo_label)
        layout.addWidget(self.correo_input)

    # Botón para confirmar
        self.confirm_button = QPushButton("Confirmar", dialog)
        layout.addWidget(self.confirm_button)

        dialog.setLayout(layout)

    # Conectar el botón "Confirmar" a la función que cierra el diálogo
        self.confirm_button.clicked.connect(dialog.accept)  # Cierra el diálogo al hacer clic

    # Mostrar el diálogo
        dialog.exec()

    # Obtener los valores de nombre y correo luego de que el diálogo se cierre
        nombre_cliente = self.nombre_input.text()
        correo_cliente = self.correo_input.text()

    # Verificar que el nombre y correo no estén vacíos
        if not nombre_cliente or not correo_cliente:
            QMessageBox.warning(self, "Error", "Debe ingresar el nombre y correo del cliente.")
            return

    # Crear una carpeta para las facturas si no existe
        directorio_facturas = "Facturas/"
        os.makedirs(directorio_facturas, exist_ok=True)
        fecha_venta = datetime.now().strftime("%d/%m/%Y")

    # Generar los datos para la factura
        items = []
        for _, row in self.df_ventas.iterrows():
            producto = self.df_inventario[self.df_inventario['Producto'] == row['Producto']]
            if not producto.empty:
                precio_venta = producto.iloc[0]['P_Venta']
                items.append({
                    'descripcion': row['Producto'],
                    'Cantidad': row['Cantidad'],
                    'Precio': precio_venta,
                    'Costo Total': row['Costo Total']
                })

    # Verificar si se obtuvieron los precios correctamente
        if not items:
            QMessageBox.warning(self, "Error", "No se pudieron obtener los precios de los productos.")
            return

    # Crear los datos para la factura
        datos_factura = {
            "cliente": nombre_cliente,
            "correo": correo_cliente,
            "fecha": fecha_venta,
            "items": items
        }

    # Nombre de la factura (basado en la fecha)
        fecha_venta_segura = fecha_venta.replace('/', '-')
        nombre_factura = f"factura_{fecha_venta_segura}.pdf"
        ruta_factura = os.path.join(directorio_facturas, nombre_factura)

    # Generar la factura y enviarla por correo
        generar_factura(ruta_factura, datos_factura)
        enviar_factura(correo_cliente, nombre_cliente, ruta_factura)

    # Mostrar el mensaje final
        QMessageBox.information(self, "Éxito", f"Factura generada y enviada a {correo_cliente}")

    # Guardar la venta en Excel después de generar la factura
        venta_data = self.crear_venta(nombre_cliente)  # Crear la venta con el nombre del cliente
        self.guardar_venta_en_excel(venta_data)  # Guardar la venta en el archivo Excel
        self.limpiar_campos


    def limpiar_campos(self):
    #Limpia todos los campos de la interfaz."""
        self.input_id.clear()  # Limpiar el campo ID
        self.input_cantidad.clear()  # Limpiar el campo cantidad
        self.search_bar.clear()  # Limpiar la barra de búsqueda
        self.lista_productos.clear()  # Limpiar la lista de productos
        self.tabla.setRowCount(0)  # Limpiar la tabla de ventas
        self.df_ventas = pd.DataFrame(columns=['Producto', 'Cantidad', 'Precio', 'Costo Total'])  # Limpiar ventas
        self.actualizar_tabla()
        self.total_label.setText("Total a Pagar: $0.00")  # Limpiar el total

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = VentanaLogin()
    login.show()
    sys.exit(app.exec())
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    # Mover este código dentro de la clase donde self está definido
    print(ventana.df_inventario.columns)
    sys.exit(app.exec())