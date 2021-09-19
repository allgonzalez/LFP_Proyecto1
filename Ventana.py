from tkinter import *
from tkinter import ttk

ventana = Tk()
notebook = ttk.Notebook(ventana)
notebook.pack(fill='both', expand = 'yes')
pes = ttk.Frame(notebook)
pes1 = ttk.Frame(notebook)

notebook.add(pes, text='Analizar')
notebook.add(pes1, text='Imagen')
boton = Button(pes, text='Holaaa').place(x=20, y=50)
ventana.geometry('300x300')
ventana.mainloop()