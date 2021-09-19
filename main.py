from Analizador import Analizador
from io import open

def Leer_Archivos(entrada):
    archivos_texto = open(entrada, 'r')
    texto = archivos_texto.read()
    return texto

print('--------------------Analizador Léxico------------------------')
entrada = ''
opcion = 0
lexico = Analizador()

while opcion != 11:
    print('1. Ingresar archivo')
    print('2. Procesar archivo')
    print('3. Procesar Archivo')
    print('4. Generar reporte de Errores')
    print('5. Generar Arreglos')
    print('6. Imprimir arreglos')
    print('7. Filas y Columnas')
    print('8. Nombres')
    print('9. Filtros')
    print('10. Tamaños')
    print('11.Salir')
    
    opcion = int(input('>Ingrese una opción: '))

    if opcion == 1:
        archivo = input('Ingrese el nombre del archivo con extensión ".pxla": ')
        entrada = Leer_Archivos(archivo)
    
    elif opcion == 2:
        lexico.scanner(entrada)
    
    elif opcion == 3:
        print('-------------------------------')
        lexico.imprimirTokens()
        print('')
    
    elif opcion == 4: 
        lexico.imprimirErrores()
        print('')
    
    elif opcion == 5:
        lexico.arreglosCeldasPintar()
    
    elif opcion == 6:
        print('-------------------------------')
        lexico.arregloNombres()
        nombre = input('Ingrese el nombre a procesar: ')
        lexico.Pintar(nombre)
        
        print('')
    elif opcion == 7:
        lexico.arregloColFil()
    elif opcion == 8:
        lexico.arregloNombres()
    
    elif opcion == 9:
        lexico.arreglosFiltros()
    
    elif opcion == 10:
        lexico.arregloTamaños()

    elif opcion == 11:
        break

