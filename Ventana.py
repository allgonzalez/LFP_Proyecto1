from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from Analizador import Analizador
from PIL import ImageTk,Image
from io import open



dibujo = Analizador()


ventana = Tk()
notebook = ttk.Notebook(ventana)
notebook.pack(fill='both', expand = 'yes')
pesAnalizar = ttk.Frame(notebook)
pesImagen = ttk.Frame(notebook)
pesTokens = ttk.Frame(notebook)

#Pestañas
notebook.add(pesAnalizar, text='Analizar')
notebook.add(pesImagen, text='Imagen')
notebook.add(pesTokens, text= 'Tokens')
    

#Funciones
def arbirArchivo():
    archivo = filedialog.askopenfilename(title="Abrir", filetypes=[("pixeles", "*.pxla")])
    archivos_texto = open(archivo, 'r')
    texto = archivos_texto.read()
    dibujo.scanner(texto)
    dibujo.arreglosCeldasPintar()
    dibujo.arregloColFil()
    dibujo.arregloNombres()
    dibujo.arreglosFiltros()
    dibujo.arregloTamaños()
    dibujo.Pintar('"Creeper"')

def generarImagen():
    global imagenA1, imagenA

    imagenA = ImageTk.PhotoImage(Image.open('dibujo.png').resize((500,500)))
    imagenA1 = Label(pesImagen,image = imagenA).place(x=150,y=250)
    

#Imagenes
imagenA = ImageTk.PhotoImage(Image.open('vacio.png').resize((200,200)))
imagenA1 = Label(pesImagen,image = imagenA).place(x=150,y=250)



#Botones
botonAnalizar = Button(pesAnalizar, text='Cargar Archivo', command=arbirArchivo).place(x=80, y=50)
botonImagen = Button(pesImagen, text = 'Celdas pintar', command =generarImagen ).place(x=20, y=110)


#Cerrar ventanas
ventana.geometry('800x800')
ventana.mainloop()


