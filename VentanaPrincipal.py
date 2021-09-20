from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from Analizador import Analizador
from PIL import ImageTk,Image
from io import open
from tkinter import messagebox
from tkinter.ttk import *


continuar = False

dibujo = Analizador()

nombres = []

#Creo mis ventanas
ventana = Tk()
notebook = ttk.Notebook(ventana)
notebook.pack(fill='both', expand = 'yes')

#Creacion de pestañas
pesAnalizar = ttk.Frame(notebook)
pesImagen = ttk.Frame(notebook)
pesTokens = ttk.Frame(notebook)

#Pestañas
notebook.add(pesAnalizar, text='Analizar')
notebook.add(pesImagen, text='Imagen')
notebook.add(pesTokens, text= 'Tokens')

#Estilos
style = Style()
 
style.configure('TButton', font =
               ('calibri', 12, 'bold'),
                    borderwidth = '4')
style = ttk.Style()
style.configure("TLabel", foreground="black", background="white")

#Funciones
def arbirArchivo():
    global continuar, comboNombres
    archivo = filedialog.askopenfilename(title="Abrir", filetypes=[("pixeles", "*.pxla")])
    archivos_texto = open(archivo, 'r')
    texto = archivos_texto.read()
    dibujo.scanner(texto)
    dibujo.arreglosCeldasPintar()
    dibujo.arregloColFil()
    dibujo.arregloNombres()
    dibujo.arreglosFiltros()
    dibujo.arregloTamaños()
    #dibujo.Pintar('"Hongo"')
    comboNombres = ttk.Combobox(pesImagen)
    comboNombres.place(x=25,y=50)
    comboNombres['values'] = dibujo.nombres

    if dibujo.generarErrores:
        dibujo.imprimirErrores()
    else:
        continuar = True

def generarImagen():
    global comboNombres
    if continuar:
        global imagenA1, imagenA, botonMirrorX
        var = comboNombres.get()
        dibujo.Pintar(var)
        imagenA = ImageTk.PhotoImage(Image.open('dibujo.png').resize((500,500)))
        imagenA1 = Label(pesImagen,image = imagenA).place(x=150,y=250)
        botonOriginal.place(x=300, y=50)
        for i in dibujo.filtros:
            if var == i.getNombre():
                if i.getMirrorx().lower() == 'mirrorx':
                    botonMirrorX.place(x=400, y=50)
                if i.getMirrory().lower()=='mirrory':
                    botonMirrorY.place(x=500, y=50)
                if i.getDoubleMirror().lower()=='doublemirror':
                    botonDoubleMirror.place(x=600, y=50)
            
            """
            #IGNORAR ESTE CODIGOOOOOOOOOOO!!!!!!!!!! PERO SE QUEDA AQUI POR SI ACASO XD
            if i.getMirrorx() != 'empty' and i.getMirrory()!='empty' and i.getDoubleMirror()!='empty':
                botonMirrorX.winfo_ismapped()
                botonMirrorY.winfo_ismapped()
                botonDoubleMirror.winfo_ismapped()
                break
            elif i.getMirrorx()!= 'empty' and i.getMirrory()!='empty':
                botonMirrorX.winfo_ismapped()
                botonMirrorY.winfo_ismapped()
                break
            elif i.getMirrorx()!='empty' and i.getDoubleMirror()!='empty':
                botonMirrorX.winfo_ismapped()
                botonDoubleMirror.winfo_ismapped()
                break
            elif i.getMirrorx()!='empty' and i.getDoubleMirror()!='empty':
                botonMirrorY.winfo_ismapped()
                botonDoubleMirror.winfo_ismapped()
                break
            elif i.getMirrorx()!='empty':
                botonMirrorX.winfo_ismapped()
                break
            elif i.getMirrory()!='empty':
                botonMirrorY.winfo_ismapped()
                break
            elif i.getDoubleMirror()!='empty':
                botonDoubleMirror.winfo_ismapped()
                break
            """
    else:
        mensajeError()
        print('hubo un error por favor corriga el documento')

def mensajeError():
    messagebox.showinfo("ERROR","Tiene un error en su documento o no ha cargado ningún archivo y no se puede ejecutar las demás instrucciones, por favor ¡corrígalo!")

def mensajeErrorNoHay():
    if dibujo.generarErrores:
        dibujo.imprimirErrores()
    else:
        messagebox.showinfo("NO HAY ERRORES","El archivo no contiene errores")

    

def mirrorX():
    global original_img, horz_img, imagenA, imagenA1
    original_img = Image.open("dibujo.png") 
  
    
    horz_img = original_img.transpose(method=Image.FLIP_LEFT_RIGHT) 
    horz_img.save("dibujoMIRRORX.png") 
  
    original_img.close() 
    horz_img.close() 

    imagenA = ImageTk.PhotoImage(Image.open('dibujoMIRRORX.png').resize((500,500)))
    imagenA1 = Label(pesImagen,image = imagenA).place(x=150,y=250)

def mirrorY():
    global original_img, vertical_img, imagenA, imagenA1
    original_img = Image.open("dibujo.png") 
  
    vertical_img = original_img.transpose(method=Image.FLIP_TOP_BOTTOM) 
    vertical_img.save("dibujoMIRRORY.png") 
  
    original_img.close() 
    vertical_img.close()
    imagenA = ImageTk.PhotoImage(Image.open('dibujoMIRRORY.png').resize((500,500)))
    imagenA1 = Label(pesImagen,image = imagenA).place(x=150,y=250)


def doubleMirror():
    global original_img, vertical_img, horz_img, imagenA, imagenA1

    original_img = Image.open("dibujo.png") 
  
    vertical_img = original_img.transpose(method=Image.FLIP_TOP_BOTTOM)  
    horz_img = vertical_img.transpose(method=Image.FLIP_LEFT_RIGHT) 
    horz_img.save("dibujoDOUBLEMIRROR.png") 
  
    original_img.close() 
    horz_img.close() 
    vertical_img.close()
    
    imagenA = ImageTk.PhotoImage(Image.open('dibujoDOUBLEMIRROR.png').resize((500,500)))
    imagenA1 = Label(pesImagen,image = imagenA).place(x=150,y=250)

def original():
    global imagenA, imagenA1
    imagenA = ImageTk.PhotoImage(Image.open('dibujo.png').resize((500,500)))
    imagenA1 = Label(pesImagen,image = imagenA).place(x=150,y=250)

def limpiarFiltros():
     botonMirrorX.place_forget()
     botonMirrorY.place_forget()
     botonDoubleMirror.place_forget()
     botonOriginal.place_forget()

#Imagenes
imagenA = ImageTk.PhotoImage(Image.open('vacio.png').resize((500,500)))
imagenA1 = Label(pesImagen,image = imagenA).place(x=150,y=250)

#Botones
s = ttk.Style()
s.configure(
    "MyButton.TButton",
    background = '#076858',
    width = 25,
    foreground="#119B58",
)
s.configure(
    "MyButton1.TButton",
    background = 'red',
    width = 25,
    foreground="red",
)
s.configure(
    "MyButton2.TButton",
    background = 'blue',
    width = 45,
    foreground="green",
)
s.configure(
    "MyButton3.TButton",
    background = 'red',
    width = 45,
    foreground="red",
)
botonAnalizar = Button(pesAnalizar, text='Cargar Archivo', command=arbirArchivo, style="MyButton.TButton")
botonAnalizar.place(x=260, y=250)

#botonAnalizar.config(fg='red')

botonImagen = Button(pesImagen, text = 'Renderizar imagen', command =generarImagen ).place(x=35, y=110)
botonLimpiarFiltros = Button(pesImagen, text='Limpiar Filtros', command=limpiarFiltros).place(x=450, y=110)


botonOriginal = Button(pesImagen, text='ORIGINAL', command=original)
botonOriginal.place(x=300, y=50)
botonOriginal.place_forget()

botonMirrorX = Button(pesImagen, text='MIRRORX', command=mirrorX)
botonMirrorX.place(x=400, y=50)
botonMirrorX.place_forget()
     

botonMirrorY = Button(pesImagen, text='MIRRORY', command=mirrorY)
botonMirrorY.place(x=500, y=50)
botonMirrorY.place_forget()
     



botonDoubleMirror = Button(pesImagen, text='DOUBLEMIRROR', command=doubleMirror)
botonDoubleMirror.place(x=600, y=50)
botonDoubleMirror.place_forget()

botonGenerarReportes = Button(pesTokens, text='GENERAR REPORTE DE TOKENS VÁLIDOS', command= dibujo.imprimirTokens, style="MyButton2.TButton")
botonGenerarReportes.place(x=200, y=300)

botonGenerarReportesErrores = Button(pesTokens, text='GENERAR REPORTE DE TOKENS CON ERRORES', command= mensajeErrorNoHay, style="MyButton3.TButton")
botonGenerarReportesErrores.place(x=200, y=400)

botonSalir = Button(pesAnalizar, text='SALIR', command=ventana.destroy, style="MyButton1.TButton")

botonSalir.place(x=260, y=300)




#Labels
labelNombres = Label(pesImagen, text="Lista de Nombres")
labelNombres.place(x= 25, y=15)

labelNombres = Label(pesImagen, text="Filtros para la imagen").place(x= 450, y=15)

#Extras
logo = ImageTk.PhotoImage(Image.open('Pixelart.png'))
logo1 = Label(pesAnalizar,image = logo).place(x=80,y=10)

reportesLogo = ImageTk.PhotoImage(Image.open('reportes.png'))
reportesLogo1 = Label(pesTokens,image = reportesLogo).place(x=50,y=10)

bienvenido = ImageTk.PhotoImage(Image.open('bienvenido.png'))
bienvenido1 = Label(pesAnalizar,image = bienvenido).place(x=170,y=450)






#Cerrar ventanas y tamaño
ventana.geometry('800x800')
ventana.mainloop()


