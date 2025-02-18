import random
import openpyxl
import pandas as pd
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
import sys
import pandas as pd
from PyQt6.QtWidgets import (QApplication,  QVBoxLayout, QPushButton,
                             QLabel,  QTableWidget, QTableWidgetItem,
                             QMessageBox,)

from PyQt6.QtWidgets import QApplication, QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt6.QtWidgets import QDialog, QVBoxLayout,QLabel, QPushButton
from Login import *
from GuardarVentas import *


class VentanaDevoluciones(QDialog):
    def __init__(self, ventas, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Devoluciones")
        self.setGeometry(100, 100, 1280, 720)  # Tamaño de la ventana
        self.ventas = ventas  # Venta se pasa desde la ventana principal
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Título
        self.label = QLabel("Selecciona una venta para devolver productos:")
        layout.addWidget(self.label)

        # ComboBox para seleccionar la venta
        self.combo_ventas = QComboBox(self)
        for venta in self.ventas:  # Suponiendo que 'ventas' es una lista de ventas con un ID único
            self.combo_ventas.addItem(f"ID: {venta['ID']} - Cliente: {venta['Cliente']}")  # Mostrar ID y cliente
        layout.addWidget(self.combo_ventas)

        # Botón para seleccionar la venta
        self.btn_ver_detalles = QPushButton("Ver Detalles de Venta", self)
        self.btn_ver_detalles.clicked.connect(self.mostrar_detalles_venta)
        layout.addWidget(self.btn_ver_detalles)

        # Tabla para mostrar detalles de la venta
        self.tabla_detalles = QTableWidget(self)
        self.tabla_detalles.setColumnCount(4)
        self.tabla_detalles.setHorizontalHeaderLabels(["Producto", "Cantidad", "Precio", "Total"])
        layout.addWidget(self.tabla_detalles)

        # Botón para realizar la devolución
        self.btn_devolver = QPushButton("Realizar Devolución", self)
        self.btn_devolver.clicked.connect(self.realizar_devolucion)
        layout.addWidget(self.btn_devolver)

        # Establecer el layout de la ventana
        self.setLayout(layout)

    def mostrar_detalles_venta(self):
        venta_id = self.combo_ventas.currentIndex()
        venta = self.ventas[venta_id]  # Venta seleccionada

        self.tabla_detalles.setRowCount(len(venta['productos']))  # Mostrar los productos de la venta seleccionada

        for i, producto in enumerate(venta['productos']):
            self.tabla_detalles.setItem(i, 0, QTableWidgetItem(producto["producto"]))
            self.tabla_detalles.setItem(i, 1, QTableWidgetItem(str(producto["cantidad"])))
            self.tabla_detalles.setItem(i, 2, QTableWidgetItem(str(producto["precio"])))
            self.tabla_detalles.setItem(i, 3, QTableWidgetItem(f"${producto['total']:.2f}"))

    def realizar_devolucion(self):
        selected_row = self.tabla_detalles.currentRow()
        if selected_row >= 0:
            producto = self.tabla_detalles.item(selected_row, 0).text()
            cantidad = int(self.tabla_detalles.item(selected_row, 1).text())
            QMessageBox.information(self, "Devolución", f"Producto '{producto}' devuelto. Cantidad: {cantidad}")
            # Aquí deberías actualizar la base de datos o archivo Excel para reflejar la devolución
            self.close()