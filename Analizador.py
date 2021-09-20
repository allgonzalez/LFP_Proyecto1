from Tokens import Token
from Filas_Columnas import FilasColumnas
from Filtros import Filtros
from Tamaño import Tamaño
from io import open
from os import truncate
import webbrowser
from Pintar import Pintar
import imgkit

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
    
    #Conjunto de nombres que existen en el arreglo
    nombres = []
    
    #Conjunto de filas y columnas va a contener objetos
    filasCol = []

    #Conjunto de filtros
    filtros  = []

    #Conjunto de tamaños
    tamaños = []

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
    def arreglosCeldasPintar(self):
        
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
    
    def arregloColFil(self):
        bolFilas = False
        bolColumnas = False
        nombre = ''
        filas= 0
        columnas = 0
        fin1 = False
        fin2 = False        
        for i in self.tokens:
            if i.tipo == tipos.CADENA:
                nombre = i.getLexema()
                
            elif i.tipo == tipos.PALABRA_RESERVADA and i.getLexema().lower() == 'filas':
                bolFilas = True

            elif i.tipo == tipos.NUMERO and bolFilas:
                filas = i.getLexema()
                bolFilas = False
                fin1 = True
        
            elif i.tipo == tipos.PALABRA_RESERVADA and i.getLexema().lower() == 'columnas':
                bolColumnas = True
                

            elif i.tipo == tipos.NUMERO and bolColumnas:
                columnas = i.getLexema()
                bolColumnas = False
                fin2 = True
            
            elif fin1 and fin2:
                self.filasCol.append(FilasColumnas(nombre, filas, columnas))
                fin1 = False
                fin2 = False


        for x in self.filasCol:
            print('Nombre: ',x.getNombre(), 'Filas: ', x.getFilas(), 'Columnas: ',x.getColumnas())
        
        

    ##LImpiar todos los arreglos recordar

    def arregloNombres(self):
        nombre1 = ''
        for i in self.tokens:
            if i.tipo == tipos.CADENA:
                nombre1 = i.getLexema()
                self.nombres.append(nombre1)

        for x in self.nombres:
            print("nombre: ", x)
    

    def arreglosFiltros(self):
        bolFiltros = False
        mirrorx = 'empty'
        mirrory= 'empty'
        doublemirror = 'empty'
        nombre2 = 'empty'
       
        for i in self.tokens:
            if i.tipo == tipos.CADENA:
                nombre2 = i.getLexema()
                
            elif i.tipo == tipos.PALABRA_RESERVADA and i.getLexema().lower() == 'filtros':
                bolFiltros = True
                
            elif i.tipo == tipos.PALABRA_RESERVADA and i.getLexema().lower()=='mirrorx' and bolFiltros:
                mirrorx = i.getLexema()
        
            elif i.tipo == tipos.PALABRA_RESERVADA and i.getLexema().lower() == 'mirrory' and bolFiltros:
                mirrory = i.getLexema()

            elif i.tipo == tipos.PALABRA_RESERVADA and i.getLexema().lower() == 'doublemirror' and bolFiltros:
                doublemirror = i.getLexema()
            
            elif i.tipo == tipos.PUNTO_COMA and bolFiltros:
                self.filtros.append(Filtros(nombre2, mirrorx, mirrory, doublemirror))
                mirrorx = 'empty'
                mirrory= 'empty'
                doublemirror = 'empty'
                bolFiltros = False

        for j in self.filtros:
            print('Nombre: ',j.getNombre(), 'Mirrorx ', j.getMirrorx(), 'MirrorY: ',j.getMirrory(), 'DoubleMirror: ', j.getDoubleMirror())
    
    def arregloTamaños(self):
        bolAncho = False
        bolAlto = False
        nombre = ''
        ancho= 0
        alto = 0
        fin1 = False
        fin2 = False        
        for i in self.tokens:
            if i.tipo == tipos.CADENA:
                nombre = i.getLexema()

            elif i.tipo == tipos.PALABRA_RESERVADA and i.getLexema().lower() == 'ancho':
                bolAncho = True
                
            elif i.tipo == tipos.NUMERO and bolAncho:
                ancho = i.getLexema()
                bolAncho = False
                fin1 = True
        
            elif i.tipo == tipos.PALABRA_RESERVADA and i.getLexema().lower() == 'alto':
                bolAlto = True
                

            elif i.tipo == tipos.NUMERO and bolAlto:
                alto = i.getLexema()
                bolAlto = False
                fin2 = True
            
            elif fin1 and fin2:
                self.tamaños.append(Tamaño(nombre, ancho, alto))
                fin1 = False
                fin2 = False


        for x in self.tamaños:
                print('Nombre: ',x.getNombre(), 'Ancho: ', x.getAncho(), 'Alto: ',x.getAlto())

    def Pintar(self, nombre):


        colors = []
        colorActual = ''
        filas = 0
        columnas = 0
        contColor = 1
        ancho = 0
        alto = 0


        for j in self.filasCol:
            if j.getNombre() == nombre:
                filas = int(j.getFilas())
                columnas = int(j.getColumnas())
                break
        
        for k in self.tamaños:
            if k.getNombre()== nombre:
                ancho = int(k.getAncho())
                alto = int(k.getAlto())
                break
  
        #HAcer el html con los pixeles
        docHTML1 = open('dibujo.html','w')
        docHTML1.write(
            """
<!DOCTYPE html>
<html lang="es">
<head>
\t<meta charset="UTF-8">
\t<meta http-equiv="X-UA-Compatible" content="IE=edge">
\t<meta name="viewport" content="width=device-width, initial-scale=1.0">
\t<style type="text/css">
\t\ttable, th, td{
\t\t\tborder: 1px solid black;
\t\t\tborder-collapse: collapse;
\t\t}
.box {
    """)
        docHTML1.write('width : '+str(ancho)+'px; height : '+str(alto)+'px;' )
        docHTML1.write('height : '+str(alto)+'px;')
        docHTML1.write('}')
        docHTML1.write(
"""
\t</style>\n
\t<title>Dibujo</title>\n
</head>\n
\t<body>\n

\t\t\t\t<div class="box">\n
\t\t\t\t\t<table style="width: 100%; height: 100%;">\n
            """
        )

        #Variables para ir contando los cuadros
        colActual = 0
        filActual = 0
        seguir = True
        #Pintar los cuadritos
        for x in range(filas):
            docHTML1.write('\t\t\t\t\t\t<tr>\n')
            for y in range(columnas):
                for z in self.celdasPintar:
                    if int(z.getPosx())== filActual and int(z.getPosy())== colActual and z.getBooleano().lower()=='true' and z.getNombre() == nombre:
                        docHTML1.write('\t\t\t\t\t\t\t<td style="background-color: '+z.getColor()+';">\n')
                        docHTML1.write('\t\t\t\t\t\t\t</td>\n')
                        seguir = False
                        break
                if seguir:
                    docHTML1.write('\t\t\t\t\t\t\t<td>\n')
                    docHTML1.write('\t\t\t\t\t\t\t</td>\n')
                
                seguir = True
                colActual += 1
            docHTML1.write('\t\t\t\t\t\t</tr>\n')
                
            filActual +=1
            colActual = 0
            
            
        
        docHTML1.write(
            """
\t\t\t\t\t</table>\n
\t\t\t\t</div>\n
\t</body>\n
</html>
            """
        )

        
        docHTML1.close()
    
        anchoImagen = ancho + 16
        options = {
        'format': 'png',
        'crop-w': str(anchoImagen),
        'encoding': "UTF-8",
    
        'custom-header' : [
        ('Accept-Encoding', 'gzip')
            ]
        }

        path_wkthmltoimage = r'C:\\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe'
        config = imgkit.config(wkhtmltoimage=path_wkthmltoimage)
        imgkit.from_file('dibujo.html', 'dibujo.png', config=config, options=options)


    """
        #Fases de prueba para imprimir
        for i in colors:
            print('Color: ', i)

        for x in self.celdasPintar:
            print('Nombre: ',x.getNombre(),'PosX: ',x.getPosx(),'PosY: ',x.getPosy(), 'Booleano: ',x.getBooleano(),'Color: ', x.getColor())
    """


        
    
    


