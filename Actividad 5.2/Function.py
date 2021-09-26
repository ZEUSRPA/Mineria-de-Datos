from numpy.core.numeric import Inf
import pandas as pd
import numpy as np

#Clase que contiene las funciones para ejecutar la evaluacion con los algoritmos zero-R y one-R
class Function:
    #Constructor de la clase
    def __init__(self) -> None:
        """Constructor de la clase Function
        Parametros:Ninguno
        """
        self.data=[]
        self.train_data=[]
        self.test_data=[]
        self.one_evaluation=[]
        self.zero_evaluation=[]
        
    #Funcion para cargar los datos desde un archivo csv
    def loadData(self,file):
        """Cargar archivo csv
        Parametros:
        file:string
            ruta del archivo a cargar
        """
        try:
            self.data=pd.read_csv(file)
            return 1
        except:
            return -1

    #Funcion para Dividir el conjunto de datos en prueba y entrenamiento
    def split_data(self,testPercent):
        """Dividir conjunto de datos en prueba y entrenamiento
        Parametros:
        testPercent:int
            indica el porcentaje de datos a usar para pruebas, utilizar 0 para indicar que se usara todo el conjunto tanto para pruebas como para entrenamiento
        """
        if(testPercent==0 or testPercent==100):
            self.test_data=self.data
            self.train_data=self.data
        else:
            testAmount = len(self.data)*testPercent//100
            self.data=self.data.sample(frac=1)
            self.test_data = self.data[:testAmount]
            self.train_data = self.data[testAmount:]
    
    #Funcion para utilizar zero-R en el conjunto de datos
    def zeroR(self,clase = 'Clase'):
        """Ejecutar algoritmo Zero-R
        Parametros:
        clase:string
            Indica la columna target en el conjunto de datos, por defecto 'Clase'
        """
        #Encontramos el valor mas repetido
        valor = self.train_data[clase].mode().iloc[0]
        #Cuenta las veces que el nombre se repite
        radio = self.test_data[self.test_data.eq(valor).any(1)].count().max()
        #Numero de veces que aparece
        clases = self.test_data.groupby([clase]).size().max()
         #Numero total de registros
        total_registros = self.test_data.count().max()
        #Porcentaje aciertos a partir del promedio
        aciertos = (clases/total_registros)*100 
        #Porcentaje de erroes 
        errores = 100 - aciertos

        return aciertos
        #pass
        

    #Funcion para utilizar one-R en el conjunto de datos
    def oneR(self, target='Clase'):
        """Ejecutar algoritmo One-R
        Parametros:
        target:string
            Indica la columna target en el conjunto de datos, por defecto 'Clase' 
        """
        model=""
        min_error = Inf
        res = dict()
        
        #Tablas de frecuencias: obtener de cada atributo la cantidad de veces que aparece en determinada clase objetivo
        classes = self.data[target].unique()

        for i in self.train_data:

            if i == target:
                continue
            freq_tab = pd.crosstab(self.train_data[i], self.data[target])
            
            # idxmax(axis=1) : column per row w highest value
            #Reglas: determinar error total de cada atributo
            res[str(i)] = dict(freq_tab.idxmax(axis=1))
            #Descripcion del modelo: Seleccionar el mejor atributo, es decir el que tiene un menor error total
            count = len(self.train_data)
            
            for index, row in freq_tab.iterrows():
                for column in classes:
                    if(res[str(i)][index]==column):
                        if column in row:
                            count-=row[column]
            if count<min_error:
                min_error=count
                model=str(i)
        
      

        #Evaluacion: evaluar el modelo
        total=0
        acc=0 
        for index,row in self.test_data.iterrows():
            if row[model]in res[model] and res[model][row[model]]== row[target]:
                acc+=1
            total+=1
        acc=acc*100/total
        return acc

    #Funcion para ejecutar los algoritmos zero-R y one-R
    def evaluation(self,params):
        """Ejecutar evaluacion con los algoritmos Zero-R y One-R
        Parametros:
        params:dictionary
            repeatTimes:int
                Indica el numero de interaciones
            testPercent:int
                Indica el porcentaje de datos para pruebas
            Class:string
                Indica el atributo target
        """
        self.one_evaluation=[]
        self.zero_evaluation=[]
        zeroA=0
        oneA=0
        ok=False
        if params['Class'] in self.data:
            ok=True
            for i in range(0,params["repeatTimes"]):
                self.split_data(params["testPercent"])
                aux = self.zeroR(params['Class'])
                zeroA+=aux
                self.zero_evaluation.append(aux)
                aux=self.oneR(params['Class'])
                oneA+=aux
                self.one_evaluation.append(aux)

        zeroA=zeroA/params["repeatTimes"]
        oneA=oneA/params["repeatTimes"]
        ans = {"OK":ok,"zeroR":self.zero_evaluation,"oneR":self.one_evaluation,"zeroA":zeroA,"oneA":oneA}
        return ans
            