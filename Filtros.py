class Filtros:

    def __init__(self, nombre, mirrorx, mirrory, doublemirror):
        self.nombre = nombre
        self.mirrorx = mirrorx
        self.mirrory = mirrory
        self.doublemirror = doublemirror
    
    def getNombre(self):
        return self.nombre

    def getMirrorx(self):
        return self.mirrorx
    
    def getMirrory(self):
        return self.mirrory
    
    def getDoubleMirror(self):
        return self.doublemirror