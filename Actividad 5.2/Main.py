from tkinter import *  
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Function import *

class main_menu:
    def __init__(self) -> None:
        self.title=Label(root, text="Algoritmos Zero-R y One-R",font=("Arial",25))
        self.file_label=Label(root,text="Archivo seleccionado: ",font=("Arial",14))
        self.load_file_button=Button(root,text="Cargar archivo CSV",command=self.loadFile,bg="sky blue")
        self.load_file_button.config(height=2,width=15)
        self.repeat_label=Label(root,text="Número de iteraciones:",font=("Arial",14))
        self.repeat_times=Spinbox(root,from_=1,to=100000000000000000000000)
        self.start_label=Label(root,text="Iniciar Evaluación de Modelos:",font=("Arial",14))
        self.start_evaluation_button=Button(root,text="Iniciar",command=self.startEvaluation,bg="sky blue",state=DISABLED)
        self.start_evaluation_button.config(height=2,width=15)
        self.functions=Function()


    #Muestra la vista principal
    def show(self):
        self.title.pack()
        self.file_label.pack()
        self.load_file_button.pack()
        self.repeat_label.pack()
        self.repeat_times.pack()
        self.start_label.pack()
        self.start_evaluation_button.pack()
    
    
    def loadFile(self):
        filename = filedialog.askopenfilename(initialdir=".")
        if not filename: return
        if self.functions.loadData(filename)==-1:
            messagebox.showerror("Formato Archivo","El formato del archivo no es CSV")
            self.start_evaluation_button.config(state=DISABLED)
        else:
            self.file_label.config(text="Archivo seleccionado:\n "+filename)
            self.start_evaluation_button.config(state=NORMAL)

    def startEvaluation(self):
        pass
   



root = Tk()
root.title("Algorithms Comparison")
root.geometry("1000x800")
program=main_menu()
program.show()
root.mainloop()
