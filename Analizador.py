from Tokens import Token

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
                    elif self.booleanos(self.lexema):
                        self.agregarToken(tipos.BOOLEANOS)
                        self.lexema = actual
                        self.columna += 1
                        self.agregarToken(tipos.COMA)
                    else:
                        self.agregarToken(tipos.DESCONOCIDO)
                        self.generarErrores = True
            
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
            
            elif self.estado == 4:
                if actual.isdigit():
                    self.estado = 4
                    self.columna +=1
                    self.lexema += actual
                else:
                    if actual == ',':
                        self.agregarToken(tipos.NUMERO)
                        self.lexema = actual
                        self.columna += 1
                        self.agregarToken(tipos.COMA)
                        
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
                if actual != '#' and actual!= ']':
                    self.estado = 6
                    self.columna += 1
                    self.lexema += actual
                elif actual == ']':
                    self.agregarToken(tipos.COLOR)
                    self.lexema = actual
                    self.columna += 1
                    self.agregarToken(tipos.CORCHETE_D)
            
            

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
    
    def imprimirErrores(self):
        if self.generarErrores:
            print('------------------------Errores----------------------')
            for i in self.tokens :
                if i.tipo == tipos.DESCONOCIDO:
                    print('Lexema : ', i.getLexema(), ' Fila : ', i.getFila(), ' Columna : ', i.getColumna())
        else:
            print('No hay errores por mostrar')
    

