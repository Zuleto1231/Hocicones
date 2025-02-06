import pandas as pd
from datetime import datetime
from openpyxl import *
from FacturaElectronica import *

# Cargar el inventario desde Excel
file_path = "BD.xlsx"
df_inventario = pd.read_excel(file_path)

# Eliminar espacios extra en los nombres de las columnas
df_inventario.columns = df_inventario.columns.str.strip()


def ingreso_de_productos():
    print(" ,--,    ,----..                                     ,----..            ,--.                       ")
    print("      ,--.'|   /   /   \\    ,----..     ,---,  ,----..     /   /   \\         ,--.'|    ,---,.  .--.--.    ")
    print("   ,--,  | :  /   .     :  /   /   \\`--.' | /   /   \\   /   .     :    ,--,:  : |  ,'  .' | /  /    '.  ")
    print(",---.'|  : ' .   /   ;.  \\\|   :     :|   :  :|   :     : .   /   ;.  \\\,`--.'`|  ' :,---.'   ||  :  /`. /  ")
    print("|   | : _' |.   ;   /  ` ;.   |  ;. /:   |  '.   |  ;. /.   ;   /  ` ;|   :  :  | ||   |   .';  |  |--`   ")
    print(":   : |.'  |;   |  ; \\ ; |.   ; /--` |   :  |.   ; /--` ;   |  ; \\ ; |:   |   \\ | ::   :  |-,|  :  ;_     ")
    print("|   ' '  ; :|   :  | ; | ';   | ;    '   '  ;;   | ;    |   :  | ; | '|   : '  '; |:   |  ;/| \\  \\    `.  ")
    print("'   |  .'. |.   |  ' ' ' :|   : |    |   |  ||   : |    .   |  ' ' ' :'   ' ;.    ;|   :   .'  `----.   ")
    print("|   | :  | ''   ;  \\; /  |.   | '___ '   :  ;.   | '___ '   ;  \\; /  ||   | | \\   ||   |  |-,  __ \\  \\  | ")
    print("'   : |  : ; \\   \\  ',  / '   ; : .'||   |  ''   ; : .'| \\   \\  ',  / '   : |  ; .''   :  ;/| /  /`--'  / ")
    print("|   | '  ,/   ;   :    /  '   | '/  :'   :  |'   | '/  :  ;   :    /  |   | '`--'  |   |    \\\'--'.     /  ")
    print(";   : ;--'     \\   \\ .'   |   :    / ;   |.' |   :    /    \\   \\ .'   '   : |      |   :   .'  `--'---'   ")
    print("|   ,/          `---`      \\   \\ .'  '---'    \\   \\ .'      `---`     ;   |.'      |   | ,'               ")
    print("'---'                       `---`              `---`                  '---'        `----'                 ")
    print("==========================================================================================================")
    print("|| ¡Bienvenido a Hocicones!                                                                              ||")
    print("==========================================================================================================")
    print("|| Por favor, ingrese los productos que va a vender                                                     ||")
    print("==========================================================================================================")
    print("|| Ingrese el ID del producto y la cantidad a vender                                                   ||")
    print("==========================================================================================================")
    print("|| Para finalizar, escriba 'fin'                                                                        ||")
    print("==========================================================================================================")
    print("\n"*2)
    
    df_ventas = pd.DataFrame(columns=['Producto', 'Cantidad', 'Precio', 'Costo Total'])
    
    while True:
        entrada = input("Ingrese el ID del producto y la cantidad y fin cuando desees finalizar el registro de venta: ").split()    
        if entrada[0].lower() == "fin":
            break 
        try:
            
            producto_id = int(entrada[0])
            cantidad_vendida = int(entrada[1])
            producto = df_inventario[df_inventario['ID'] == producto_id]
            
            if producto.empty:
                print("ID de producto no encontrado.")
                continue
            
            stock_disponible = producto.iloc[0]['Stock']
            precio_venta = producto.iloc[0]['P_Venta']
            
            if cantidad_vendida > stock_disponible:
                print(f"Stock insuficiente. Solo hay {stock_disponible} unidades disponibles.")
                continue
            
            # Actualizar el inventario
            df_inventario.loc[df_inventario['ID'] == producto_id, 'Stock'] -= cantidad_vendida
            
            # Calcular costo total
            costo_total = cantidad_vendida * precio_venta 
            IVA = costo_total * 0.19
            total = costo_total + IVA
            # Agregar venta al DataFrame
            nueva_fila = pd.DataFrame([{
                'Producto': producto.iloc[0]['Producto'],
                'Cantidad': cantidad_vendida,
                'Precio': precio_venta,
                'Costo Total': total }])
            if df_ventas.empty:
                 df_ventas = nueva_fila
            else:
                df_ventas = pd.concat([df_ventas, nueva_fila], ignore_index=True)            
        except ValueError:
            print("Error en el formato de ingreso. Use: ID|Numero")
            continue
        
    
    # Guardar cambios en el inventario
    df_inventario.to_excel(file_path, index=False)

    # Imprimir resumen de la compra
    if not df_ventas.empty:
        print("\nResumen de la compra:")
        print(df_ventas.to_string(index=False))  # Imprime todos los productos comprados
    else:
        print("No se realizaron ventas.")



    while True:
        respuesta = input("¿Desea devolver algún producto? (sí/no): ").strip().lower()
        
        if respuesta == 'sí':
#########            #df_ventas, df_inventario = devolver_producto(df_ventas, df_inventario)
#####           #total_venta = mostrar_resumen_venta(df_ventas)
####        #elif respuesta == 'no':
            print("Compra confirmada.")
            break
        else:
            print("Respuesta no válida. Por favor ingrese 'sí' o 'no'.")

    # Generar factura
    print("Generando factura...")
    # Generar la factura aquí
    #generar_factura(ruta_factura, datos_factura)

    # Guardar cambios en el inventario
    df_inventario.to_excel("BD.xlsx", index=False)
    print("Inventario actualizado y guardado.")

    #GENERAR Y MANDAR LA FACTURA    
    items = []
    nombre_cliente = input("Nombre del cliente: ")
    correo_cliente = input("Correo del cliente: ")
    fecha_venta = datetime.now().strftime("%d/%m/%Y")  # Fecha actual
    items = []
    for idx, row in df_ventas.iterrows():
        item = {
                'descripcion': row['Producto'],
                'Cantidad': row['Cantidad'],
                'Precio': row['Precio'],
                'Costo Total': row['Costo Total']
                }
        items.append(item)

            # Generar los datos para la factura
        datos_factura = {
            "cliente": nombre_cliente,
            "correo": correo_cliente,
            "fecha": fecha_venta,
            "items": items  # Aquí pasamos la lista de producto
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

if __name__ == "__main__":
    ingreso_de_productos()
