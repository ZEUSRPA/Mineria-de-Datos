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
        self.title=Label(root, text="Análisis bivariable",font=("Arial",25))
        self.file_label=Label(root,text="Archivo seleccionado: ",font=("Arial",14))
        self.load_file_button=Button(root,text="Cargar archivo CSV",command=self.loadFile,bg="sky blue")
        self.load_file_button.config(height=2,width=15)
        self.start_label=Label(root,text="Iniciar Análisis",font=("Arial",14))
        self.start_evaluation_button=Button(root,text="Iniciar",command=self.startEvaluation,bg="sky blue",state=DISABLED)
        self.start_evaluation_button.config(height=2,width=15)
        self.analisis_label=Label(root,text="Resultados del Análisis",font=("Arial",14))
        self.analisis_results=Canvas(root, width=1000, height=500)
        self.functions=Function()
        self.analisis_evaluation=[]
        #self.load_charts()


    def load_charts(self):
        """Funcion para cargar los graficos en la interfaz"""
        self.graph_frame=graph_frame()
        self.figure=plt.Figure(figsize=(12,10))
        self.graph_frame.add_graph(self.figure)

        self.analisisGraph=self.figure.add_subplot(111)
        self.analisisGraph.set_title("analisis")
        self.analisisGraph.plot(self.knn_evaluation)




    #Muestra la vista principal
    def show(self):
        """Funcion para mostrar la vista principal"""
        self.title.pack()
        self.file_label.pack()
        self.load_file_button.pack()
        self.start_label.pack()
        self.start_evaluation_button.pack()
        self.analisis_label.pack()
        self.analisis_results.pack()
        #self.graph_frame.pack()
    
    def showResults(self,results):
        """Funcion para mostrar en pantalla los resultados de la evaluacion de los algoritmos
        Parametros:
        results:dictionary
            OK:bool
                Se utiliza para verificar que no existan errores en la ejecucion
            knn:list
                Lista de los resultados obtenidos para el algoritmo
            knnA:float
                Indica el promedio de aciertos de KNN
        """
        # for x in results['NaiveBayes']:
        #     showing=showing+x+'\n'
        y=0
        self.analisis_results.delete('all')
        for x in results['answers']:
            print (x)
            label = Label(self.analisis_results,text=x, font=("Courier", 14), compound=RIGHT)
            self.analisis_results.create_window(0, y, window=label, anchor=NW)
            y += 80

        scrollbar = Scrollbar(self.analisis_results, orient=VERTICAL, command=self.analisis_results.yview)
        scrollbar.place(relx=1, rely=0, relheight=1, anchor=NE)
        self.analisis_results.config(yscrollcommand=scrollbar.set, scrollregion=(0, 0, 0, y))
        # for x in results['NaivBayes']:
        #     showing=showing+x+'\n'
        # del self.knnGraph.lines[0]
        # self.knnGraph.plot(self.knn_evaluation)
        # self.figure.canvas.draw()

    
    def loadFile(self):
        self.filename = filedialog.askopenfilename(initialdir=".")
        aux=self.filename.split('/')
        if not self.filename: return
        if self.functions.loadData(self.filename)==-1:
            messagebox.showerror("Formato Archivo","El formato del archivo no es CSV")
            self.start_evaluation_button.config(state=DISABLED)
        else:
            self.file_label.config(text="Archivo seleccionado:\n "+aux[-1])
            self.start_evaluation_button.config(state=NORMAL)

    def startEvaluation(self):
        params = {"file":self.filename}
        self.showResults(self.functions.evaluation(params))
   



root = Tk()
root.title("Análisis bivariable")
root.geometry("1000x800")
program=main_menu()
program.show()
root.mainloop()
