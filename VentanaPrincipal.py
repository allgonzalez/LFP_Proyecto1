from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from Analizador import Analizador
from PIL import ImageTk,Image
from io import open
from tkinter import messagebox


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
                    print('encontrado mirrorx')
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
    messagebox.showinfo("ERROR","Tiene un error en su documento y no se puede ejecutar las demás instrucciones, por favor corrígalo")


    

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
imagenA = ImageTk.PhotoImage(Image.open('vacio.png').resize((200,200)))
imagenA1 = Label(pesImagen,image = imagenA).place(x=150,y=250)

#Botones
botonAnalizar = Button(pesAnalizar, text='Cargar Archivo', command=arbirArchivo).place(x=80, y=50)
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

botonGenerarReportes = Button(pesTokens, text='GENERAR REPORTE DE TOKENS VÁLIDOS', command= dibujo.imprimirTokens)
botonGenerarReportes.place(x=400, y=400)

botonSalir = Button(pesAnalizar, text='SALIR', command=ventana.destroy)

botonSalir.place(x=300, y=300)



#Labels
labelNombres = Label(pesImagen, text="Lista de Nombres").place(x= 25, y=15)
labelNombres = Label(pesImagen, text="Filtros para la imagen").place(x= 450, y=15)





#Cerrar ventanas y tamaño
ventana.geometry('800x800')
ventana.mainloop()


