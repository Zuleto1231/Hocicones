import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.utils import formataddr


def generar_factura(nombre_archivo, datos_factura):
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    c = canvas.Canvas(nombre_archivo, pagesize=letter)
    width, height = letter

    # Título de la factura
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 50, "FACTURA ELECTRÓNICA")

    # Detalles del cliente y la fecha
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Cliente: {datos_factura['cliente']}")
    c.drawString(50, height - 100, f"Fecha: {datos_factura['fecha']}")

    # Agregar ID de la venta
    c.drawString(50, height - 120, f"ID de Venta: {datos_factura['id_venta']}")  # Aquí se muestra el ID de la venta

    # Cabecera de la tabla de productos
    y = height - 140
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Descripción")
    c.drawString(250, y, "Cantidad")
    c.drawString(350, y, "Precio Unitario")
    c.drawString(450, y, "Total")
    c.line(50, y - 10, 550, y - 10)

    # Mostrar productos y calcular totales
    total = 0
    c.setFont("Helvetica", 12)
    for item in datos_factura['items']:
        y -= 30
        c.drawString(50, y, item['descripcion'])
        c.drawString(250, y, str(item['Cantidad']))
        c.drawString(350, y, f"${item['Precio']:.2f}")
        total_item = item['Cantidad'] * item['Precio']
        c.drawString(450, y, f"${total_item:.2f}")
        total += total_item

    # Calcular impuestos y total final
    impuestos = total * 0.19
    total_final = total + impuestos

    # Detalles de totales
    c.line(50, y - 20, 550, y - 20)
    y -= 40
    c.drawString(350, y, "Subtotal:")
    c.drawString(450, y, f"${total:.2f}")
    y -= 20
    c.drawString(350, y, "Impuestos (19%):")
    c.drawString(450, y, f"${impuestos:.2f}")
    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(350, y, "Total a pagar:")
    c.drawString(450, y, f"${total_final:.2f}")

    # Guardar el archivo PDF
    c.save()

def enviar_factura(correo_cliente, nombre_cliente, archivo_factura, venta_id):
    servidor_smtp = "smtp.gmail.com"
    puerto_smtp = 587
    usuario_email = "karenliceth755@gmail.com"  
    contrasena_email = "epvl jrmb xqyx ifeu" 

    # Crear el mensaje
    msg = MIMEMultipart()
    msg['From'] = formataddr(('Hocicones', usuario_email))
    msg['To'] = correo_cliente
    msg['Subject'] = f"Factura Electrónica de {nombre_cliente} - ID Venta {venta_id}"

    # Cuerpo del mensaje
    cuerpo = f"Hola {nombre_cliente},\n\nAdjunto encontrarás la factura electrónica correspondiente a tu compra realizada en Hocicones (ID de Venta: {venta_id})."
    msg.attach(MIMEText(cuerpo, 'plain'))

    # Adjuntar la factura
    with open(archivo_factura, "rb") as archivo:
        part = MIMEApplication(archivo.read(), Name=f"factura_{venta_id}_{nombre_cliente}.pdf")
        part['Content-Disposition'] = f'attachment; filename="factura_{venta_id}_{nombre_cliente}.pdf"'
        msg.attach(part)

    # Enviar el correo
    try:
        with smtplib.SMTP(servidor_smtp, puerto_smtp) as server:
            server.starttls()  # Activar TLS (encriptación)
            server.login(usuario_email, contrasena_email)
            server.sendmail(usuario_email, correo_cliente, msg.as_string())
            print(f"Factura enviada a {correo_cliente}")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
