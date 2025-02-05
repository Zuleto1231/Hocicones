import pandas as pd
from datetime import datetime
from FacruraElectronica import *

def ingreso_de_productos():
    print(" ,--,    ,----..                                     ,----..            ,--.                       ")
    print("      ,--.'|   /   /   \\    ,----..     ,---,  ,----..     /   /   \\         ,--.'|    ,---,.  .--.--.    ")
    print("   ,--,  | :  /   .     :  /   /   \\ ,`--.' | /   /   \\   /   .     :    ,--,:  : |  ,'  .' | /  /    '.  ")
    print(",---.'|  : ' .   /   ;.  \\|   :     :|   :  :|   :     : .   /   ;.  \\,`--.'`|  ' :,---.'   ||  :  /`. /  ")
    print("|   | : _' |.   ;   /  ` ;.   |  ;. /:   |  '.   |  ;. /.   ;   /  ` ;|   :  :  | ||   |   .';  |  |--`   ")
    print(":   : |.'  |;   |  ; \\ ; |.   ; /--` |   :  |.   ; /--` ;   |  ; \\ ; |:   |   \\ | ::   :  |-,|  :  ;_     ")
    print("|   ' '  ; :|   :  | ; | ';   | ;    '   '  ;;   | ;    |   :  | ; | '|   : '  '; |:   |  ;/| \\  \\    `.  ")
    print("'   |  .'. |.   |  ' ' ' :|   : |    |   |  ||   : |    .   |  ' ' ' :'   ' ;.    ;|   :   .'  `----.   \\ ")
    print("|   | :  | ''   ;  \\; /  |.   | '___ '   :  ;.   | '___ '   ;  \\; /  ||   | | \\   ||   |  |-,  __ \\  \\  | ")
    print("'   : |  : ; \\   \\  ',  / '   ; : .'||   |  ''   ; : .'| \\   \\  ',  / '   : |  ; .''   :  ;/| /  /`--'  / ")
    print("|   | '  ,/   ;   :    /  '   | '/  :'   :  |'   | '/  :  ;   :    /  |   | '`--'  |   |    \\'--'.     /  ")
    print(";   : ;--'     \\   \\ .'   |   :    / ;   |.' |   :    /    \\   \\ .'   '   : |      |   :   .'  `--'---'   ")
    print("|   ,/          `---`      \\   \\ .'  '---'    \\   \\ .'      `---`     ;   |.'      |   | ,'               ")
    print("'---'                       `---`              `---`                  '---'        `----'                 ")
    print("==========================================================================================================")
    print("|| ¡Bienvenido a Hocicones!                                                                              ||")
    print("==========================================================================================================")
    print("|| Por favor, ingrese los productos que va a vender                                                     ||")
    print("==========================================================================================================")
    print("|| Recuerde seguir el siguiente formato: producto cantidad precio                                       ||")
    print("==========================================================================================================")
    print("|| Ejemplo: Dog Chow 2 5000                                                                             ||")
    print("==========================================================================================================")
    print("|| Para finalizar, escriba 'fin'                                                                        ||")
    print("==========================================================================================================")
    print("\n"*2)

    # Indice de la cantidad de productos de una venta
    indice = 1
    # DataFrame donde se guardan los productos de la venta
    df = pd.DataFrame(columns=['Producto', 'Cantidad', 'Precio', 'Costo Total'])

    # Ciclo de ejecución hasta que el usuario decida finalizar la venta
    while True:
        # Preguntamos por el próximo producto
        venta = input(f"Ingrese el producto {indice}: ").split()

        # Si la venta es igual a "fin", se finaliza la venta
        if venta[0] == "fin":
            
            # Recoger datos del cliente
            print("\nPor favor, ingrese los datos del cliente para generar la factura.")
            nombre_cliente = input("Nombre del cliente: ")
            correo_cliente = input("Correo del cliente: ")
            fecha_venta = datetime.now().strftime("%d/%m/%Y")  # Fecha actual

            # Mostramos un resumen de la venta
            print("\nLa venta fue la siguiente:")
            print(df)

            # Calculamos el costo total de la venta
            calculo_costo_total(df)

            # Ingresamos la venta a la base de datos
            ingreso_venta_BD(df)

            # Generamos los productos para pasar a la factura en el formato esperado
            items = []
            for idx, row in df.iterrows():
                item = {
                    'descripcion': row['Producto'],
                    'cantidad': row['Cantidad'],
                    'precio_unitario': row['Precio']
                }
                items.append(item)

            # Generar los datos para la factura
            datos_factura = {
                "cliente": nombre_cliente,
                "correo": correo_cliente,
                "fecha": fecha_venta,
                "items": items  # Aquí pasamos la lista de productos
            }         
            directorio_facturas = "Facturas/"
            os.makedirs(directorio_facturas, exist_ok=True)  # Crea la carpeta si no existe
            archivos_existentes = os.listdir(directorio_facturas)
            numeros_facturas = [int(f.split("_")[1].split(".")[0]) for f in archivos_existentes if f.startswith("factura_") and f.endswith(".pdf")]
            nuevo_numero = max(numeros_facturas) + 1 if numeros_facturas else 1  # Si no hay facturas, empieza en 1
            nombre_factura = f"factura_{nuevo_numero}.pdf"  
            ruta_factura = os.path.join(directorio_facturas, nombre_factura)
            generar_factura(ruta_factura, datos_factura)
            print(f"Factura generada en: {ruta_factura}")
            # Generar la factura PDF
            nombre_factura = f"factura_{fecha_venta}.pdf"
            generar_factura(ruta_factura, datos_factura)
            enviar_factura(correo_cliente, nombre_cliente, ruta_factura)
            print(f"Factura generada y enviada a {correo_cliente}")
            break
        
        elif venta[0] == "fin" and indice == 1:
            print("No se ingresaron productos")
            continue

        elif venta[0] == 'borrar':
            borrar_producto(df)
            continue

        elif venta[0] == 'borrar' and indice == 1:
            print("No hay productos para borrar")
            continue

        elif venta[0] == 'mostrar':
            print("\n"*2)
            print(df)
            print("\n"*2)
            continue

        else:
            try:
                producto = venta[0]
                cantidad = int(venta[1])
                precio = int(venta[2])
                costo_total = cantidad * precio
                df = df._append({'Producto': producto, 'Cantidad': cantidad, 'Precio': precio, 'Costo Total': costo_total}, ignore_index=True)
                indice += 1
            except:
                print("Error en el formato de ingreso o comando no existente")
                continue
    
def calculo_costo_total(df):
    costo_total = df['Costo Total'].sum() 
    iva = costo_total * 0.19
    totaliva = iva + costo_total
    print("\nEl costo total de la venta es: $", totaliva)

def ingreso_venta_BD(df):
    pass

def creacion_recibo(df):
    pass

def borrar_producto(df):
    print("\n"*2)
    print("¿Qué producto desea borrar?")
    print("\n"*2)
    print(df)
    print("\n"*2)
    producto = int(input("Ingrese el índice del producto a borrar: "))
    df.drop(producto, inplace=True)
    print("Producto borrado")
    print("\n"*2)

if __name__ == "__main__":
    ingreso_de_productos()
