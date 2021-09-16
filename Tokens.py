class Token():
    lexema_valido = ''
    tipo = 0
    columna = 0

    #Identificar por el número de tipo 
    PALABRA_RESERVADA = 1
    CADENA = 2
    NUMERO = 3
    COLOR = 4
    IGUAL = 5
    LLAVE_I = 6
    LLAVE_D = 7
    CORCHETE_I = 8
    CORCHETE_D = 9
    COMA = 10
    PUNTO_COMA = 11
    BOOLEANOS = 12
    DESCONOCIDO = 13

    #Método constructor

    def __init__(self, lexema, tipo, fila, columna):
        self.lexema_valido = lexema
        self.tipo = tipo
        self.fila = fila
        self.columna = columna

    def getLexema(self):
        return self.lexema_valido

    def getFila(self):
        return self.fila

    def getColumna(self):
        return self.columna
    
    def getTipo(self):
        if self.tipo == self.PALABRA_RESERVADA:
            return 'PALABRA RESERVADA'
        elif self.tipo == self.CADENA:
            return 'CADENA'
        elif self.tipo == self.NUMERO:
            return 'NUMERO'
        elif self.tipo == self.COLOR:
            return 'COLOR'
        elif self.tipo == self.IGUAL:
            return 'IGUAL'
        elif self.tipo == self.LLAVE_I:
            return 'LLAVE IZQUIERDA'
        elif self.tipo == self.LLAVE_D:
            return 'LLAVE DERECHA'
        elif self.tipo == self.CORCHETE_I:
            return 'CORCHETE IZQUIERDO'
        elif self.tipo == self.CORCHETE_D:
            return 'CORCHETE DERECHO'
        elif self.tipo == self.COMA:
            return 'COMA'
        elif self.tipo == self.PUNTO_COMA:
            return 'PUNTO Y COMA'
        elif self.tipo == self.BOOLEANOS:
            return 'BOOLEANOS'
        