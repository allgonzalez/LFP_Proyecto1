from io import open
from os import truncate
from Tokens import Token
import webbrowser
from Pintar import Pintar

class Analizador:
    #Variable que guardará lo que vaya recorriendo poco a poco
    lexema = ''
    #Arreglo de tokens
    tokens = []
    #EStados para ir distribuyendo los distintos símbolos encontrados
    estado = 1
    #Fila en la que estoy
    fila = 1
    #Columna en la que estoy 
    columna = 1
    #Ayuda a ver si generamos un reporte de errores por si hay símbolos que son desconocidos
    generarErrores = False

    #Arreglo para ver que vamos a pintar
    celdasPintar = []

    #Creamos nuestro scanner que hará todo el trabajo de analisis 

    def scanner(self, entrada):
        #Manejo de tipos
        global tipos
        tipos = Token("random", 0, 0,0) #Llenamos de datos random
        self.estado = 1
        self.lexema = ''
        self.tokens = []
        self.fila = 1
        self.columna = 1
        self.generarErrores = False

        entrada = entrada + '$'
        actual = ''
        longitud = len(entrada)

        for i in range(longitud):
            actual = entrada[i]

            if self.estado == 1:
                if actual.isalpha(): #Se verifica si es alfabetico [a-zA-Z]
                    self.estado = 2  #Agregamos los estados para ir concatenando
                    self.columna += 1
                    self.lexema += actual
                    continue

                elif actual.isdigit(): #VErificamos si es dígito [0-9]
                    self.estado = 4
                    self.columna += 1
                    self.lexema += actual
                
                elif actual == '"':
                    self.estado = 5
                    self.columna += 1
                    self.lexema += actual
                
                elif actual == '=':  
                    self.columna += 1
                    self.lexema += actual
                    self.agregarToken(tipos.IGUAL) #Como el igual no es signo que se combine con otros mas se agrega a la lista de tokens
                
                elif actual == '{':
                    self.columna += 1
                    self.lexema += actual
                    self.agregarToken(tipos.LLAVE_I)
                elif actual == '}':
                    self.columna += 1
                    self.lexema += actual
                    self.agregarToken(tipos.LLAVE_D)
                
                elif actual == '[':
                    self.columna += 1
                    self.lexema += actual
                    self.agregarToken(tipos.CORCHETE_I)
                elif actual == ']':
                    self.columna += 1
                    self.lexema += actual
                    self.agregarToken(tipos.CORCHETE_D)
                
                elif actual == ',':
                    self.columna += 1
                    self.lexema += actual
                    self.agregarToken(tipos.COMA)
                
                elif actual == ';':
                    self.columna += 1
                    self.lexema += actual
                    self.agregarToken(tipos.PUNTO_COMA)
                
                #Agregamos para los colores
                elif actual == '#':
                    self.estado = 6
                    self.columna += 1
                    self.lexema += actual
                
                #Ver si es un separador
                elif actual == '@':
                    self.estado = 7  #Estado para el manejo de los separadores
                    self.columna += 1
                    self.lexema += actual

                elif actual == ' ':
                    self.columna += 1
                    self.estado = 1
                
                elif actual == '\n':
                    self.fila += 1
                    self.columna = 1
                    self.estado = 1
                
                elif actual == '\r':
                    self.estado = 1
                
                elif actual == '\t':
                    self.columna += 5
                    self.estado = 1
                

                elif actual == '$' and i == longitud-1:
                    print('Análisis finalizado con éxito :) ')
                
                else:
                    self.lexema += actual
                    self.columna += 1
                    self.agregarToken(tipos.DESCONOCIDO)
                    self.generarErrores = True

            #Estado para palabras reservadas y booleanos      
            elif self.estado == 2:
                if actual.isalpha():
                    self.estado = 2
                    self.columna += 1
                    self.lexema += actual
                    continue
                elif actual.isdigit():
                    self.estado = 3
                    self.columna += 1
                    self.lexema += actual
                    continue
                else:
                    if self.palabra_reservada(self.lexema):
                        self.agregarToken(tipos.PALABRA_RESERVADA)
                        if actual == ";":
                            self.lexema = actual
                            self.columna += 1
                            self.agregarToken(tipos.PUNTO_COMA)
                        elif actual == ",":
                            self.lexema = actual
                            self.columna += 1
                            self.agregarToken(tipos.COMA)
                        elif actual == "=":
                            self.lexema = actual
                            self.columna += 1
                            self.agregarToken(tipos.IGUAL)
                        elif actual == ' ':
                            self.columna +=1    
                        
                    elif self.booleanos(self.lexema):
                        self.agregarToken(tipos.BOOLEANOS)
                        if actual == ',':
                            self.lexema = actual
                            self.columna += 1
                            self.agregarToken(tipos.COMA)
                        elif actual == ' ':
                            self.columna += 1
                    else:
                        self.agregarToken(tipos.DESCONOCIDO)
                        self.generarErrores = True
           
            #Estado de errores
            elif self.estado == 3:
                if actual.isalpha():
                    self.estado = 3
                    self.columna += 1
                    self.lexema += actual
                    continue
                elif actual.isdigit():
                    self.estado = 3
                    self.columna += 1
                    self.lexema += actual
                    continue
                else:
                    self.agregarToken(tipos.DESCONOCIDO)
                    self.generarErrores = True
            
            #Estado para los numeros
            elif self.estado == 4:
                if actual.isdigit():
                    self.estado = 4
                    self.columna +=1
                    self.lexema += actual
                else:
                    if actual == ',' or ' ' or ';':
                        self.agregarToken(tipos.NUMERO)
                        self.lexema = actual
                        self.columna += 1
                        if actual == ',':
                            self.agregarToken(tipos.COMA)
                        elif actual == ';':
                            self.agregarToken(tipos.PUNTO_COMA)
            
            #Estado para las cadenas
            elif self.estado == 5:
                if actual != '"':
                    self.estado = 5
                    self.columna += 1
                    self.lexema += actual
        
                elif actual == '"':
                    self.lexema += actual
                    self.columna += 1
                    self.agregarToken(tipos.CADENA)

            #Estado para los colores
            elif self.estado == 6:
                if actual != '#' and actual!= ']' and actual != ' ':
                    self.estado = 6
                    self.columna += 1
                    self.lexema += actual
                elif actual == ']':
                    self.agregarToken(tipos.COLOR)
                    self.lexema = actual
                    self.columna += 1
                    self.agregarToken(tipos.CORCHETE_D)
                elif actual == ' ':
                    self.agregarToken(tipos.COLOR)
                    self.columna += 1
            #Estado para los separadores
            elif self.estado == 7:
                if actual == '@':
                    self.estado = 7
                    self.columna += 1
                    self.lexema += actual
                    if self.lexema == "@@@@":
                        self.agregarToken(tipos.SEPARADOR)
                else:
                    self.lexema += actual
                    self.columna += 1
                    self.agregarToken(tipos.DESCONOCIDO)
                    self.generarErrores = True

    #Funcion para ir agregando nuestros tokens
    def agregarToken(self,tipo):
        self.tokens.append(Token(self.lexema, tipo, self.fila, self.columna))
        self.lexema = ""
        self.estado = 1
    
    #Funcion para verificar si tenemos palabras reservadas
    def palabra_reservada(self, entrada = ''):
        entrada = entrada.lower()
        reservada = False
        reservadas = ['titulo','alto', 'ancho', 'filas', 'columnas', 'celdas', 'filtros', 'mirrorx', 'mirrory', 'doublemirror']

        if entrada in reservadas:
            reservada = True
        return reservada
    
    #Función para detectar booleanos
    def booleanos(self, entrada = ''):
        entrada = entrada.lower()
        booleano = False
        booleanos = ['true', 'false']

        if entrada in booleanos:
            booleano = True
        return booleano
    
    def imprimirTokens(self):
        print('---------------------Tokens Válidos-----------------')
        for i in self.tokens:
            if i.tipo != tipos.DESCONOCIDO:
                print('Lexema : ',i.getLexema(),' Tipo : ',i.getTipo(), ' Fila : ', i.getFila(), ' Columna : ', i.getColumna())

        docHTML = open('reporteTokensValidos.html', 'w')
        docHTML.write('\n<!DOCTYPE html>')
        docHTML.write('\n<html lang="es">')
        docHTML.write('\n<meta charset="utf-8">')
        docHTML.write('\n<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">')
        docHTML.write('\n<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">')
        docHTML.write('\n<title>Reporte de Tokens</title>')
        docHTML.write('\n</head>')
        docHTML.write('\n<body>')
        docHTML.write('\n<div class="container">')
        docHTML.write('\n <h4 class= "text-center"> Lista de Tokens Validos </h4>')
        docHTML.write('\n<div>')
        docHTML.write('\n<div class="container">')
        docHTML.write('\n<table class="table" border="1">')    
        docHTML.write('\n\t <thead class="thead-dark">')
        docHTML.write('\n\t\t <tr>')
        docHTML.write('\n\t\t\t<th scope = "col">Token</th>')
        docHTML.write('\n\t\t\t<th scope = "col">Lexema</th>')
        docHTML.write('\n\t\t\t<th scope = "col">Fila</th>')
        docHTML.write('\n\t\t\t<th scope = "col">Columna</th>')
        docHTML.write('\n\t\t </tr>')
        docHTML.write('\n\t </thead>')
        docHTML.write('\n\t <tbody>')
        
        for i in self.tokens:
            if i.tipo != tipos.DESCONOCIDO:
                docHTML.write('\n\t\t <tr class="table-success">')
                docHTML.write('\n\t\t\t<th scope = "row">'+str(i.getTipo()))
                docHTML.write('</th>')
                docHTML.write('\n\t\t\t<td>'+str(i.getLexema()))
                docHTML.write('</td>')
                docHTML.write('\n\t\t\t<td>'+ str(i.getFila()))
                docHTML.write('</td>')
                docHTML.write('\n\t\t\t<td>'+ str(i.getColumna()))
                docHTML.write('</td>')
                docHTML.write('\n\t\t </tr>')

        docHTML.write('\n\t </tbody>')
        docHTML.write('\n</table>')
        docHTML.write('\n</div>')  
        docHTML.write('\n</body')
        docHTML.write('\n</html>')
        
        docHTML.close()

        webbrowser.open_new_tab('reporteTokensValidos.html')

        
    
    def imprimirErrores(self):
        if self.generarErrores:
            print('------------------------Errores----------------------')
            for i in self.tokens :
                if i.tipo == tipos.DESCONOCIDO:
                    print('Lexema : ', i.getLexema(), ' Fila : ', i.getFila(), ' Columna : ', i.getColumna())
            
            docHTML = open('reporteTokensErrores.html', 'w')
            docHTML.write('\n<!DOCTYPE html>')
            docHTML.write('\n<html lang="es">')
            docHTML.write('\n<meta charset="utf-8">')
            docHTML.write('\n<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">')
            docHTML.write('\n<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">')
            docHTML.write('\n<title>Reporte de Tokens</title>')
            docHTML.write('\n</head>')
            docHTML.write('\n<body>')
            docHTML.write('\n<div class="container">')
            docHTML.write('\n <h4 class= "text-center"> Lista de Tokens con Errores </h4>')
            docHTML.write('\n<div>')
            docHTML.write('\n<div class="container">')
            docHTML.write('\n<table class="table" border="1">')    
            docHTML.write('\n\t <thead class="thead-dark">')
            docHTML.write('\n\t\t <tr>')
            docHTML.write('\n\t\t\t<th scope = "col">Token</th>')
            docHTML.write('\n\t\t\t<th scope = "col">Lexema</th>')
            docHTML.write('\n\t\t\t<th scope = "col">Fila</th>')
            docHTML.write('\n\t\t\t<th scope = "col">Columna</th>')
            docHTML.write('\n\t\t </tr>')
            docHTML.write('\n\t </thead>')
            docHTML.write('\n\t <tbody>')
        
            for i in self.tokens:
                if i.tipo == tipos.DESCONOCIDO:
                    docHTML.write('\n\t\t <tr class="table-danger">')
                    docHTML.write('\n\t\t\t<th scope = "row">'+'DESCONOCIDO')
                    docHTML.write('</th>')
                    docHTML.write('\n\t\t\t<td>'+str(i.getLexema()))
                    docHTML.write('</td>')
                    docHTML.write('\n\t\t\t<td>'+ str(i.getFila()))
                    docHTML.write('</td>')
                    docHTML.write('\n\t\t\t<td>'+ str(i.getColumna()))
                    docHTML.write('</td>')
                    docHTML.write('\n\t\t </tr>')

            docHTML.write('\n\t </tbody>')
            docHTML.write('\n</table>')
            docHTML.write('\n</div>')  
            docHTML.write('\n</body')
            docHTML.write('\n</html>')
        
            docHTML.close()

            webbrowser.open_new_tab('reporteTokensErrores.html')
        else:
            print('No hay errores por mostrar')
    
    #Funciones para encontrar las celas y agruparlas en arreglos
    def arreglosColores(self):
        
        nombre = ''
        posx = 0
        posy = 0
        booleano = ''
        color = ''
        bolNum = False
        posyB = False
        fin = False
        #Encontrar las posiciones y sus respectivos colores
        for i in self.tokens:
            if i.tipo == tipos.CADENA:
                nombre = i.getLexema()
                
            elif i.tipo == tipos.CORCHETE_I:
                bolNum = True
            elif i.tipo == tipos.NUMERO and bolNum:
                posx = i.getLexema()
                posyB = True
                bolNum = False
                
            
            elif i.tipo == tipos.NUMERO and posyB:
                posy = i.getLexema()
            
                posyB = False
            
            elif i.tipo == tipos.BOOLEANOS:
                booleano = str(i.getLexema())

            elif i.tipo == tipos.COLOR:
                color = str(i.getLexema())

            elif i.tipo == tipos.CORCHETE_D:
                fin = True
            
            elif fin:
                self.celdasPintar.append(Pintar(nombre, posx, posy, booleano, color))
                fin = False
        

    
    def Pintar(self):
        colors = []
        colorActual = ''
        fil1 = False
        fil2 = False
        col1 = False
        col2 = False
        filas = 0
        columnas = 0
        
        #Encontrar las filas y columnas
        for j in self.tokens:
            if j.getLexema().lower() == 'filas':
                fil1 = True
                continue
            elif j.getLexema() == '=' and fil1:
                fil2 = True
                
            elif j.tipo == tipos.NUMERO and fil1 and fil2:
                filas = int(j.getLexema())
                fil1 = False
                fil2 = False
            
            elif j.getLexema().lower() == 'columnas':
                col1 = True
                continue
            elif j.getLexema() == '=' and col1:
                col2 = True
                
            elif j.tipo== tipos.NUMERO and col1 and col2:
                columnas = int(j.getLexema())
                col1 = False
                col2 = False
                
        print('-----------------------Filas y columnas-------------------------')
        print('Filas: ', filas)
        print('columnas: ', columnas)

            

        

        #Encontrar colores para poder pintar
        for y in self.celdasPintar:
            colorActual = y.getColor()
            if colorActual in colors:
                continue
            else:
                colors.append(colorActual)

        


        #Fases de prueba para imprimir
        for i in colors:
            print('Color: ', i)

        for x in self.celdasPintar:
            print('Nombre: ',x.getNombre(),'PosX: ',x.getPosx(),'PosY: ',x.getPosy(), 'Booleano: ',x.getBooleano(),'Color: ', x.getColor())

        
    
    


