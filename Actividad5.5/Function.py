from numpy.core.numeric import Inf
import pandas as pd
import numpy as np
import math
from pandas.api.types import is_numeric_dtype
from pandas.api.types import is_bool_dtype
from pandas.core.algorithms import mode

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
        self.naive_evaluation=[]
        
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
    


    def getMean(self,array):
        sum=0
        for x in array:
            sum+=x
        return sum/len(array)
    
    def getVar(self, array,mean):
        s2=0
        for x in array:
            s2+=pow((x-mean),2)
        # if len(array)>1:
        #     s2/=(len(array)-1)
        # else:
        #     s2/=(len(array))
        s2/=len(array)-1
        return math.sqrt(s2)

    def fx(self,v,m,x):
        print(v)
        res= pow(math.e,-1*(pow(x-m,2)/(2*pow(v,2))))/(math.sqrt(2*math.pi)*v)
        return res

    #Funcion para utilizar Naïve Bayes en el conjunto de datos
    def naiveB(self, target='Clase'):
        """Ejecutar algoritmo Naïve Bayes
        Parametros:
        target:string
            Indica la columna target en el conjunto de datos, por defecto 'Clase' 
        """
        categorical = []
        numerical = []
        for x in self.data.columns.values.tolist():
            if(is_bool_dtype(self.data[x])):
                categorical.append(x)
            elif is_numeric_dtype(self.data[x]):
                numerical.append(x)
            else:
                categorical.append(x)

        modelCat = {}
        modelNum = {}
        modelClass = {}
        classes = self.data[target].unique()
        #Inicializar modelos
        for x in categorical:
            if x == target:
                continue
            modelCat[x]={}
            for y in self.data[x].unique():
                modelCat[x][y]={}
                for c in classes:
                    modelCat[x][y][c]=0
        
        for x in numerical:
            modelNum[x]={}
            for c in classes:
                modelNum[x][c]=[]
        for x in classes:
            modelClass[x]=0
        
        
        #Tabla de frecuencia clase
        
        for index,row in self.train_data.iterrows():
            modelClass[row[target]]+=1
        for x in modelClass:
            modelClass[x]=modelClass[x]/len(self.train_data)
        
        #print(modelClass)
         
        #Tabla de frecuencia categoricos
        for x in categorical:
            if x == target:
                continue
            temp=dict()
            cont={}
            for y in classes:
                cont[y]=0
            for y in self.data[x].unique():
                temp[y]=dict()
                for c in classes:
                    temp[y][c]=1
                    cont[c]+=1
            for index,row in self.train_data.iterrows():
                temp[row[x]][row[target]]+=1
                cont[row[target]]+=1
            for a in temp:
                for b in temp[a]:
                    modelCat[x][a][b]=temp[a][b]/cont[b]
        
                    
        #Modelo valores numericos
        for x in numerical:
            temp={}
            for y in classes:
                temp[y]=[]
            for index,row in self.train_data.iterrows():
                temp[row[target]].append(row[x])
            for a in temp:
                modelNum[x][a].append(self.getMean(temp[a]))
                modelNum[x][a].append(self.getVar(temp[a],modelNum[x][a][0]))

        # print(modelCat)
        # print(modelNum)
        
        #Evaluacion del modelo

        tot=0
        acc=0
        for index,row in self.test_data.iterrows():
            prediction = ""
            bestacc = 0
            for c in classes:
                currentacc=modelClass[c]
                for x in categorical:
                    if row[x] in modelCat:
                        currentacc*=modelCat[x][row[x]][c]
                for x in numerical:
                    currentacc*=self.fx(modelNum[x][c][1],modelNum[x][c][0],row[x])
                if currentacc>bestacc:
                    bestacc=currentacc
                    prediction=c
            if(prediction==row[target]):
                acc+=1
            tot+=1
        print("acc: ",acc)
        return acc*100/tot

    #Funcion para ejecutar los algoritmos zero-R y one-R
    def evaluation(self,params):
        """Ejecutar evaluacion con el algoritmo naive bayes
        Parametros:
        params:dictionary
            repeatTimes:int
                Indica el numero de interaciones
            testPercent:int
                Indica el porcentaje de datos para pruebas
            Class:string
                Indica el atributo target
        """
        self.naive_evaluation=[]
        naiveA=0
        ok=False
        if params['Class'] in self.data:
            ok=True
            for i in range(0,params["repeatTimes"]):
                self.split_data(params["testPercent"])
                aux = self.naiveB(params['Class'])
                naiveA+=aux
                self.naive_evaluation.append(aux)

        naiveA=naiveA/params["repeatTimes"]
        ans = {"OK":ok,"naive":self.naive_evaluation,"naiveA":naiveA}
        return ans
            