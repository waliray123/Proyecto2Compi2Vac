
import pandas as pd
from matplotlib import pyplot as plt
from sklearn import preprocessing
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score
import io, base64



class Analisis1():
    nombrePais = ''
    campoPaises = ''
    campodia = ''
    camponum = ''
    archivoEn = any
    diasPrediccion = 0


    def __init__(self,nombrePais,campoPaises,campodia,camponum,archivoEn):
        self.nombrePais = nombrePais
        self.campoPaises = campoPaises
        self.campodia = campodia
        self.camponum = camponum
        self.archivoEn = archivoEn

    def analizar(self):
        nombreArchivo = self.archivoEn.name
        df = any

        #Revisar el tipo de archivo para crear el dataframe
        if nombreArchivo.endswith('.csv'):
            df = pd.read_csv(self.archivoEn)            
        elif nombreArchivo.endswith('.xls') or nombreArchivo.endswith('.xlsx'):
            df = pd.read_excel(self.archivoEn)            
        elif nombreArchivo.endswith('.json'):
            df = pd.read_json(self.archivoEn)
        
        #Diferenciar los datos del pais
        pais = np.asarray(df[self.campoPaises].str.contains(self.nombrePais))             

        #Obtener todos los datos que son del pais
        dfPais = df[pais]

        
        #Crear un array del largo de los dias y que represente las fechas en su valor

        lbl_enc = preprocessing.LabelEncoder()
        diasLimpios = lbl_enc.fit_transform(dfPais[self.campodia])


        X = np.array(diasLimpios).reshape(-1,1)
        Y = dfPais[self.camponum]

        #Obtener el mayor dia y el menor
        menorDia = np.amin(X)
        mayorDia = np.amax(X)
        #Obtener el mayor numero de infectados y el menor
        menorInf = np.amin(Y) 
        mayorInf = np.amax(Y) 

        #Ploteamos los datos que nos dieron

        plt.scatter(X,Y) 

        #Definimos el modelo

        nb_degree = 3
        polynomial_features = PolynomialFeatures(degree = nb_degree) 

        X_TRANSF = polynomial_features.fit_transform(X)

        # Entrenamos el modelo

        model = LinearRegression() 
        model.fit(X_TRANSF, Y)  
        Y_NEW = model.predict(X_TRANSF)  

        #Obtenemos el error y el r cuadrado

        rmse = np.sqrt(mean_squared_error(Y,Y_NEW)) 
        r2 = r2_score(Y,Y_NEW) 

        print('RMSE: ', rmse) 
        print('R2: ', r2)


        # PREDICCION FINAL

        x_new_min = menorDia
        x_new_max = mayorDia + self.diasPrediccion

        X_NEW = np.arange(x_new_max).reshape(-1,1)  

        X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)  
        Y_NEW = model.predict(X_NEW_TRANSF)  

        #Prediccion de ultimo dia
        prediccionUltDia = Y_NEW[-1]
        print(prediccionUltDia)

        plt.plot(X_NEW, Y_NEW, color='coral', linewidth=3)  

        plt.grid()  
        plt.xlim(x_new_min,x_new_max)  
        plt.ylim(menorInf,mayorInf)  

        title = 'Grado = {}; RMSE = {}; R2 = {}'.format(nb_degree,rmse, r2)
        plt.title('Tendencia de infeccion\n ' + title, fontsize=10)
        plt.xlabel('Dia')
        plt.ylabel('Infectados ')         

        #Generar imagen y retornarla                                             
        flike = io.BytesIO()
        plt.savefig(flike)
        b64 = base64.b64encode(flike.getvalue()).decode()
        plt.clf()
        #plt.cla()

        print("Analizando analisis1");
        return b64



        