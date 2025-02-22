from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QMessageBox, QDialog, QComboBox,QHeaderView,QAbstractItemView,QInputDialog,QLineEdit
import pandas as pd
class VentanaDevoluciones(QDialog):
    def __init__(self, ventas, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Devoluciones")
        self.setGeometry(100, 100, 1280, 720)  # Tamaño de la ventana
        self.ventas = ventas  # Ventas que se pasan desde la ventana principal
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Título
        self.label = QLabel("Ingrese el ID de la venta para devolver productos:")
        layout.addWidget(self.label)

        # Campo para ingresar el ID de la venta
        self.input_venta_id = QLineEdit(self)
        self.input_venta_id.setPlaceholderText("ID de la Venta")
        self.input_venta_id.textChanged.connect(self.filtrar_ventas_en_combo)
        layout.addWidget(self.input_venta_id)

        # ComboBox para seleccionar la venta
        self.combo_ventas = QComboBox(self)
        self.combo_ventas.addItem("Seleccionar Venta...")  # Opción inicial
        layout.addWidget(self.combo_ventas)

        # Botón para ver los detalles de la venta
        self.btn_ver_detalles = QPushButton("Ver Detalles de Venta", self)
        self.btn_ver_detalles.clicked.connect(self.mostrar_detalles_venta)
        layout.addWidget(self.btn_ver_detalles)

        # Tabla para mostrar detalles de la venta
        self.tabla_detalles = QTableWidget(self)
        self.tabla_detalles.setColumnCount(4)
        self.tabla_detalles.setHorizontalHeaderLabels(["Producto", "Cantidad", "Precio", "Total"])
        layout.addWidget(self.tabla_detalles)
        self.tabla_detalles.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Botón para realizar la devolución
        self.btn_devolver = QPushButton("Realizar Devolución", self)
        self.btn_devolver.clicked.connect(self.realizar_devolucion)
        layout.addWidget(self.btn_devolver)

        self.tabla_detalles.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla_detalles.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

        # Establecer el layout de la ventana
        self.setLayout(layout)

    def filtrar_ventas_en_combo(self):
        """Filtra las ventas por ID en tiempo real y las muestra en el ComboBox."""
        venta_id_input = self.input_venta_id.text()
    
    # Limpiar las opciones del ComboBox
        self.combo_ventas.clear()
        self.combo_ventas.addItem("Seleccionar Venta...")  # Añadir la opción inicial

    # Filtrar las ventas por el ID ingresado
        ventas_filtradas = [venta for venta in self.ventas if str(venta['ID']).startswith(venta_id_input)]

    # Agregar las ventas filtradas al ComboBox
        for venta in ventas_filtradas:
            self.combo_ventas.addItem(f"ID: {venta['ID']} - Cliente: {venta['Cliente']}", venta['ID'])  # Asignar ID como dato adicional

    def mostrar_detalles_venta(self):
        """Muestra los detalles de la venta seleccionada en la tabla."""
    # Obtener el ID de la venta seleccionada desde el ComboBox
        venta_id = self.combo_ventas.currentData()

        if venta_id is None:
            QMessageBox.warning(self, "Error", "Seleccione una venta de la lista.")
            return

    # Buscar la venta seleccionada por su ID
        venta = next((v for v in self.ventas if v['ID'] == venta_id), None)

        if not venta:
            QMessageBox.warning(self, "Error", "Venta no encontrada.")
            return

    # Mostrar los productos de la venta seleccionada
        self.tabla_detalles.setRowCount(len(venta['productos']))

        for i, producto in enumerate(venta['productos']):
            self.tabla_detalles.setItem(i, 0, QTableWidgetItem(producto["producto"]))
            self.tabla_detalles.setItem(i, 1, QTableWidgetItem(str(producto["cantidad"])))
            self.tabla_detalles.setItem(i, 2, QTableWidgetItem(str(producto["precio"])))
            self.tabla_detalles.setItem(i, 3, QTableWidgetItem(f"${producto['total']:.0f}"))

    def realizar_devolucion(self):
        selected_rows = self.tabla_detalles.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Error", "Seleccione al menos un producto para devolver.")
            return

        productos_devueltos = []

        for row in selected_rows:
            row_index = row.row()
            producto = self.tabla_detalles.item(row_index, 0).text()
            cantidad_original = int(self.tabla_detalles.item(row_index, 1).text())

            # Pedir la cantidad a devolver
            cantidad_a_devolver, ok = QInputDialog.getInt(
                self, "Cantidad a devolver",
                f"Ingrese la cantidad a devolver para '{producto}':",
                min=1, max=cantidad_original
            )

            if ok and cantidad_a_devolver > 0:
                productos_devueltos.append((producto, cantidad_a_devolver))

        if not productos_devueltos:
            return  # Si el usuario canceló, no hacer nada

        confirmacion = QMessageBox.question(
            self, "Confirmar Devolución",
            f"¿Está seguro de devolver los productos seleccionados?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if confirmacion == QMessageBox.StandardButton.Yes:
            try:
                file_path = "BD.xlsx"
                # Leer las hojas de Inventario y Ventas
                df_inventario = pd.read_excel(file_path, sheet_name="Sheet1")
                ventas_df = pd.read_excel(file_path, sheet_name="Ventas")

                # Obtener el ID de la venta seleccionada
                venta_id = self.combo_ventas.currentData()  # Usar currentData() para obtener el ID
                venta = next((v for v in self.ventas if v['ID'] == venta_id), None)

                if not venta:
                    QMessageBox.warning(self, "Error", "Venta no encontrada.")
                    return

                for producto, cantidad_a_devolver in productos_devueltos:
                    # Buscar el producto en la base de datos (Inventario)
                    producto_index = df_inventario[df_inventario["Producto"] == producto].index

                    if not producto_index.empty:
                        # Aumentar el stock del producto
                        df_inventario.loc[producto_index, "Stock"] += cantidad_a_devolver

                    # Encontrar el producto en la venta y reducir la cantidad
                    producto_index_venta = next((i for i, p in enumerate(venta['productos']) if p["producto"] == producto), None)

                    if producto_index_venta is not None:
                        # Reducir la cantidad del producto en la venta
                        venta['productos'][producto_index_venta]["cantidad"] -= cantidad_a_devolver

                        # Si la cantidad en la venta es 0, eliminar el producto
                        if venta['productos'][producto_index_venta]["cantidad"] == 0:
                            venta['productos'].pop(producto_index_venta)

                        # Si queda al menos un producto, actualizamos la cantidad en la hoja de ventas
                        elif venta['productos'][producto_index_venta]["cantidad"] > 0:
                            for idx, row in ventas_df.iterrows():
                                if row["ID"] == venta['ID'] and row["Producto"] == producto:
                                    ventas_df.at[idx, "Cantidad"] = venta['productos'][producto_index_venta]["cantidad"]

                # Guardar los cambios en el archivo Excel
                with pd.ExcelWriter(file_path, engine="openpyxl", mode="w") as writer:
                    # Guardamos las actualizaciones de la hoja de Inventario y Ventas
                    df_inventario.to_excel(writer, sheet_name="Sheet1", index=False)
                    ventas_df.to_excel(writer, sheet_name="Ventas", index=False)

                QMessageBox.information(self, "Devolución Exitosa", "Se han devuelto los productos correctamente.")
                self.mostrar_detalles_venta()  # Refrescar la tabla de detalles de venta

            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo actualizar el stock en la base de datos.\n{str(e)}")
