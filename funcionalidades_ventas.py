import pandas as pd

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


    #Indice de la cantidad de productos de una venta
    indice = 1
    #dataframe donde se guardan los productos de la venta
    df = pd.DataFrame(columns=['Producto', 'Cantidad', 'Precio', 'Costo Total'])

    #ciclo de ejecucion hasta que el usuario decida finalizar la venta [producto, cantidad, precio]
    while True:
        #preguntamos por el proximo producto 
        venta = input(f"Ingrese el producto {indice}: ").split() 

        #si la venta es igual a "fin" se finaliza la venta
        if venta[0] == "fin":
            
            #mostramos un resumen de la venta
            print("\n La venta fue la siguiente:")
            print(df)

            #calculamos el costo total de la venta y lo mostramos
            calculo_costo_total(df)

            #ingresamos la venta a la base de datos
            ingreso_venta_BD(df)

            #generamos el recibo del cliente
            creacion_recibo(df)
            
            #finalizamos el programa
            break

        #si no se ingresaron productos continuamos con el ciclo
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
                costo_total= cantidad * precio
                df = df._append({'Producto': producto, 'Cantidad': cantidad, 'Precio': precio, 'Costo Total': costo_total}, ignore_index=True)
                indice += 1
            except:
                print("Error en el formato de ingreso o comando no existente")
                continue
    
def calculo_costo_total(df):
    costo_total = df['Costo Total'].sum()
    print("\nEl costo total de la venta es: $", costo_total)

def ingreso_venta_BD(df):
    pass

def creacion_recibo(df):
    pass

def borrar_producto(df):
    print("\n"*2)
    print("Cual producto desea borrar?")
    print("\n"*2)
    print(df)
    print("\n"*2)
    producto = int(input("Ingrese el indice del producto a borrar: "))
    df.drop(producto, inplace=True)
    print("Producto borrado")
    print("\n"*2)
    indice -= 1


if __name__ == "__main__":
    ingreso_de_productos()