import sys
import os
import pandas as pd
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
                             QMessageBox, QInputDialog, QFileDialog, QHBoxLayout, QListWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from FacturaElectronica import generar_factura, enviar_factura

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()

        # Inicialización de los datos
        self.file_path = "BD.xlsx"
        self.df_inventario = pd.read_excel(self.file_path)
        self.df_inventario.columns = self.df_inventario.columns.str.strip()  # Eliminar espacios innecesarios
        
        # Aseguramos que los tipos de datos estén bien definidos
        self.df_inventario['ID'] = pd.to_numeric(self.df_inventario['ID'], errors='coerce').astype('Int64')  # Asegurar tipo correcto
        
        self.df_ventas = pd.DataFrame(columns=['Producto', 'Cantidad', 'Precio', 'Costo Total'])

        # Inicializamos la interfaz de usuario
        self.initUI()

    def initUI(self):
        # Configuración de la ventana
        self.setWindowTitle("Gestión de Ventas - Hocicones")
        self.setGeometry(100, 100, 1280, 720)  # Ajustamos el tamaño de la ventana

        layout = QVBoxLayout()

        # Fuente más grande para los labels y campos de texto
        font = QFont()
        font.setPointSize(18)  # Aumentamos el tamaño de la fuente

        # Añadir elementos de interfaz
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


        # Botón para generar factura
        self.btn_generar_factura = QPushButton("Generar Factura", self)
        self.btn_generar_factura.setFont(font)
        self.btn_generar_factura.setFixedWidth(1280)  # Ajustamos el tamaño del botón
        self.btn_generar_factura.clicked.connect(self.generar_factura)  # Conectamos la función generar_factura
        layout.addWidget(self.btn_generar_factura)

        # Establecemos el layout de la ventana
        self.setLayout(layout)

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

    def agregar_venta(self):
        try:
            if 'P_Venta' not in self.df_inventario.columns:
                QMessageBox.warning(self, "Error", "La columna 'P_Venta' no existe en el inventario.")
                return
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
            total = costo_total + IVA  
            nueva_fila = pd.DataFrame([{
                'Producto': producto.iloc[0]['Producto'], 
                'Cantidad': cantidad_vendida,
                'Precio': precio_venta, 
                'Costo Total': total
            }])
            nueva_fila = nueva_fila.dropna(axis=1, how='all')  # Eliminar columnas vacías de nueva_fila
            self.df_ventas = pd.concat([self.df_ventas, nueva_fila], ignore_index=True)
            self.actualizar_tabla()

        except ValueError:
            QMessageBox.warning(self, "Error", "Formato incorrecto. Use solo números.")

    def actualizar_tabla(self):
        """Actualiza la tabla de ventas."""
        self.tabla.setRowCount(len(self.df_ventas))
        for i, row in self.df_ventas.iterrows():
            self.tabla.setItem(i, 0, QTableWidgetItem(str(row['Producto'])))
            self.tabla.setItem(i, 1, QTableWidgetItem(str(row['Cantidad'])))
            self.tabla.setItem(i, 2, QTableWidgetItem(f"${row['Precio']:.2f}"))
            self.tabla.setItem(i, 3, QTableWidgetItem(f"${row['Costo Total']:.2f}"))

    def generar_factura(self):
        if self.df_ventas.empty:
            QMessageBox.warning(self, "Error", "No hay productos vendidos.")
            return
        nombre_cliente, ok = QInputDialog.getText(self, "Nombre del Cliente", "Ingrese el nombre del cliente:")
        if not ok or not nombre_cliente:
            return
        correo_cliente, ok = QInputDialog.getText(self, "Correo Electrónico", "Ingrese el correo del cliente:")
        if not ok or not correo_cliente:
            return
        directorio_facturas = "Facturas/"
        os.makedirs(directorio_facturas, exist_ok=True)  # Crear la carpeta si no existe
        fecha_venta = datetime.now().strftime("%d/%m/%Y")
    
    # Generar los datos para la factura
        items = []
        for _, row in self.df_ventas.iterrows():
            producto = self.df_inventario[self.df_inventario['Producto'] == row['Producto']]  # Obtener el precio desde el inventario
            if not producto.empty:
                precio_venta = producto.iloc[0]['P_Venta']  # Acceder a P_Venta en self.df_inventario
                items.append({
                'descripcion': row['Producto'], 
                'Cantidad': row['Cantidad'], 
                'Precio': precio_venta, 
                'Costo Total': row['Costo Total']
                })
    
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

    # Nombre de la factura
        # Nombre de la factura
        fecha_venta_segura = fecha_venta.replace('/', '-')  # Reemplazar '/' por '-'
        nombre_factura = f"factura_{fecha_venta_segura}.pdf"
        ruta_factura = os.path.join(directorio_facturas, nombre_factura)
    # Generar la factura y enviarla por correo
        generar_factura(ruta_factura, datos_factura)
        enviar_factura(correo_cliente, nombre_cliente, ruta_factura)
        QMessageBox.information(self, "Éxito", f"Factura generada y enviada a {correo_cliente}")
    
    # Actualizar el inventario
        self.df_inventario.to_excel(self.file_path, index=False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()

    # Mover este código dentro de la clase donde self está definido
    print(ventana.df_inventario.columns)

    sys.exit(app.exec())