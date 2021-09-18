class Pintar:

    def __init__(self, nombre, posx, posy, booleano, color):
        self.nombre = nombre
        self.posx = posx
        self.posy = posy
        self.booleano = booleano
        self.color = color
    
    def getNombre(self):
        return self.nombre
    
    def getPosx(self):
        return self.posx
    
    def getPosy(self):
        return self.posy
    
    def getBooleano(self):
        return self.booleano
    
    def getColor(self):
        return self.color
    