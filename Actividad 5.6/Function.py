from tkinter.constants import NUMERIC
from numpy.core.numeric import Inf
import pandas as pd
import numpy as np
import math
from pandas.api.types import is_numeric_dtype
from pandas.api.types import is_bool_dtype
from pandas.core.algorithms import mode

#Clase que contiene las funciones para ejecutar la evaluacion con el algoritmo  KNN
class Function:
    #Constructor de la clase
    def __init__(self) -> None:
        """Constructor de la clase Function
        Parametros:Ninguno
        """
        self.data=[]
        self.train_data=[]
        self.test_data=[]
        self.knn_evaluation=[]
        self.categorical=[]
        self.numerical=[]
        self.targetType=""
        
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
    
    def preprocessing(self,target):
        self.categorical=[]
        self.numerical=[]
        for x in self.data.columns.tolist():
            if(x!=target):
                if(self.data.at[0,x].lower()=="numérico" or self.data.at[0,x].lower()=="numerico"):
                    self.numerical.append(x)
                else:
                    self.categorical.append(x)
            else:
                if(self.data.at[0,x].lower()=="numérico" or self.data.at[0,x].lower()=="numerico"):
                    self.targetType="numerical"
                else:
                    self.targetType="categorical"
        self.data=self.data.drop(self.data.index[[0]])
        if(self.targetType=="numerical"):
            self.data[target]=self.data[target].astype(float)

        
        for x in self.categorical:
            self.data[x]=self.data[x].astype(object)
        for x in self.numerical:
            self.data[x]=self.data[x].astype(float)

        #Normalizar
        for x in self.numerical:
            maximo=self.data[x].loc[self.data[x].idxmax()]
            minimo=self.data[x].loc[self.data[x].idxmin()]
            
            for index,row in self.data.iterrows():
                self.data.at[index,x]=(row[x]-minimo)/(maximo-minimo)
       
        


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
    


    #Funcion para utilizar KNN en el conjunto de datos
    def knn(self, target='Clase',k=1):
        """Ejecutar algoritmo KNN
        Parametros:
        target:string
            Indica la columna target en el conjunto de datos, por defecto 'Clase' 
        """
        
        acc=0
        for ind,row in self.test_data.iterrows():
            results=dict()
            for index,x in self.train_data.iterrows():
                disimilitud=0
                for c in self.categorical:
                    if(x[c]!=row[c]):
                        disimilitud+=1
                for n in self.numerical:
                    disimilitud+=(abs(x[n]-row[n]))
                results[index]=disimilitud
            if self.targetType=="numerical":
                ans=0.0
                aux=dict(sorted(results.items(),key=lambda z:z[1]))
                i=1
                for y in aux:
                    ans+=self.train_data.at[y,target]
                    if(i==k):
                        break
                    i+=1
                ans/=k
                acc+=(row[target]-ans)**2
            else:
                aux=dict(sorted(results.items(),key=lambda z:z[1]))
                res=dict()
                i=1
                for y in aux:
                    if(self.train_data.at[y,target] in res):
                        res[self.train_data.at[y,target]]+=1
                    else:
                        res[self.train_data.at[y,target]]=1
                    if(i==k):
                        break
                    i+=1
                restwo=dict(sorted(res.items(),key=lambda z:z[1],reverse=True))
                for y in restwo:
                    if(y==row[target]):
                        acc+=1
                    break
        if(self.targetType=="numerical"):
            return acc/len(self.test_data)
        else:
            return acc*100/len(self.test_data)
                        

    #Funcion para ejecutar el algoritmo KNN
    def evaluation(self,params):
        """Ejecutar evaluacion con el algoritmo KNN
        Parametros:
        params:dictionary
            repeatTimes:int
                Indica el numero de interaciones
            testPercent:int
                Indica el porcentaje de datos para pruebas
            Class:string
                Indica el atributo target
        """
        self.loadData(params['file'])
        self.preprocessing(params['Class'])
        self.knn_evaluation=[]
        
        ok=False
        bestK=1
        bestMSE=math.inf
        bestAcc=0
        if params['Class'] in self.data:
            ok=True
            self.split_data(params["testPercent"])
            for i in range(1,params["repeatTimes"]+1):
                aux = self.knn(params['Class'],i)
                self.knn_evaluation.append(aux)
                if(self.targetType=="numerical"):
                    if(aux<bestMSE):
                        bestMSE=aux
                        bestK=i
                else:
                    if(aux>bestAcc):
                        bestAcc=aux
                        bestK=i
        
        ans = {"OK":ok,"knn":self.knn_evaluation,"bestK":bestK,"bestMSE":bestMSE,"bestAcc":bestAcc,"type":self.targetType}
        return ans
            