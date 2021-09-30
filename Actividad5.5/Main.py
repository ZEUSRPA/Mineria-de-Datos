from tkinter import *  
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Function import *


#Frame utilizado para mostrar los graficos
class graph_frame(Frame):
    def __init__(self):
        """Constructor de la clase graph_frame
        """
        Frame.__init__(self,root)
       
    
    def add_graph(self,fig):
        """Funcion para agregar una figura en el frame
        Parametros:
        fig:plt.figure
            Indica la figura que se va a insertar en el frame
        """
        self.mpl_canvas=FigureCanvasTkAgg(fig,self)
        
        self.mpl_canvas.get_tk_widget().pack(fill=BOTH,expand=True)
        self.mpl_canvas._tkcanvas.pack( fill=BOTH, expand=True)
    def remove_graph(self):
        """Elimina la figura del frame"""
        self.mpl_canvas.get_tk_widget().pack_forget()
        self.mpl_canvas._tkcanvas.pack_forget()
        del self.mpl_canvas

class main_menu:
    def __init__(self) -> None:
        """Constructor de la clase main_menu
        """
        self.title=Label(root, text="Algoritmo Naïve Bayes",font=("Arial",25))
        self.file_label=Label(root,text="Archivo seleccionado: ",font=("Arial",14))
        self.load_file_button=Button(root,text="Cargar archivo CSV",command=self.loadFile,bg="sky blue")
        self.load_file_button.config(height=2,width=15)
        self.target_label=Label(root,text="Nombre del atributo clase:",font=("Arial",14))
        self.target_entry=Entry(root)
        self.repeat_label=Label(root,text="Número de iteraciones:",font=("Arial",14))
        self.repeat_times=Spinbox(root,from_=1,to=100000000000000000000000)
        self.test_label=Label(root,text="Porcentaje de datos para prueba:",font=("Arial",14))
        self.test_percent=Spinbox(root,from_=0,to=100)
        self.start_label=Label(root,text="Iniciar Evaluación de Modelo:",font=("Arial",14))
        self.start_evaluation_button=Button(root,text="Iniciar",command=self.startEvaluation,bg="sky blue",state=DISABLED)
        self.start_evaluation_button.config(height=2,width=15)
        self.naive_label=Label(root,text="Resultados Naïve Bayes",font=("Arial",14))
        self.naive_results=Label(root,font=("Arial",12))
        self.functions=Function()
        self.naive_evaluation=[]
        self.load_charts()


    def load_charts(self):
        """Funcion para cargar los graficos en la interfaz"""
        self.graph_frame=graph_frame()
        self.figure=plt.Figure(figsize=(12,10))
        self.graph_frame.add_graph(self.figure)

        self.naiveGraph=self.figure.add_subplot(111)
        self.naiveGraph.set_title("Naïve Bayes")
        self.naiveGraph.plot(self.naive_evaluation)




    #Muestra la vista principal
    def show(self):
        """Funcion para mostrar la vista principal"""
        self.title.pack()
        self.file_label.pack()
        self.load_file_button.pack()
        self.target_label.pack()
        self.target_entry.pack()
        self.repeat_label.pack()
        self.repeat_times.pack()
        self.test_label.pack()
        self.test_percent.pack()
        self.start_label.pack()
        self.start_evaluation_button.pack()
        self.naive_label.pack()
        self.naive_results.pack()
        self.graph_frame.pack()
    
    def showResults(self,results):
        """Funcion para mostrar en pantalla los resultados de la evaluacion de los algoritmos
        Parametros:
        results:dictionary
            OK:bool
                Se utiliza para verificar que no existan errores en la ejecucion
            naive:list
                Lista de los resultados obtenidos para el algoritmo zero-R
            naiveA:float
                Indica el promedio de aciertos de Naïve Bayes
        """
        if results['OK'] == False:
            messagebox.showerror("Nombre Clase","El nombre de la clase no se encuentra en el archivo")
            return
        self.naive_evaluation=results['naive']
        showing=""
        # for x in results['zeroR']:
        #     showing=showing+x+'\n'
        showing=showing + "Promedio de aciertos: "+str(results['naiveA'])+'\n'
        showing=showing + "Promedio de errores: "+str(100-results['naiveA'])+'\n'

        self.naive_results.config(text=showing)
        showing=""
        # for x in results['oneR']:
        #     showing=showing+x+'\n'
        del self.naiveGraph.lines[0]
        self.naiveGraph.plot(self.naive_evaluation)
        self.figure.canvas.draw()

    
    def loadFile(self):
        filename = filedialog.askopenfilename(initialdir=".")
        aux=filename.split('/')
        if not filename: return
        if self.functions.loadData(filename)==-1:
            messagebox.showerror("Formato Archivo","El formato del archivo no es CSV")
            self.start_evaluation_button.config(state=DISABLED)
        else:
            self.file_label.config(text="Archivo seleccionado:\n "+aux[-1])
            self.start_evaluation_button.config(state=NORMAL)

    def startEvaluation(self):
        params = {"testPercent":int(self.test_percent.get()),"repeatTimes":int(self.repeat_times.get()),"Class":self.target_entry.get()}
        self.showResults(self.functions.evaluation(params))
   



root = Tk()
root.title("Naïve Bayes")
root.geometry("1000x800")
program=main_menu()
program.show()
root.mainloop()
