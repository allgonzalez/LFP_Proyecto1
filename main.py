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

while opcion != 7:
    print('1. Ingresar archivo')
    print('2. Procesar archivo')
    print('3. Generar reporte de Tokens')
    print('4. Generar reporte de Errores')
    print('5. Generar Arreglos')
    print('6. Imprimir arreglos')
    print('7. Salir')
    
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
        lexico.arreglosColores()
    
    elif opcion == 6:
        print('-------------------------------')
        lexico.Pintar()
        print('')
    
    elif opcion == 7:
        break
