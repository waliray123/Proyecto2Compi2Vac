
import pandas as pd
from matplotlib import pyplot as plt
from sklearn import preprocessing
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, r2_score
import io, base64


#Tendencia de la infección por Covid-19 en un País.
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

        #Preparar grafos
        fig, axs = plt.subplots(2, 2)
        #Prediccion 1 dia despues

        x_new_min = menorDia
        x_new_max = mayorDia + 1

        X_NEW = np.arange(x_new_max).reshape(-1,1)  

        X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)  
        Y_NEW = model.predict(X_NEW_TRANSF)  

        axs[0,0].scatter(X,Y) 

        axs[0,0].plot(X_NEW, Y_NEW, color='coral', linewidth=3)  

        axs[0,0].grid()  
        axs[0,0].set_xlim(x_new_min,x_new_max)  
        axs[0,0].set_ylim(menorInf,mayorInf)  

        axs[0,0].set_title('Tendencia de infeccion actual', fontsize=10)
        axs[0,0].set_xlabel('Dia')
        axs[0,0].set_ylabel('Infectados ') 

        prediccion1 = Y_NEW[-1]

        #Prediccion a 1 mes
        x_new_min = menorDia
        x_new_max = mayorDia + 30

        X_NEW = np.arange(x_new_max).reshape(-1,1)  

        X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)  
        Y_NEW = model.predict(X_NEW_TRANSF)  

        prediccion2 = Y_NEW[-1]

        axs[0,1].scatter(X,Y) 

        axs[0,1].plot(X_NEW, Y_NEW, color='coral', linewidth=3)  

        axs[0,1].grid()  
        axs[0,1].set_xlim(x_new_min,x_new_max)  
        axs[0,1].set_ylim(menorInf,prediccion2)  

        axs[0,1].set_title('Tendencia de infeccion a 1 mes', fontsize=10)
        axs[0,1].set_xlabel('Dia')
        axs[0,1].set_ylabel('Infectados ') 

        #Prediccion a 6 meses
        x_new_min = menorDia
        x_new_max = mayorDia + 180

        X_NEW = np.arange(x_new_max).reshape(-1,1)  

        X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)  
        Y_NEW = model.predict(X_NEW_TRANSF) 

        prediccion3 = Y_NEW[-1]

        axs[1,0].scatter(X,Y) 

        axs[1,0].plot(X_NEW, Y_NEW, color='coral', linewidth=3)  

        axs[1,0].grid()  
        axs[1,0].set_xlim(x_new_min,x_new_max)  
        axs[1,0].set_ylim(menorInf,prediccion3)  

        axs[1,0].set_title('\nTendencia de infeccion a 6 meses', fontsize=10)
        axs[1,0].set_xlabel('Dia')
        axs[1,0].set_ylabel('Infectados ') 



        #Prediccion a 1 anio
        x_new_min = menorDia
        x_new_max = mayorDia + 365

        X_NEW = np.arange(x_new_max).reshape(-1,1)  

        X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)  
        Y_NEW = model.predict(X_NEW_TRANSF)  

        prediccion4 = Y_NEW[-1]

        axs[1,1].scatter(X,Y) 

        axs[1,1].plot(X_NEW, Y_NEW, color='coral', linewidth=3)  

        axs[1,1].grid()  
        axs[1,1].set_xlim(x_new_min,x_new_max)  
        axs[1,1].set_ylim(menorInf,prediccion4)  

        axs[1,1].set_title('\nTendencia de infeccion 1 Anio', fontsize=10)
        axs[1,1].set_xlabel('Dia')
        axs[1,1].set_ylabel('Infectados ') 


        
        #Generar imagen y retornarla                                             
        flike = io.BytesIO()
        plt.savefig(flike)
        b64 = base64.b64encode(flike.getvalue()).decode()        
        #plt.clf()
        plt.cla()

        #Retornar un arreglo que contenga la descripcion y el grafico
        arrReturn =[any]*3
        arrReturn[0] = b64        

        #Generar una descripcion
        descripcion = ""
        descripcion += " Los datos fueron obtenidos mediante una funcion polinomial de tercer grado brindada por sklearn\n"
        descripcion += " Esta funcion presento los siguientes resultados:\n"
        descripcion += " RMSE : " + str(rmse) + "\n"
        descripcion += " R2 : " + str(r2) + "\n"

        descripcion += "\nLa tendencia de infeccion en el pais: "+ self.nombrePais + ", se realiza mediante varias perspectivas, la primera es al dia siguiente"
        descripcion += "donde se obtiene una prediccion de "+str(prediccion1) + " infectados, la segunda se observa hacia un futuro cercano, un mes para ser exactos"
        descripcion += "donde se obtiene una prediccion de "+str(prediccion2) + " infectados, la tercera se observa igual hacia seis meses adelante"
        descripcion += "donde se obtiene una prediccion de "+str(prediccion3) + " infectados, y la ultima se realiza hacia un año adelante"
        descripcion += "donde se obtiene una prediccion de "+str(prediccion4) + " infectados, entonces podemos "
        if prediccion1 > prediccion4:
            descripcion += "concluir que al cabo de un año obtendremos menos infectados que en el mes cercano, por lo que se puede decir que tendera a bajar el numero de infectados en un año"            
        else:
            descripcion += "concluir que al cabo de un año obtendremos mas infectados que en el mes cercano, por lo que se puede decir que tendera a subir el numero de infectados en un año"    

        arrReturn[1] = descripcion         

        return arrReturn

#Predicción de Infectados en un País.
class Analisis2():
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

        #Preparar grafos
        fig, axs = plt.subplots(2, 2)
        #Prediccion 1 dia despues

        x_new_min = menorDia
        x_new_max = mayorDia + 1

        X_NEW = np.arange(x_new_max).reshape(-1,1)  

        X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)  
        Y_NEW = model.predict(X_NEW_TRANSF)  

        axs[0,0].scatter(X,Y) 

        axs[0,0].plot(X_NEW, Y_NEW, color='coral', linewidth=3)  

        axs[0,0].grid()  
        axs[0,0].set_xlim(x_new_min,x_new_max)  
        axs[0,0].set_ylim(menorInf,mayorInf)  

        axs[0,0].set_title('Tendencia de infeccion actual', fontsize=10)
        axs[0,0].set_xlabel('Dia')
        axs[0,0].set_ylabel('Infectados ') 

        prediccion1 = Y_NEW[-1]

        #Prediccion a 1 mes
        x_new_min = menorDia
        x_new_max = mayorDia + 30

        X_NEW = np.arange(x_new_max).reshape(-1,1)  

        X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)  
        Y_NEW = model.predict(X_NEW_TRANSF)  

        prediccion2 = Y_NEW[-1]

        axs[0,1].scatter(X,Y) 

        axs[0,1].plot(X_NEW, Y_NEW, color='coral', linewidth=3)  

        axs[0,1].grid()  
        axs[0,1].set_xlim(x_new_min,x_new_max)  
        axs[0,1].set_ylim(menorInf,prediccion2)  

        axs[0,1].set_title('Tendencia de infeccion a 1 mes', fontsize=10)
        axs[0,1].set_xlabel('Dia')
        axs[0,1].set_ylabel('Infectados ') 

        #Prediccion a 6 meses
        x_new_min = menorDia
        x_new_max = mayorDia + 180

        X_NEW = np.arange(x_new_max).reshape(-1,1)  

        X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)  
        Y_NEW = model.predict(X_NEW_TRANSF) 

        prediccion3 = Y_NEW[-1]

        axs[1,0].scatter(X,Y) 

        axs[1,0].plot(X_NEW, Y_NEW, color='coral', linewidth=3)  

        axs[1,0].grid()  
        axs[1,0].set_xlim(x_new_min,x_new_max)  
        axs[1,0].set_ylim(menorInf,prediccion3)  

        axs[1,0].set_title('\nTendencia de infeccion a 6 meses', fontsize=10)
        axs[1,0].set_xlabel('Dia')
        axs[1,0].set_ylabel('Infectados ') 



        #Prediccion a 1 anio
        x_new_min = menorDia
        x_new_max = mayorDia + 365

        X_NEW = np.arange(x_new_max).reshape(-1,1)  

        X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)  
        Y_NEW = model.predict(X_NEW_TRANSF)  

        prediccion4 = Y_NEW[-1]

        axs[1,1].scatter(X,Y) 

        axs[1,1].plot(X_NEW, Y_NEW, color='coral', linewidth=3)  

        axs[1,1].grid()  
        axs[1,1].set_xlim(x_new_min,x_new_max)  
        axs[1,1].set_ylim(menorInf,prediccion4)  

        axs[1,1].set_title('\nPredicción de Infertados en un País', fontsize=10)
        axs[1,1].set_xlabel('Dia')
        axs[1,1].set_ylabel('Infectados ') 


        
        #Generar imagen y retornarla                                             
        flike = io.BytesIO()
        plt.savefig(flike)
        b64 = base64.b64encode(flike.getvalue()).decode()
        #plt.clf()
        plt.cla()

        #Retornar un arreglo que contenga la descripcion y el grafico
        arrReturn =[any]*2
        arrReturn[0] = b64

        #Generar una descripcion
        descripcion = ""
        descripcion += " Los datos fueron obtenidos mediante una funcion polinomial de tercer grado brindada por sklearn\n"
        descripcion += " Esta funcion presento los siguientes resultados:\n"
        descripcion += " RMSE : " + str(rmse) + "\n"
        descripcion += " R2 : " + str(r2) + "\n"

        descripcion += "\nLa tendencia de infeccion en el pais: "+ self.nombrePais + ", se realiza mediante varias perspectivas, la primera es al dia siguiente"
        descripcion += "donde se obtiene una prediccion de "+str(prediccion1) + " infectados, la segunda se observa hacia un futuro cercano, un mes para ser exactos"
        descripcion += "donde se obtiene una prediccion de "+str(prediccion2) + " infectados, la tercera se observa igual hacia seis meses adelante"
        descripcion += "donde se obtiene una prediccion de "+str(prediccion3) + " infectados, y la ultima se realiza hacia un año adelante"
        descripcion += "donde se obtiene una prediccion de "+str(prediccion4) + " infectados, entonces podemos "
        if prediccion1 > prediccion4:
            descripcion += "concluir que al cabo de un año obtendremos menos infectados que en el mes cercano, por lo que se puede decir que tendera a bajar el numero de infectados en un año"            
        else:
            descripcion += "concluir que al cabo de un año obtendremos mas infectados que en el mes cercano, por lo que se puede decir que tendera a subir el numero de infectados en un año"    

        arrReturn[1] = descripcion         

        return arrReturn

#Indice de Progresión de la pandemia.
class Analisis3():
    nombrePais = ''
    campoPaises = ''
    campodia = ''
    camponum = ''
    camponumIsopado = ''
    archivoEn = any
    diaProyeccion = 0

    def __init__(self,nombrePais,campoPaises,campodia,camponum,archivoEn,camponumIsopado,cantidadDias):
        self.nombrePais = nombrePais
        self.campoPaises = campoPaises
        self.campodia = campodia
        self.camponum = camponum
        self.archivoEn = archivoEn
        self.diaProyeccion = cantidadDias
        self.camponumIsopado = camponumIsopado
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
        Y1 = dfPais[self.camponum]          #Numero de infectados
        Y2 = dfPais[self.camponumIsopado]   #Numero de isopados realizados ese dia

        #Obtener el mayor dia y el menor
        menorDia = np.amin(X)
        mayorDia = np.amax(X)
        
        #Definimos el modelo

        nb_degree = 3
        polynomial_features = PolynomialFeatures(degree = nb_degree) 

        X_TRANSF = polynomial_features.fit_transform(X)

        # Entrenamos el modelo

        model1 = LinearRegression() 
        model1.fit(X_TRANSF, Y1)  
        Y1_NEW = model1.predict(X_TRANSF)  

        model2 = LinearRegression()
        model2.fit(X_TRANSF,Y2)
        Y2_NEW = model2.predict(X_TRANSF)  

        #Obtenemos el error y el r cuadrado
        indice = -1;
        npi = 0
        npi1 = 0
        tsi =0
        tsi1 =0 
        numDia = int(self.diaProyeccion)
        if int(self.diaProyeccion) > 0:
            #Realizar el calculo
            if int(self.diaProyeccion) <= mayorDia:
                #Realizar el calculo dentro de los dias dados
                npi = Y1[numDia]
                npi1 = Y1[numDia-1]
                tsi = Y2[numDia]
                tsi1 = Y2[numDia-1]
                indice = (npi-npi1)/(tsi-tsi1)                
            else:
                #Realizar una prediccion y realizar el calculo en base a ellos                
                #Obtener npi                
                x_new_max = numDia
                X_NEW = np.arange(x_new_max).reshape(-1,1)
                X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)
                Y1_NEW = model1.predict(X_NEW_TRANSF)
                npi = Y1_NEW[-1]

                #Obtener npi-1
                x_new_max = numDia-1
                X_NEW = np.arange(x_new_max).reshape(-1,1)
                X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)
                Y1_NEW = model1.predict(X_NEW_TRANSF)
                npi1 = Y1_NEW[-1]

                #Obtener tsi
                x_new_max = numDia
                X_NEW = np.arange(x_new_max).reshape(-1,1)
                X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)
                Y2_NEW = model1.predict(X_NEW_TRANSF)
                tsi = Y2_NEW[-1]

                #Obtener tsi-1
                x_new_max = numDia-1
                X_NEW = np.arange(x_new_max).reshape(-1,1)
                X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)
                Y2_NEW = model1.predict(X_NEW_TRANSF)
                tsi1 = Y2_NEW[-1]

                #Obtener el indice
                indice = (npi-npi1)/(tsi-tsi1)                
        else:
            #Retornar error: No se puede calcular el indice en el dia 0
            print("Error: No se puede calcular el indice en el dia 0")

        print(indice)

        descripcion = "El indice de progresion de la pandemia se mide de la siguiente manera: \n"
        descripcion += "es una medida del porcentaje de personas infectadas con respecto al número de hisopados realizados.\n"
        descripcion += "este indice indica que tan fuerte es la propagacion de la pandemia. La siguiente formula es la utilizada para calcularlo\n"
        descripcion += "Indice de progresion de la pandemia = (npi-npi1)/(tsi-tsi1)\n"
        descripcion += "Donde npi es el numero de infectados en el dia i, y npi1 es el numero de infectados en el dia i-1, "
        descripcion += "asi como tambien tsi es el numero de hisopados realizados el dia i y tsi1 es el numero de hisopados realizados el dia i-1"
        descripcion += "Este indice se presenta en numero entre 0 y 1 donde 1 significa un avance en la epidemia y 0 y detenimiento\n"
        descripcion += "Segun la informacion que se proporciono se obtubieron los siguientes resultados: \n"
        descripcion += "npi : "+ str(npi) + "\n"
        descripcion += "npi1 : "+ str(npi1) + "\n"
        descripcion += "tsi : "+ str(tsi) + "\n"
        descripcion += "tsi1 : "+ str(tsi1) + "\n"
        descripcion += "Indice = "+ str(indice) + "\n"        
        descripcion += "Por lo que podemos concluir en base al indice que :"

        if indice == 0:
            descripcion += "Esperamos que la epidemia se detenga\n"
        elif indice <= 0.1 and indice > 0:
            descripcion += "Esperamos que la epidemia siga disminuyendo hasta detener\n"
        elif indice <= 0.5 and indice > 0.1:
            descripcion += "Por el momento la pandemia seguira avanzando con una constante disminucion\n"
        elif indice <=0.7 and indice > 0.5:
            descripcion += "La pandemia seguira avanzando aunque su propagacion empieza a dismunuir\n"
        elif indice > 0.7 and indice <= 1:
            descripcion += "La infeccion en la pandemia es demasiado alto, la pandemia seguira avanzando\n"

        descripcion += "Para realizar el calculo de este indice se utilizan los datos brindados en el documento, si en dado caso el dia esta mas alla"
        descripcion += "de los dias brindados se realiza una prediccion con sklearn de forma polinomial de 3er grado para obtener asi npi, npi1, tsi y tsi1.\n"
        

        print("Analizar Indice de proyeccion de la pandemia")
        return descripcion

#Predicción de mortalidad por COVID en un Departamento.
class Analisis4(): 
    nombrePais = ''
    campoPaises = ''
    campoDepartamento = ''
    campodia = ''
    camponum = ''
    archivoEn = any
    diasPrediccion = 0


    def __init__(self,nombrePais,campoPaises,campodia,camponum,archivoEn,campoDepartamento):
        self.nombrePais = nombrePais
        self.campoPaises = campoPaises
        self.campodia = campodia
        self.camponum = camponum
        self.archivoEn = archivoEn
        self.campoDepartamento = campoDepartamento

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

        #Obtener todos los datos que son del departamento
        dfDep = dfPais[self.campoDepartamento]

        #Crear un array del largo de los dias y que represente las fechas en su valor

        lbl_enc = preprocessing.LabelEncoder()
        diasLimpios = lbl_enc.fit_transform(dfDep[self.campodia])


        X = np.array(diasLimpios).reshape(-1,1)
        Y = dfDep[self.camponum]

        #Obtener el mayor dia y el menor
        menorDia = np.amin(X)
        mayorDia = np.amax(X)
        #Obtener el mayor numero de infectados y el menor
        menorInf = np.amin(Y) 
        mayorInf = np.amax(Y) 

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

        #Preparar grafos
        fig, axs = plt.subplots(2, 2)
        #Prediccion 1 dia despues

        x_new_min = menorDia
        x_new_max = mayorDia + 1

        X_NEW = np.arange(x_new_max).reshape(-1,1)  

        X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)  
        Y_NEW = model.predict(X_NEW_TRANSF)  

        axs[0,0].scatter(X,Y) 

        axs[0,0].plot(X_NEW, Y_NEW, color='coral', linewidth=3)  

        axs[0,0].grid()  
        axs[0,0].set_xlim(x_new_min,x_new_max)  
        axs[0,0].set_ylim(menorInf,mayorInf)  

        axs[0,0].set_title('Tendencia de infeccion actual', fontsize=10)
        axs[0,0].set_xlabel('Dia')
        axs[0,0].set_ylabel('Infectados ') 

        prediccion1 = Y_NEW[-1]

        #Prediccion a 1 mes
        x_new_min = menorDia
        x_new_max = mayorDia + 30

        X_NEW = np.arange(x_new_max).reshape(-1,1)  

        X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)  
        Y_NEW = model.predict(X_NEW_TRANSF)  

        prediccion2 = Y_NEW[-1]

        axs[0,1].scatter(X,Y) 

        axs[0,1].plot(X_NEW, Y_NEW, color='coral', linewidth=3)  

        axs[0,1].grid()  
        axs[0,1].set_xlim(x_new_min,x_new_max)  
        axs[0,1].set_ylim(menorInf,prediccion2)  

        axs[0,1].set_title('Tendencia de infeccion a 1 mes', fontsize=10)
        axs[0,1].set_xlabel('Dia')
        axs[0,1].set_ylabel('Infectados ') 

        #Prediccion a 6 meses
        x_new_min = menorDia
        x_new_max = mayorDia + 180

        X_NEW = np.arange(x_new_max).reshape(-1,1)  

        X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)  
        Y_NEW = model.predict(X_NEW_TRANSF) 

        prediccion3 = Y_NEW[-1]

        axs[1,0].scatter(X,Y) 

        axs[1,0].plot(X_NEW, Y_NEW, color='coral', linewidth=3)  

        axs[1,0].grid()  
        axs[1,0].set_xlim(x_new_min,x_new_max)  
        axs[1,0].set_ylim(menorInf,prediccion3)  

        axs[1,0].set_title('\nTendencia de infeccion a 6 meses', fontsize=10)
        axs[1,0].set_xlabel('Dia')
        axs[1,0].set_ylabel('Infectados ') 



        #Prediccion a 1 anio
        x_new_min = menorDia
        x_new_max = mayorDia + 365

        X_NEW = np.arange(x_new_max).reshape(-1,1)  

        X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)  
        Y_NEW = model.predict(X_NEW_TRANSF)  

        prediccion4 = Y_NEW[-1]

        axs[1,1].scatter(X,Y) 

        axs[1,1].plot(X_NEW, Y_NEW, color='coral', linewidth=3)  

        axs[1,1].grid()  
        axs[1,1].set_xlim(x_new_min,x_new_max)  
        axs[1,1].set_ylim(menorInf,prediccion4)  

        axs[1,1].set_title('\nTendencia de infeccion 1 Anio', fontsize=10)
        axs[1,1].set_xlabel('Dia')
        axs[1,1].set_ylabel('Infectados ') 


        
        #Generar imagen y retornarla                                             
        flike = io.BytesIO()
        plt.savefig(flike)
        b64 = base64.b64encode(flike.getvalue()).decode()
        #plt.clf()
        plt.cla()

        #Retornar un arreglo que contenga la descripcion y el grafico
        arrReturn =[any]*2
        arrReturn[0] = b64

        #Generar una descripcion
        descripcion = ""
        descripcion += " Los datos fueron obtenidos mediante una funcion polinomial de tercer grado brindada por sklearn\n"
        descripcion += " Esta funcion presento los siguientes resultados:\n"
        descripcion += " RMSE : " + str(rmse) + "\n"
        descripcion += " R2 : " + str(r2) + "\n"

        descripcion += "\nLa prediccion mortalidad por casos de corononavirus en el pais: "+ self.nombrePais + ", y departamento " + self.campoDepartamento
        descripcion += ", se realiza mediante varias perspectivas, la primera es al dia siguiente"
        descripcion += "donde se obtiene una prediccion de "+str(prediccion1) + " infectados, la segunda se observa hacia un futuro cercano, un mes para ser exactos"
        descripcion += "donde se obtiene una prediccion de "+str(prediccion2) + " infectados, la tercera se observa igual hacia seis meses adelante"
        descripcion += "donde se obtiene una prediccion de "+str(prediccion3) + " infectados, y la ultima se realiza hacia un año adelante"
        descripcion += "donde se obtiene una prediccion de "+str(prediccion4) + " infectados, entonces podemos "
        if prediccion1 > prediccion4:
            descripcion += "concluir que al cabo de un año obtendremos menos infectados que en el mes cercano, por lo que se puede decir que tendera a bajar el numero de muertes en un año"            
        else:
            descripcion += "concluir que al cabo de un año obtendremos mas infectados que en el mes cercano, por lo que se puede decir que tendera a subir el numero de muertes en un año"    

        arrReturn[1] = descripcion         

        return arrReturn

#Predicción de mortalidad por COVID en un Pais.
class Analisis5(): 
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

        #Preparar grafos
        fig, axs = plt.subplots(2, 2)
        #Prediccion 1 dia despues

        x_new_min = menorDia
        x_new_max = mayorDia + 1

        X_NEW = np.arange(x_new_max).reshape(-1,1)  

        X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)  
        Y_NEW = model.predict(X_NEW_TRANSF)  

        axs[0,0].scatter(X,Y) 

        axs[0,0].plot(X_NEW, Y_NEW, color='coral', linewidth=3)  

        axs[0,0].grid()  
        axs[0,0].set_xlim(x_new_min,x_new_max)  
        axs[0,0].set_ylim(menorInf,mayorInf)  

        axs[0,0].set_title('Tendencia de infeccion actual', fontsize=10)
        axs[0,0].set_xlabel('Dia')
        axs[0,0].set_ylabel('Infectados ') 

        prediccion1 = Y_NEW[-1]

        #Prediccion a 1 mes
        x_new_min = menorDia
        x_new_max = mayorDia + 30

        X_NEW = np.arange(x_new_max).reshape(-1,1)  

        X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)  
        Y_NEW = model.predict(X_NEW_TRANSF)  

        prediccion2 = Y_NEW[-1]

        axs[0,1].scatter(X,Y) 

        axs[0,1].plot(X_NEW, Y_NEW, color='coral', linewidth=3)  

        axs[0,1].grid()  
        axs[0,1].set_xlim(x_new_min,x_new_max)  
        axs[0,1].set_ylim(menorInf,prediccion2)  

        axs[0,1].set_title('Tendencia de infeccion a 1 mes', fontsize=10)
        axs[0,1].set_xlabel('Dia')
        axs[0,1].set_ylabel('Infectados ') 

        #Prediccion a 6 meses
        x_new_min = menorDia
        x_new_max = mayorDia + 180

        X_NEW = np.arange(x_new_max).reshape(-1,1)  

        X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)  
        Y_NEW = model.predict(X_NEW_TRANSF) 

        prediccion3 = Y_NEW[-1]

        axs[1,0].scatter(X,Y) 

        axs[1,0].plot(X_NEW, Y_NEW, color='coral', linewidth=3)  

        axs[1,0].grid()  
        axs[1,0].set_xlim(x_new_min,x_new_max)  
        axs[1,0].set_ylim(menorInf,prediccion3)  

        axs[1,0].set_title('\nTendencia de infeccion a 6 meses', fontsize=10)
        axs[1,0].set_xlabel('Dia')
        axs[1,0].set_ylabel('Infectados ') 



        #Prediccion a 1 anio
        x_new_min = menorDia
        x_new_max = mayorDia + 365

        X_NEW = np.arange(x_new_max).reshape(-1,1)  

        X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)  
        Y_NEW = model.predict(X_NEW_TRANSF)  

        prediccion4 = Y_NEW[-1]

        axs[1,1].scatter(X,Y) 

        axs[1,1].plot(X_NEW, Y_NEW, color='coral', linewidth=3)  

        axs[1,1].grid()  
        axs[1,1].set_xlim(x_new_min,x_new_max)  
        axs[1,1].set_ylim(menorInf,prediccion4)  

        axs[1,1].set_title('\nTendencia de infeccion 1 Anio', fontsize=10)
        axs[1,1].set_xlabel('Dia')
        axs[1,1].set_ylabel('Infectados ') 


        
        #Generar imagen y retornarla                                             
        flike = io.BytesIO()
        plt.savefig(flike)
        b64 = base64.b64encode(flike.getvalue()).decode()
        #plt.clf()
        plt.cla()

        #Retornar un arreglo que contenga la descripcion y el grafico
        arrReturn =[any]*2
        arrReturn[0] = b64

        #Generar una descripcion
        descripcion = ""
        descripcion += " Los datos fueron obtenidos mediante una funcion polinomial de tercer grado brindada por sklearn\n"
        descripcion += " Esta funcion presento los siguientes resultados:\n"
        descripcion += " RMSE : " + str(rmse) + "\n"
        descripcion += " R2 : " + str(r2) + "\n"

        descripcion += "\nLa prediccion mortalidad por casos de corononavirus en el pais: "+ self.nombrePais
        descripcion += ", se realiza mediante varias perspectivas, la primera es al dia siguiente"
        descripcion += "donde se obtiene una prediccion de "+str(prediccion1) + " infectados, la segunda se observa hacia un futuro cercano, un mes para ser exactos"
        descripcion += "donde se obtiene una prediccion de "+str(prediccion2) + " infectados, la tercera se observa igual hacia seis meses adelante"
        descripcion += "donde se obtiene una prediccion de "+str(prediccion3) + " infectados, y la ultima se realiza hacia un año adelante"
        descripcion += "donde se obtiene una prediccion de "+str(prediccion4) + " infectados, entonces podemos "
        if prediccion1 > prediccion4:
            descripcion += "concluir que al cabo de un año obtendremos menos infectados que en el mes cercano, por lo que se puede decir que tendera a bajar el numero de muertes en un año"            
        else:
            descripcion += "concluir que al cabo de un año obtendremos mas infectados que en el mes cercano, por lo que se puede decir que tendera a subir el numero de muertes en un año"    

        arrReturn[1] = descripcion         

        return arrReturn

#Análisis del número de muertes por coronavirus en un País.
class Analisis6(): 
    nombrePais = ''
    campoPaises = ''    
    campodia = ''
    camponum = ''
    archivoEn = any    


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

        #Definimos el modelo en este caso es lineal ya que es el mas comun en el analisis de 2 datos bastante dispersos

        regr = LinearRegression()

        regr.fit(X,Y)

        Y_PRED = regr.predict(X)

        prediccion1 = regr.predict([[mayorDia+1]])
        prediccion2 = regr.predict([[mayorDia+365]])

        r2 = r2_score(Y,Y_PRED)        
        rmse = np.sqrt(mean_squared_error(Y,Y_PRED))         

        plt.scatter(X,Y,color="black")
        plt.plot(X,Y_PRED,color="blue")

        plt.ylim(menorInf,mayorInf) 


        
        #Generar imagen y retornarla                                             
        flike = io.BytesIO()
        plt.savefig(flike)
        b64 = base64.b64encode(flike.getvalue()).decode()
        #plt.clf()
        plt.cla()

        #Retornar un arreglo que contenga la descripcion y el grafico
        arrReturn =[any]*2
        arrReturn[0] = b64

        #Generar una descripcion
        descripcion = ""
        descripcion += " Los datos fueron obtenidos mediante una funcion lineal brindada por sklearn\n"
        descripcion += " Esta funcion presento los siguientes resultados:\n"
        descripcion += " RMSE : " + str(rmse) + "\n"
        descripcion += " R2 : " + str(r2) + "\n"

        descripcion += " El modelo que presento mediante el entrenamiento segun los datos brindados es el siguiente: \n"
        descripcion += " Y = " + str(regr.coef_[0][0]) + "X+" + str(regr.intercept_[0]) + "\n"

        descripcion += "\nLa prediccion mortalidad por casos de corononavirus en el pais: "+ self.nombrePais
        descripcion += ", se realiza mediante varias perspectivas, la primera es al dia siguiente"
        descripcion += " donde se obtiene una prediccion de "+str(prediccion1) + " infectados, la segunda se observa hacia futuro ,año despues del ultimo para ser exactos"                
        descripcion += " donde se obtiene una prediccion de "+str(prediccion2) + " infectados.\n"

        descripcion += " Analizando el modelo que se presento se comcluye que: \n"
        if str(regr.coef_[0][0]) < 0:
            descripcion += " Las muertes en el pais estaran disminuyendo\n"
        else:
            descripcion += " Las muertes en el pais estaran aumentando\n"                

        arrReturn[1] = descripcion         

        return arrReturn

#Tendencia del número de infectados por día de un País.
class Analisis7():
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

        #Preparar grafos
        fig, axs = plt.subplots(2, 2)
        #Prediccion 1 dia despues

        x_new_min = menorDia
        x_new_max = mayorDia + 1

        X_NEW = np.arange(x_new_max).reshape(-1,1)  

        X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)  
        Y_NEW = model.predict(X_NEW_TRANSF)  

        axs[0,0].scatter(X,Y) 

        axs[0,0].plot(X_NEW, Y_NEW, color='coral', linewidth=3)  

        axs[0,0].grid()  
        axs[0,0].set_xlim(x_new_min,x_new_max)  
        axs[0,0].set_ylim(menorInf,mayorInf)  

        axs[0,0].set_title('Tendencia de infectados actual', fontsize=10)
        axs[0,0].set_xlabel('Dia')
        axs[0,0].set_ylabel('Infectados ') 

        prediccion1 = Y_NEW[-1]

        #Prediccion a 1 mes
        x_new_min = menorDia
        x_new_max = mayorDia + 30

        X_NEW = np.arange(x_new_max).reshape(-1,1)  

        X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)  
        Y_NEW = model.predict(X_NEW_TRANSF)  

        prediccion2 = Y_NEW[-1]

        axs[0,1].scatter(X,Y) 

        axs[0,1].plot(X_NEW, Y_NEW, color='coral', linewidth=3)  

        axs[0,1].grid()  
        axs[0,1].set_xlim(x_new_min,x_new_max)  
        axs[0,1].set_ylim(menorInf,prediccion2)  

        axs[0,1].set_title('Tendencia de infectados a 1 mes', fontsize=10)
        axs[0,1].set_xlabel('Dia')
        axs[0,1].set_ylabel('Infectados ') 

        #Prediccion a 6 meses
        x_new_min = menorDia
        x_new_max = mayorDia + 180

        X_NEW = np.arange(x_new_max).reshape(-1,1)  

        X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)  
        Y_NEW = model.predict(X_NEW_TRANSF) 

        prediccion3 = Y_NEW[-1]

        axs[1,0].scatter(X,Y) 

        axs[1,0].plot(X_NEW, Y_NEW, color='coral', linewidth=3)  

        axs[1,0].grid()  
        axs[1,0].set_xlim(x_new_min,x_new_max)  
        axs[1,0].set_ylim(menorInf,prediccion3)  

        axs[1,0].set_title('\nTendencia de infectados a 6 meses', fontsize=10)
        axs[1,0].set_xlabel('Dia')
        axs[1,0].set_ylabel('Infectados ') 



        #Prediccion a 1 anio
        x_new_min = menorDia
        x_new_max = mayorDia + 365

        X_NEW = np.arange(x_new_max).reshape(-1,1)  

        X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)  
        Y_NEW = model.predict(X_NEW_TRANSF)  

        prediccion4 = Y_NEW[-1]

        axs[1,1].scatter(X,Y) 

        axs[1,1].plot(X_NEW, Y_NEW, color='coral', linewidth=3)  

        axs[1,1].grid()  
        axs[1,1].set_xlim(x_new_min,x_new_max)  
        axs[1,1].set_ylim(menorInf,prediccion4)  

        axs[1,1].set_title('\nTendencia de infectados 1 Anio', fontsize=10)
        axs[1,1].set_xlabel('Dia')
        axs[1,1].set_ylabel('Infectados ') 


        
        #Generar imagen y retornarla                                             
        flike = io.BytesIO()
        plt.savefig(flike)
        b64 = base64.b64encode(flike.getvalue()).decode()        
        #plt.clf()
        plt.cla()

        #Retornar un arreglo que contenga la descripcion y el grafico
        arrReturn =[any]*3
        arrReturn[0] = b64        

        #Generar una descripcion
        descripcion = ""
        descripcion += " Los datos fueron obtenidos mediante una funcion polinomial de tercer grado brindada por sklearn\n"
        descripcion += " Esta funcion presento los siguientes resultados:\n"
        descripcion += " RMSE : " + str(rmse) + "\n"
        descripcion += " R2 : " + str(r2) + "\n"

        descripcion += "\nLa tendencia de infeccion en el pais: "+ self.nombrePais + ", se realiza mediante varias perspectivas, la primera es al dia siguiente"
        descripcion += "donde se obtiene una prediccion de "+str(prediccion1) + " infectados, la segunda se observa hacia un futuro cercano, un mes para ser exactos"
        descripcion += "donde se obtiene una prediccion de "+str(prediccion2) + " infectados, la tercera se observa igual hacia seis meses adelante"
        descripcion += "donde se obtiene una prediccion de "+str(prediccion3) + " infectados, y la ultima se realiza hacia un año adelante"
        descripcion += "donde se obtiene una prediccion de "+str(prediccion4) + " infectados, entonces podemos "
        if prediccion1 > prediccion4:
            descripcion += "concluir que al cabo de un año obtendremos menos infectados que en el mes cercano, por lo que se puede decir que tendera a bajar el numero de infectados en un año"            
        else:
            descripcion += "concluir que al cabo de un año obtendremos mas infectados que en el mes cercano, por lo que se puede decir que tendera a subir el numero de infectados en un año"    

        arrReturn[1] = descripcion         

        return arrReturn

#Predicción de casos de un país para un año.
class Analisis8():
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
        #Prediccion a 1 anio
        x_new_min = menorDia
        x_new_max = mayorDia + 365

        X_NEW = np.arange(x_new_max).reshape(-1,1)  

        X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)  
        Y_NEW = model.predict(X_NEW_TRANSF)  

        prediccion1 = Y_NEW[-1]

        plt.scatter(X,Y) 

        plt.plot(X_NEW, Y_NEW, color='coral', linewidth=3)  

        plt.grid()  
        plt.set_xlim(x_new_min,x_new_max)  
        plt.set_ylim(menorInf,prediccion1)  

        plt.set_title('\nTendencia de infeccion 1 Anio', fontsize=10)
        plt.set_xlabel('Dia')
        plt.set_ylabel('Infectados ') 


        
        #Generar imagen y retornarla                                             
        flike = io.BytesIO()
        plt.savefig(flike)
        b64 = base64.b64encode(flike.getvalue()).decode()
        #plt.clf()
        plt.cla()

        #Retornar un arreglo que contenga la descripcion y el grafico
        arrReturn =[any]*2
        arrReturn[0] = b64

        #Generar una descripcion
        descripcion = ""
        descripcion += " Los datos fueron obtenidos mediante una funcion polinomial de tercer grado brindada por sklearn\n"
        descripcion += " Esta funcion presento los siguientes resultados:\n"
        descripcion += " RMSE : " + str(rmse) + "\n"
        descripcion += " R2 : " + str(r2) + "\n"
        #se realiza hacia un año adelante
        descripcion += "\nLa tendencia de infeccion en el pais: "+ self.nombrePais + ", se realiza mediante varias perspectivas, la primera es al dia siguiente"
        descripcion += " donde se obtiene una prediccion de "+str(prediccion1) + " infectados."

        arrReturn[1] = descripcion         

        return arrReturn

#Tendencia de la vacunación de en un País.
class Analisis9():
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

        #Preparar grafos
        fig, axs = plt.subplots(2, 2)
        #Prediccion 1 dia despues

        x_new_min = menorDia
        x_new_max = mayorDia + 1

        X_NEW = np.arange(x_new_max).reshape(-1,1)  

        X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)  
        Y_NEW = model.predict(X_NEW_TRANSF)  

        axs[0,0].scatter(X,Y) 

        axs[0,0].plot(X_NEW, Y_NEW, color='coral', linewidth=3)  

        axs[0,0].grid()  
        axs[0,0].set_xlim(x_new_min,x_new_max)  
        axs[0,0].set_ylim(menorInf,mayorInf)  

        axs[0,0].set_title('Tendencia de vacunacion actual', fontsize=10)
        axs[0,0].set_xlabel('Dia')
        axs[0,0].set_ylabel('Vacunados ') 

        prediccion1 = Y_NEW[-1]

        #Prediccion a 1 mes
        x_new_min = menorDia
        x_new_max = mayorDia + 30

        X_NEW = np.arange(x_new_max).reshape(-1,1)  

        X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)  
        Y_NEW = model.predict(X_NEW_TRANSF)  

        prediccion2 = Y_NEW[-1]

        axs[0,1].scatter(X,Y) 

        axs[0,1].plot(X_NEW, Y_NEW, color='coral', linewidth=3)  

        axs[0,1].grid()  
        axs[0,1].set_xlim(x_new_min,x_new_max)  
        axs[0,1].set_ylim(menorInf,prediccion2)  

        axs[0,1].set_title('Tendencia de vacunacion a 1 mes', fontsize=10)
        axs[0,1].set_xlabel('Dia')
        axs[0,1].set_ylabel('Vacunados ') 

        #Prediccion a 6 meses
        x_new_min = menorDia
        x_new_max = mayorDia + 180

        X_NEW = np.arange(x_new_max).reshape(-1,1)  

        X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)  
        Y_NEW = model.predict(X_NEW_TRANSF) 

        prediccion3 = Y_NEW[-1]

        axs[1,0].scatter(X,Y) 

        axs[1,0].plot(X_NEW, Y_NEW, color='coral', linewidth=3)  

        axs[1,0].grid()  
        axs[1,0].set_xlim(x_new_min,x_new_max)  
        axs[1,0].set_ylim(menorInf,prediccion3)  

        axs[1,0].set_title('\nTendencia de vacunacion a 6 meses', fontsize=10)
        axs[1,0].set_xlabel('Dia')
        axs[1,0].set_ylabel('Vacunados ') 



        #Prediccion a 1 anio
        x_new_min = menorDia
        x_new_max = mayorDia + 365

        X_NEW = np.arange(x_new_max).reshape(-1,1)  

        X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)  
        Y_NEW = model.predict(X_NEW_TRANSF)  

        prediccion4 = Y_NEW[-1]

        axs[1,1].scatter(X,Y) 

        axs[1,1].plot(X_NEW, Y_NEW, color='coral', linewidth=3)  

        axs[1,1].grid()  
        axs[1,1].set_xlim(x_new_min,x_new_max)  
        axs[1,1].set_ylim(menorInf,prediccion4)  

        axs[1,1].set_title('\nTendencia de vacunacion 1 Año', fontsize=10)
        axs[1,1].set_xlabel('Dia')
        axs[1,1].set_ylabel('Vacunados ') 


        
        #Generar imagen y retornarla                                             
        flike = io.BytesIO()
        plt.savefig(flike)
        b64 = base64.b64encode(flike.getvalue()).decode()        
        #plt.clf()
        plt.cla()

        #Retornar un arreglo que contenga la descripcion y el grafico
        arrReturn =[any]*3
        arrReturn[0] = b64        

        #Generar una descripcion
        descripcion = ""
        descripcion += " Los datos fueron obtenidos mediante una funcion polinomial de tercer grado brindada por sklearn\n"
        descripcion += " Esta funcion presento los siguientes resultados:\n"
        descripcion += " RMSE : " + str(rmse) + "\n"
        descripcion += " R2 : " + str(r2) + "\n"

        descripcion += "\nLa tendencia de infeccion en el pais: "+ self.nombrePais + ", se realiza mediante varias perspectivas, la primera es al dia siguiente"
        descripcion += "donde se obtiene una prediccion de "+str(prediccion1) + " vacunados, la segunda se observa hacia un futuro cercano, un mes para ser exactos"
        descripcion += "donde se obtiene una prediccion de "+str(prediccion2) + " vacunados, la tercera se observa igual hacia seis meses adelante"
        descripcion += "donde se obtiene una prediccion de "+str(prediccion3) + " vacunados, y la ultima se realiza hacia un año adelante"
        descripcion += "donde se obtiene una prediccion de "+str(prediccion4) + " vacunados, entonces podemos "
        if prediccion1 > prediccion4:
            descripcion += "concluir que al cabo de un año obtendremos menos vacunados que en el mes cercano, por lo que se puede decir que tendera a bajar el numero de infectados en un año"            
        else:
            descripcion += "concluir que al cabo de un año obtendremos mas vacunados que en el mes cercano, por lo que se puede decir que tendera a subir el numero de infectados en un año"            

        arrReturn[1] = descripcion         

        return arrReturn

#Ánalisis Comparativo de Vacunaciópn entre 2 paises.
class Analisis10():
    nombrePais = ''
    nombrePais2 = ''
    campoPaises = ''
    campodia = ''
    camponum = ''
    archivoEn = any    


    def __init__(self,nombrePais,campoPaises,campodia,camponum,archivoEn,nombrePais2):
        self.nombrePais = nombrePais
        self.nombrePais2 = nombrePais2
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
        
        #Diferenciar los datos de los paises
        pais = np.asarray(df[self.campoPaises].str.contains(self.nombrePais))  
        pais2 =np.asarray(df[self.campoPaises].str.contains(self.nombrePais2))  

        #Obtener todos los datos que son del pais
        dfPais = df[pais]
        dfPais2 = df[pais2]
        
        #Crear un array del largo de los dias y que represente las fechas en su valor

        lbl_enc = preprocessing.LabelEncoder()
        diasLimpios = lbl_enc.fit_transform(dfPais[self.campodia])        

        X = np.array(diasLimpios).reshape(-1,1)
        Y = dfPais[self.camponum]
        Y2 = dfPais2[self.camponum]

        #Obtener el mayor dia y el menor
        menorDia = np.amin(X)
        mayorDia = np.amax(X)
        #Obtener el mayor numero de vacunas y el menor
        menorInf1 = np.amin(Y) 
        mayorInf1 = np.amax(Y) 

        menorInf2 = np.amin(Y2) 
        mayorInf2 = np.amax(Y2) 

        #Definimos el modelo en este caso es lineal ya que es el mas comun en el analisis de 2 datos bastante dispersos

        regr = LinearRegression()
        regr2 = LinearRegression()

        regr.fit(X,Y)
        regr2.fit(X,Y2)

        #Preparamos las figuras
        fig, axs = plt.subplots(2)


        #Realizar prediccion En pais 1
        Y_PRED = regr.predict(X)

        prediccion11 = regr.predict([[mayorDia+1]])
        prediccion21 = regr.predict([[mayorDia+365]])

        r21 = r2_score(Y,Y_PRED)        
        rmse1 = np.sqrt(mean_squared_error(Y,Y_PRED))         

        axs[0].scatter(X,Y,color="black")
        axs[0].plot(X,Y_PRED,color="blue")
        axs[0].set_ylim(menorInf1,mayorInf1) 

        #Realizar prediccion En pais 2
        Y_PRED2 = regr2.predict(X)

        prediccion12 = regr2.predict([[mayorDia+1]])
        prediccion22 = regr2.predict([[mayorDia+365]])

        r22 = r2_score(Y2,Y_PRED2)        
        rmse2 = np.sqrt(mean_squared_error(Y2,Y_PRED2))         

        axs[1].scatter(X,Y2,color="black")
        axs[1].plot(X,Y_PRED2,color="blue")
        axs[1].set_ylim(menorInf2,mayorInf2) 

        
        #Generar imagen y retornarla                                             
        flike = io.BytesIO()
        plt.savefig(flike)
        b64 = base64.b64encode(flike.getvalue()).decode()
        #plt.clf()
        plt.cla()

        #Retornar un arreglo que contenga la descripcion y el grafico
        arrReturn =[any]*2
        arrReturn[0] = b64

        #Generar una descripcion
        descripcion = ""
        descripcion += " Los datos fueron obtenidos mediante una funcion lineal brindada por sklearn\n"
        descripcion += " Esta funcion presento los siguientes resultados para el pais:"+self.nombrePais+ "\n"
        descripcion += " RMSE : " + str(rmse1) + "\n"
        descripcion += " R2 : " + str(r21) + "\n"

        descripcion += " Esta funcion presento los siguientes resultados para el pais:"+self.nombrePais2+ "\n"
        descripcion += " RMSE : " + str(rmse2) + "\n"
        descripcion += " R2 : " + str(r22) + "\n"

        descripcion += " Para aclarar el primer grafico es que del pais : "+ self.nombrePais + ", y el segundo grafico corresponde al pais: " + self.nombrePais2
        descripcion += " una vez aclarado esto se puede dar una descripcion acerca de cada uno de ellos"
        descripcion += " El modelo que presento mediante el entrenamiento segun los datos brindados del pais: " + self.nombrePais+" es el siguiente: \n"
        descripcion += " Y = " + str(regr.coef_[0][0]) + "X+" + str(regr.intercept_[0]) + "\n"
        descripcion += " Ademas de predecir hacia un año que la vacunacion seria de: " + prediccion21 +"\n"
        descripcion += " Y el modelo que presento mediante el entrenamiento segun los datos brindados del pais: " + self.nombrePais2+" es el siguiente: \n"
        descripcion += " Y = " + str(regr.coef_[0][0]) + "X+" + str(regr.intercept_[0]) + "\n"
        descripcion += " Ademas de predecir hacia un año que la vacunacion seria de: " + prediccion22 +"\n"

        descripcion += " Entonces podemos concluir que: \n"
        if prediccion21 > prediccion12:
            descripcion += " El pais: "+self.nombrePais + "tendra una mejor vacunacion en un año que " + self.nombrePais2
        elif prediccion12 > prediccion21:
            descripcion += " El pais: "+self.nombrePais2 + "tendra una mejor vacunacion en un año que " + self.nombrePais
        else:
            descripcion += " El pais: "+self.nombrePais2 + "tendra la misma vacunacion que " + self.nombrePais


        

        arrReturn[1] = descripcion         

        return arrReturn

#Porcentaje de hombres infectados por covid-19 en un País desde el primer caso activo
class Analisis11():
    nombrePais = ''
    campoPaises = ''
    campodia = ''
    camponum = ''
    archivoEn = any
    genero = ''
    campoGenero = ''


    def __init__(self,nombrePais,campoPaises,campodia,camponum,archivoEn,genero,campoGenero):
        self.nombrePais = nombrePais
        self.campoPaises = campoPaises
        self.campodia = campodia
        self.camponum = camponum
        self.archivoEn = archivoEn
        self.genero = genero
        self.campoGenero = campoGenero

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

        #Diferenciar por genero
        paisGen = np.asarray(dfPais[self.campoGenero].str.contains(self.genero))  

        #Obtener todos los datos que son del genero dado
        dfGen =  dfPais[paisGen]          
        
        #Crear un array del largo de los dias y que represente las fechas en su valor

        lbl_enc = preprocessing.LabelEncoder()
        diasLimpios = lbl_enc.fit_transform(dfGen[self.campodia])


        X = np.array(diasLimpios).reshape(-1,1)
        Y = dfGen[self.camponum]

        #Obtener el mayor dia y el menor
        menorDia = np.amin(X)
        mayorDia = np.amax(X)
        #Obtener el mayor numero de infectados y el menor
        menorInf = np.amin(Y) 
        mayorInf = np.amax(Y) 

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

        #Preparar grafos
        fig, axs = plt.subplots(2, 2)
        #Prediccion 1 dia despues

        x_new_min = menorDia
        x_new_max = mayorDia + 1

        X_NEW = np.arange(x_new_max).reshape(-1,1)  

        X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)  
        Y_NEW = model.predict(X_NEW_TRANSF)  

        axs[0,0].scatter(X,Y) 

        axs[0,0].plot(X_NEW, Y_NEW, color='coral', linewidth=3)  

        axs[0,0].grid()  
        axs[0,0].set_xlim(x_new_min,x_new_max)  
        axs[0,0].set_ylim(menorInf,mayorInf)  

        axs[0,0].set_title('Tendencia de infeccion actual', fontsize=10)
        axs[0,0].set_xlabel('Dia')
        axs[0,0].set_ylabel('Infectados ') 

        prediccion1 = Y_NEW[-1]

        #Prediccion a 1 mes
        x_new_min = menorDia
        x_new_max = mayorDia + 30

        X_NEW = np.arange(x_new_max).reshape(-1,1)  

        X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)  
        Y_NEW = model.predict(X_NEW_TRANSF)  

        prediccion2 = Y_NEW[-1]

        axs[0,1].scatter(X,Y) 

        axs[0,1].plot(X_NEW, Y_NEW, color='coral', linewidth=3)  

        axs[0,1].grid()  
        axs[0,1].set_xlim(x_new_min,x_new_max)  
        axs[0,1].set_ylim(menorInf,prediccion2)  

        axs[0,1].set_title('Tendencia de infeccion a 1 mes', fontsize=10)
        axs[0,1].set_xlabel('Dia')
        axs[0,1].set_ylabel('Infectados ') 

        #Prediccion a 6 meses
        x_new_min = menorDia
        x_new_max = mayorDia + 180

        X_NEW = np.arange(x_new_max).reshape(-1,1)  

        X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)  
        Y_NEW = model.predict(X_NEW_TRANSF) 

        prediccion3 = Y_NEW[-1]

        axs[1,0].scatter(X,Y) 

        axs[1,0].plot(X_NEW, Y_NEW, color='coral', linewidth=3)  

        axs[1,0].grid()  
        axs[1,0].set_xlim(x_new_min,x_new_max)  
        axs[1,0].set_ylim(menorInf,prediccion3)  

        axs[1,0].set_title('\nTendencia de infeccion a 6 meses', fontsize=10)
        axs[1,0].set_xlabel('Dia')
        axs[1,0].set_ylabel('Infectados ') 



        #Prediccion a 1 anio
        x_new_min = menorDia
        x_new_max = mayorDia + 365

        X_NEW = np.arange(x_new_max).reshape(-1,1)  

        X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)  
        Y_NEW = model.predict(X_NEW_TRANSF)  

        prediccion4 = Y_NEW[-1]

        axs[1,1].scatter(X,Y) 

        axs[1,1].plot(X_NEW, Y_NEW, color='coral', linewidth=3)  

        axs[1,1].grid()  
        axs[1,1].set_xlim(x_new_min,x_new_max)  
        axs[1,1].set_ylim(menorInf,prediccion4)  

        axs[1,1].set_title('\nTendencia de infeccion 1 Anio', fontsize=10)
        axs[1,1].set_xlabel('Dia')
        axs[1,1].set_ylabel('Infectados ') 


        
        #Generar imagen y retornarla                                             
        flike = io.BytesIO()
        plt.savefig(flike)
        b64 = base64.b64encode(flike.getvalue()).decode()
        #plt.clf()
        plt.cla()

        #Retornar un arreglo que contenga la descripcion y el grafico
        arrReturn =[any]*2
        arrReturn[0] = b64

        #Generar una descripcion
        descripcion = ""
        descripcion += " Los datos fueron obtenidos mediante una funcion polinomial de tercer grado brindada por sklearn\n"
        descripcion += " Esta funcion presento los siguientes resultados:\n"
        descripcion += " RMSE : " + str(rmse) + "\n"
        descripcion += " R2 : " + str(r2) + "\n"

        descripcion += "\nLa tendencia de infeccion en el genero "+self.genero+" en el pais: "+ self.nombrePais + ", se realiza mediante varias perspectivas, la primera es al dia siguiente"
        descripcion += "donde se obtiene una prediccion de "+str(prediccion1) + " infectados, la segunda se observa hacia un futuro cercano, un mes para ser exactos"
        descripcion += "donde se obtiene una prediccion de "+str(prediccion2) + " infectados, la tercera se observa igual hacia seis meses adelante"
        descripcion += "donde se obtiene una prediccion de "+str(prediccion3) + " infectados, y la ultima se realiza hacia un año adelante"
        descripcion += "donde se obtiene una prediccion de "+str(prediccion4) + " infectados, entonces podemos "
        if prediccion1 > prediccion4:
            descripcion += "concluir que al cabo de un año obtendremos menos infectados que en el mes cercano, por lo que se puede decir que tendera a bajar el numero de infectados en un año"            
        else:
            descripcion += "concluir que al cabo de un año obtendremos mas infectados que en el mes cercano, por lo que se puede decir que tendera a subir el numero de infectados en un año"    

        arrReturn[1] = descripcion         

        return arrReturn

#Ánalisis Comparativo entres 2 o más paises o continentes.
class Analisis12():
    nombrePais = ''
    nombrePais2 = ''
    campoPaises = ''
    campodia = ''
    camponum = ''
    archivoEn = any    


    def __init__(self,nombrePais,campoPaises,campodia,camponum,archivoEn,nombrePais2):
        self.nombrePais = nombrePais
        self.nombrePais2 = nombrePais2
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
        
        #Diferenciar los datos de los paises
        pais = np.asarray(df[self.campoPaises].str.contains(self.nombrePais))  
        pais2 =np.asarray(df[self.campoPaises].str.contains(self.nombrePais2))  

        #Obtener todos los datos que son del pais
        dfPais = df[pais]
        dfPais2 = df[pais2]
        
        #Crear un array del largo de los dias y que represente las fechas en su valor

        lbl_enc = preprocessing.LabelEncoder()
        diasLimpios = lbl_enc.fit_transform(dfPais[self.campodia])        

        X = np.array(diasLimpios).reshape(-1,1)
        Y = dfPais[self.camponum]
        Y2 = dfPais2[self.camponum]

        #Obtener el mayor dia y el menor
        menorDia = np.amin(X)
        mayorDia = np.amax(X)
        #Obtener el mayor numero de vacunas y el menor
        menorInf1 = np.amin(Y) 
        mayorInf1 = np.amax(Y) 

        menorInf2 = np.amin(Y2) 
        mayorInf2 = np.amax(Y2) 

        #Definimos el modelo en este caso es lineal ya que es el mas comun en el analisis de 2 datos bastante dispersos

        regr = LinearRegression()
        regr2 = LinearRegression()

        regr.fit(X,Y)
        regr2.fit(X,Y2)

        #Preparamos las figuras
        fig, axs = plt.subplots(2)


        #Realizar prediccion En pais 1
        Y_PRED = regr.predict(X)

        prediccion11 = regr.predict([[mayorDia+1]])
        prediccion21 = regr.predict([[mayorDia+365]])

        r21 = r2_score(Y,Y_PRED)        
        rmse1 = np.sqrt(mean_squared_error(Y,Y_PRED))         

        axs[0].scatter(X,Y,color="black")
        axs[0].plot(X,Y_PRED,color="blue")
        axs[0].set_ylim(menorInf1,mayorInf1) 

        #Realizar prediccion En pais 2
        Y_PRED2 = regr2.predict(X)

        prediccion12 = regr2.predict([[mayorDia+1]])
        prediccion22 = regr2.predict([[mayorDia+365]])

        r22 = r2_score(Y2,Y_PRED2)        
        rmse2 = np.sqrt(mean_squared_error(Y2,Y_PRED2))         

        axs[1].scatter(X,Y2,color="black")
        axs[1].plot(X,Y_PRED2,color="blue")
        axs[1].set_ylim(menorInf2,mayorInf2) 

        
        #Generar imagen y retornarla                                             
        flike = io.BytesIO()
        plt.savefig(flike)
        b64 = base64.b64encode(flike.getvalue()).decode()
        #plt.clf()
        plt.cla()

        #Retornar un arreglo que contenga la descripcion y el grafico
        arrReturn =[any]*2
        arrReturn[0] = b64

        #Generar una descripcion
        descripcion = ""
        descripcion += " Los datos fueron obtenidos mediante una funcion lineal brindada por sklearn\n"
        descripcion += " Esta funcion presento los siguientes resultados para el pais:"+self.nombrePais+ "\n"
        descripcion += " RMSE : " + str(rmse1) + "\n"
        descripcion += " R2 : " + str(r21) + "\n"

        descripcion += " Esta funcion presento los siguientes resultados para el pais:"+self.nombrePais2+ "\n"
        descripcion += " RMSE : " + str(rmse2) + "\n"
        descripcion += " R2 : " + str(r22) + "\n"

        descripcion += " Para aclarar el primer grafico es que del pais : "+ self.nombrePais + ", y el segundo grafico corresponde al pais: " + self.nombrePais2
        descripcion += " una vez aclarado esto se puede dar una descripcion acerca de cada uno de ellos\n"
        descripcion += " El modelo que presento mediante el entrenamiento segun los datos brindados del pais: " + self.nombrePais+" es el siguiente: \n"
        descripcion += " Y = " + str(regr.coef_[0][0]) + "X+" + str(regr.intercept_[0]) + "\n"
        descripcion += " Ademas de predecir hacia un año que los valores serian de: " + prediccion21 +"\n"
        descripcion += " Y el modelo que presento mediante el entrenamiento segun los datos brindados del pais: " + self.nombrePais2+" es el siguiente: \n"
        descripcion += " Y = " + str(regr.coef_[0][0]) + "X+" + str(regr.intercept_[0]) + "\n"
        descripcion += " Ademas de predecir hacia un año que los valores serian de: " + prediccion22 +"\n"

        descripcion += " Entonces podemos concluir que: \n"
        if prediccion21 > prediccion12:
            descripcion += " El pais: "+self.nombrePais + "tendra una mejores valores en un año que " + self.nombrePais2
        elif prediccion12 > prediccion21:
            descripcion += " El pais: "+self.nombrePais2 + "tendra una mejores valores en un año que " + self.nombrePais
        else:
            descripcion += " El pais: "+self.nombrePais2 + "tendra lo mismo que " + self.nombrePais


        

        arrReturn[1] = descripcion         

        return arrReturn

#Muertes promedio por casos confirmados y edad de covid 19 en un País.
class Analisis13():
    nombrePais = ''
    campoPaises = ''
    campodia = ''
    camponum = ''
    archivoEn = any    
    campoEdad = ''


    def __init__(self,nombrePais,campoPaises,campodia,camponum,archivoEn,campoEdad):
        self.nombrePais = nombrePais
        self.campoPaises = campoPaises
        self.campodia = campodia
        self.camponum = camponum
        self.archivoEn = archivoEn        
        self.campoEdad = campoEdad

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
        
        ed1 = np.asarray((dfPais[self.campoEdad]<25) & (dfPais[self.campoEdad]>0))
        ed2 = np.asarray((dfPais[self.campoEdad]<50) & (dfPais[self.campoEdad]>=25))
        ed3 = np.asarray((dfPais[self.campoEdad]<75) & (dfPais[self.campoEdad]>=50))
        ed4 = np.asarray(((dfPais[self.campoEdad]>=75)))

        #Cantidad de infectados
        df1 = dfPais[ed1]
        df2 = dfPais[ed2]
        df3 = dfPais[ed3]
        df4 = dfPais[ed4]

        cant1 = len(df1)
        cant2 = len(df2)
        cant3 = len(df3)
        cant4 = len(df4)
        cantTotal = len(dfPais)

        #Obtenemos porcentajes
        por1 = round((cant1/cantTotal)*100,2)
        por2 = round((cant2/cantTotal)*100,2)
        por3 = round((cant3/cantTotal)*100,2)
        por4 = round((cant4/cantTotal)*100,2)

        print(por1)
        print(por2)
        print(por3)
        print(por4)


        ## Declaramos valores para el eje x
        eje_x = ['De 0 a 25', 'De 25 a 50', 'De 50 a 75', 'mayores a 75']
        
        ## Declaramos valores para el eje y
        eje_y = [cant1,cant2,cant3,cant4]
        
        ## Creamos Gráfica
        plt.bar(eje_x, eje_y)
        
        ## Legenda en el eje y
        plt.ylabel('Cantidad Infectados')
        
        ## Legenda en el eje x
        plt.xlabel('Edad')
        
        ## Título de Gráfica
        plt.title('Infectados por edad')


        
        #Generar imagen y retornarla                                             
        flike = io.BytesIO()
        plt.savefig(flike)
        b64 = base64.b64encode(flike.getvalue()).decode()
        #plt.clf()
        plt.cla()

        #Retornar un arreglo que contenga la descripcion y el grafico
        arrReturn =[any]*2
        arrReturn[0] = b64

        #Generar una descripcion
        descripcion = ""
        descripcion += " Los datos fueron obtenidos mediante una funcion polinomial de tercer grado brindada por sklearn\n"
        descripcion += " Esta funcion presento los siguientes resultados:\n"
        descripcion += " Porcentaje de personas contagiadas de 0 a 25 años:" + str(por1) + ".\n"
        descripcion += " Porcentaje de personas contagiadas de 25 a 50 años:" + str(por2) + ".\n"
        descripcion += " Porcentaje de personas contagiadas de 50 a 75 años:" + str(por3) + ".\n"
        descripcion += " Porcentaje de personas contagiadas mayores a 75 años:" + str(por4) + ".\n"
        descripcion += " Por lo que concluimos que: "

        if por1>por2 and por1>por3 and por1>por4:
            descripcion += " Las personas de 0 a 25 años estan siendo las mas contagiadas.\n"
        elif por2>por1 and por2>por3 and por2>por4:
            descripcion += " Las personas de 25 a 50 años estan siendo las mas contagiadas.\n"
        elif por3>por2 and por3>por1 and por3>por4:
            descripcion += " Las personas de 50 a 75 años estan siendo las mas contagiadas.\n"
        elif por4>por2 and por4>por3 and por4>por1:
            descripcion += " Las personas mayores a 75 años estan siendo las mas contagiadas.\n"
        

        arrReturn[1] = descripcion         

        return arrReturn



#Tendencia de casos confirmados de Coronavirus en un departamento de un País.
class Analisis15():
    nombrePais = ''
    campoPaises = ''
    campodia = ''
    camponum = ''
    archivoEn = any
    nombreDep = ''
    campoDep = ''


    def __init__(self,nombrePais,campoPaises,campodia,camponum,archivoEn,nombreDep,campoDep):
        self.nombrePais = nombrePais
        self.campoPaises = campoPaises
        self.campodia = campodia
        self.camponum = camponum
        self.archivoEn = archivoEn
        self.nombreDep = nombreDep
        self.campoDep = campoDep

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

        #Obtener todos los datos por departamento
        dep = np.asarray(dfPais[self.campoDep].str.contains(self.nombreDep))             

        dfDep = dfPais[dep]
        
        #Crear un array del largo de los dias y que represente las fechas en su valor

        lbl_enc = preprocessing.LabelEncoder()
        diasLimpios = lbl_enc.fit_transform(dfDep[self.campodia])


        X = np.array(diasLimpios).reshape(-1,1)
        Y = dfDep[self.camponum]

        #Obtener el mayor dia y el menor
        menorDia = np.amin(X)
        mayorDia = np.amax(X)
        #Obtener el mayor numero de infectados y el menor
        menorInf = np.amin(Y) 
        mayorInf = np.amax(Y) 

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

        #Preparar grafos
        fig, axs = plt.subplots(2, 2)
        #Prediccion 1 dia despues

        x_new_min = menorDia
        x_new_max = mayorDia + 1

        X_NEW = np.arange(x_new_max).reshape(-1,1)  

        X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)  
        Y_NEW = model.predict(X_NEW_TRANSF)  

        axs[0,0].scatter(X,Y) 

        axs[0,0].plot(X_NEW, Y_NEW, color='coral', linewidth=3)  

        axs[0,0].grid()  
        axs[0,0].set_xlim(x_new_min,x_new_max)  
        axs[0,0].set_ylim(menorInf,mayorInf)  

        axs[0,0].set_title('Tendencia de infeccion actual', fontsize=10)
        axs[0,0].set_xlabel('Dia')
        axs[0,0].set_ylabel('Infectados ') 

        prediccion1 = Y_NEW[-1]

        #Prediccion a 1 mes
        x_new_min = menorDia
        x_new_max = mayorDia + 30

        X_NEW = np.arange(x_new_max).reshape(-1,1)  

        X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)  
        Y_NEW = model.predict(X_NEW_TRANSF)  

        prediccion2 = Y_NEW[-1]

        axs[0,1].scatter(X,Y) 

        axs[0,1].plot(X_NEW, Y_NEW, color='coral', linewidth=3)  

        axs[0,1].grid()  
        axs[0,1].set_xlim(x_new_min,x_new_max)  
        axs[0,1].set_ylim(menorInf,prediccion2)  

        axs[0,1].set_title('Tendencia de infeccion a 1 mes', fontsize=10)
        axs[0,1].set_xlabel('Dia')
        axs[0,1].set_ylabel('Infectados ') 

        #Prediccion a 6 meses
        x_new_min = menorDia
        x_new_max = mayorDia + 180

        X_NEW = np.arange(x_new_max).reshape(-1,1)  

        X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)  
        Y_NEW = model.predict(X_NEW_TRANSF) 

        prediccion3 = Y_NEW[-1]

        axs[1,0].scatter(X,Y) 

        axs[1,0].plot(X_NEW, Y_NEW, color='coral', linewidth=3)  

        axs[1,0].grid()  
        axs[1,0].set_xlim(x_new_min,x_new_max)  
        axs[1,0].set_ylim(menorInf,prediccion3)  

        axs[1,0].set_title('\nTendencia de infeccion a 6 meses', fontsize=10)
        axs[1,0].set_xlabel('Dia')
        axs[1,0].set_ylabel('Infectados ') 



        #Prediccion a 1 anio
        x_new_min = menorDia
        x_new_max = mayorDia + 365

        X_NEW = np.arange(x_new_max).reshape(-1,1)  

        X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)  
        Y_NEW = model.predict(X_NEW_TRANSF)  

        prediccion4 = Y_NEW[-1]

        axs[1,1].scatter(X,Y) 

        axs[1,1].plot(X_NEW, Y_NEW, color='coral', linewidth=3)  

        axs[1,1].grid()  
        axs[1,1].set_xlim(x_new_min,x_new_max)  
        axs[1,1].set_ylim(menorInf,prediccion4)  

        axs[1,1].set_title('\nTendencia de infeccion 1 Anio', fontsize=10)
        axs[1,1].set_xlabel('Dia')
        axs[1,1].set_ylabel('Infectados ') 


        
        #Generar imagen y retornarla                                             
        flike = io.BytesIO()
        plt.savefig(flike)
        b64 = base64.b64encode(flike.getvalue()).decode()
        #plt.clf()
        plt.cla()

        #Retornar un arreglo que contenga la descripcion y el grafico
        arrReturn =[any]*2
        arrReturn[0] = b64

        #Generar una descripcion
        descripcion = ""
        descripcion += " Los datos fueron obtenidos mediante una funcion polinomial de tercer grado brindada por sklearn\n"
        descripcion += " Esta funcion presento los siguientes resultados:\n"
        descripcion += " RMSE : " + str(rmse) + "\n"
        descripcion += " R2 : " + str(r2) + "\n"

        descripcion += "\nLa tendencia de infeccion en el pais: "+ self.nombrePais + "en el departamento "+self.nombreDep+", se realiza mediante varias perspectivas, la primera es al dia siguiente"
        descripcion += "donde se obtiene una prediccion de "+str(prediccion1) + " infectados, la segunda se observa hacia un futuro cercano, un mes para ser exactos"
        descripcion += "donde se obtiene una prediccion de "+str(prediccion2) + " infectados, la tercera se observa igual hacia seis meses adelante"
        descripcion += "donde se obtiene una prediccion de "+str(prediccion3) + " infectados, y la ultima se realiza hacia un año adelante"
        descripcion += "donde se obtiene una prediccion de "+str(prediccion4) + " infectados, entonces podemos "
        if prediccion1 > prediccion4:
            descripcion += "concluir que al cabo de un año obtendremos menos infectados que en el mes cercano, por lo que se puede decir que tendera a bajar el numero de infectados en un año"            
        else:
            descripcion += "concluir que al cabo de un año obtendremos mas infectados que en el mes cercano, por lo que se puede decir que tendera a subir el numero de infectados en un año"    

        arrReturn[1] = descripcion         

        return arrReturn

#Porcentaje de muertes frente al total de casos en un país, región o continente.
class Analisis16():
    nombrePais = ''
    campoPaises = ''
    campodia = ''
    camponumInf = ''
    camponumMuer = ''
    archivoEn = any

    def __init__(self,nombrePais,campoPaises,campodia,camponumInf,camponumMuer,archivoEn):
        self.nombrePais = nombrePais
        self.campoPaises = campoPaises
        self.campodia = campodia
        self.camponumInf = camponumInf
        self.camponumMuer = camponumMuer
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

        #Obtener totol de casos
        infectados = dfPais[self.camponumInf]

        totalInfectados = 0
        for infec in infectados:
            totalInfectados += infec

        #Obtener total de muertes
        muertes = dfPais[self.camponumInf]

        totalMuertes = 0
        for muerte in muertes:
            totalMuertes += muerte

        #Sacar un porcentaje
        porcentaje = (totalInfectados / totalMuertes) * 100

        #Describir
        descripcion = ""
        descripcion += "Para calcular el porcentaje de muertes frente a casos de covid en :" + self.nombrePais
        descripcion += " primero se obtuvieron los datos acerca del total de infectados y el total de muertes de la region.\n"
        descripcion += " El total de muertes es: "+ str(totalMuertes) + "\n"
        descripcion += " El total de casos infecados es: "+ str(totalInfectados) + "\n"
        descripcion += " Por lo que podemos inferir que el porcentaje de muertes frente a casos de covid en "+ self.nombrePais+" es de \n"
        descripcion += str(porcentaje)+"%\n"        

#Tasa de comportamiento de casos activos en relación al número de muertes en un continente.
class Analisis17():
    nombrePais = ''
    campoPaises = ''
    campodia = ''
    camponum = ''
    camponum2 = ''
    archivoEn = any    


    def __init__(self,nombreContinente,campoPaises,campodia,camponum,camponum2,archivoEn):
        self.nombrePais = nombreContinente
        self.campoPaises = campoPaises
        self.campodia = campodia
        self.camponum = camponum
        self.camponum2 = camponum2
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
        Y2 = dfPais[self.camponum2]
        #Obtener el mayor dia y el menor
        menorDia = np.amin(X)
        mayorDia = np.amax(X)
        #Obtener el mayor numero de vacunas y el menor
        menorInf1 = np.amin(Y) 
        mayorInf1 = np.amax(Y) 
        menorInf2 = np.amin(Y2) 
        mayorInf2 = np.amax(Y2) 
        #Definimos el modelo en este caso es lineal ya que es el mas comun en el analisis de 2 datos bastante dispersos
        regr = LinearRegression()
        regr2 = LinearRegression()
        regr.fit(X,Y)
        regr2.fit(X,Y2)
        #Preparamos las figuras
        fig, axs = plt.subplots(2)
        #Realizar prediccion Infectados
        Y_PRED = regr.predict(X)
        prediccion1Inf = regr2.predict([[mayorDia+1]])



        r21 = r2_score(Y,Y_PRED)        
        rmse1 = np.sqrt(mean_squared_error(Y,Y_PRED))         
        axs[0].scatter(X,Y,color="black")
        axs[0].plot(X,Y_PRED,color="blue")
        axs[0].set_ylim(menorInf1,mayorInf1) 
        axs[0].set_title("Infectados") 

        #Realizar prediccion Muertes
        Y_PRED2 = regr2.predict(X)

        prediccion1Muer = regr2.predict([[mayorDia+1]])



        #((total cases - total cases previous day) / total cases previous day) *100
        tasacomportamiento = round((prediccion1Inf/prediccion1Muer)*100 ,2)
        

        r22 = r2_score(Y2,Y_PRED2)        
        rmse2 = np.sqrt(mean_squared_error(Y2,Y_PRED2))         
        axs[1].scatter(X,Y2,color="black")
        axs[1].plot(X,Y_PRED2,color="blue")
        axs[1].set_ylim(menorInf2,mayorInf2) 
        axs[1].set_title("Muertes") 

        #Generar imagen y retornarla                                             
        flike = io.BytesIO()
        plt.savefig(flike)
        b64 = base64.b64encode(flike.getvalue()).decode()
        #plt.clf()
        plt.cla()

        #Retornar un arreglo que contenga la descripcion y el grafico
        arrReturn =[any]*2
        arrReturn[0] = b64

        #Generar una descripcion
        descripcion = ""
        descripcion += " Los datos fueron obtenidos mediante una funcion lineal brindada por sklearn \n"
        descripcion += " Las funciones que se presentan son las predicciones de numero de casos activos y prediccion de numero de muertes\n"                   
        descripcion += " Estas funciones presentaron los siguientes resultados:\n"                   
        descripcion += " Tasa de comportamiento de un dia predecido despues del ultimo: " + str(tasacomportamiento)+"\n"                   
        descripcion += " Esta tasa se calcula mediante la siguiente formula:\n"                   
        descripcion += " Casos/Muertes\n"                   
        descripcion += " Lo que nos indica que a un numero mayor menos muertes habran y a un numero menor\n"                   
        descripcion += " significa que terminaran en muerte mas casos activos\n"                   
        

        arrReturn[1] = descripcion         

        return arrReturn

#Predicción de muertes en el último día del primer año de infecciones en un país.
class Analisis19():
    nombrePais = ''
    campoPaises = ''
    campodia = ''
    camponum = ''
    archivoEn = any    


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
        #Prediccion a 1 anio desde el primer dia
        cantidadRestante = 365 - mayorDia

        x_new_min = menorDia
        x_new_max = 365

        X_NEW = np.arange(x_new_max).reshape(-1,1)  

        X_NEW_TRANSF = polynomial_features.fit_transform(X_NEW)  
        Y_NEW = model.predict(X_NEW_TRANSF)  

        prediccion1 = Y_NEW[-1]

        plt.scatter(X,Y) 

        plt.plot(X_NEW, Y_NEW, color='coral', linewidth=3)  

        plt.grid()  
        plt.set_xlim(x_new_min,x_new_max)  
        plt.set_ylim(menorInf,prediccion1)  

        plt.set_title('\nTendencia de infeccion 1 Anio', fontsize=10)
        plt.set_xlabel('Dia')
        plt.set_ylabel('Infectados ') 


        
        #Generar imagen y retornarla                                             
        flike = io.BytesIO()
        plt.savefig(flike)
        b64 = base64.b64encode(flike.getvalue()).decode()
        #plt.clf()
        plt.cla()

        #Retornar un arreglo que contenga la descripcion y el grafico
        arrReturn =[any]*2
        arrReturn[0] = b64

        #Generar una descripcion
        descripcion = ""
        descripcion += " Los datos fueron obtenidos mediante una funcion polinomial de tercer grado brindada por sklearn\n"
        descripcion += " Esta funcion presento los siguientes resultados:\n"
        descripcion += " RMSE : " + str(rmse) + "\n"
        descripcion += " R2 : " + str(r2) + "\n"
        #se realiza hacia un año adelante
        descripcion += "\nLa tendencia de infeccion en el pais: "+ self.nombrePais + ", se realiza hacia futuro completando un año"
        descripcion += " donde se obtiene una prediccion de "+str(prediccion1) + " casos"

        arrReturn[1] = descripcion         

        return arrReturn

#Tasa de crecimiento de casos de COVID-19 en relación con nuevos casos diarios y tasa de muerte por COVID-19
class Analisis20():
    nombrePais = ''
    campoPaises = ''
    campodia = ''
    camponum = ''
    camponum2 = ''
    archivoEn = any    


    def __init__(self,nombrePais,campoPaises,campodia,camponum,camponum2,archivoEn):
        self.nombrePais = nombrePais
        self.campoPaises = campoPaises
        self.campodia = campodia
        self.camponum = camponum
        self.camponum2 = camponum2
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

        #Crear un array del largo de los dias y que represente las fechas en su valor

        lbl_enc = preprocessing.LabelEncoder()
        diasLimpios = lbl_enc.fit_transform(df[self.campodia])        
        X = np.array(diasLimpios).reshape(-1,1)
        Y = df[self.camponum]
        Y2 = df[self.camponum2]
        #Obtener el mayor dia y el menor
        menorDia = np.amin(X)
        mayorDia = np.amax(X)
        #Obtener el mayor numero de vacunas y el menor
        menorInf1 = np.amin(Y) 
        mayorInf1 = np.amax(Y) 
        menorInf2 = np.amin(Y2) 
        mayorInf2 = np.amax(Y2) 
        #Definimos el modelo en este caso es lineal ya que es el mas comun en el analisis de 2 datos bastante dispersos
        regr = LinearRegression()
        regr2 = LinearRegression()
        regr.fit(X,Y)
        regr2.fit(X,Y2)
        #Preparamos las figuras
        fig, axs = plt.subplots(2)
        #Realizar prediccion Infectados
        Y_PRED = regr.predict(X)
        prediccion1Inf = regr2.predict([[mayorDia]])

        prediccion2Inf = regr2.predict([[mayorDia+1]])

        prediccion1Inf = int(prediccion1Inf)
        prediccion2Inf = int(prediccion2Inf)


        #((total cases - total cases previous day) / total cases previous day) *100
        tasaInf = round(((prediccion2Inf - prediccion1Inf)/prediccion1Inf)*100 ,2)
        print("Tasa de Infectados: "+ str(tasaInf) + "%")


        r21 = r2_score(Y,Y_PRED)        
        rmse1 = np.sqrt(mean_squared_error(Y,Y_PRED))         
        axs[0].scatter(X,Y,color="black")
        axs[0].plot(X,Y_PRED,color="blue")
        axs[0].set_ylim(menorInf1,mayorInf1) 
        axs[0].set_title("Infectados") 

        #Realizar prediccion Muertes
        Y_PRED2 = regr2.predict(X)

        prediccion1Muer = regr2.predict([[mayorDia]])

        prediccion2Muer = regr2.predict([[mayorDia+1]])

        prediccion1Muer = int(prediccion1Muer)
        prediccion2Muer = int(prediccion2Muer)


        #((total cases - total cases previous day) / total cases previous day) *100
        tasaMuer = round(((prediccion2Muer - prediccion1Muer)/prediccion1Muer)*100 ,2)

        print("Tasa de muerte: "+ str(tasaMuer) + "%")

        r22 = r2_score(Y2,Y_PRED2)        
        rmse2 = np.sqrt(mean_squared_error(Y2,Y_PRED2))         
        axs[1].scatter(X,Y2,color="black")
        axs[1].plot(X,Y_PRED2,color="blue")
        axs[1].set_ylim(menorInf2,mayorInf2) 
        axs[1].set_title("Muertes") 

        #Generar imagen y retornarla                                             
        flike = io.BytesIO()
        plt.savefig(flike)
        b64 = base64.b64encode(flike.getvalue()).decode()
        #plt.clf()
        plt.cla()

        #Retornar un arreglo que contenga la descripcion y el grafico
        arrReturn =[any]*2
        arrReturn[0] = b64

        #Generar una descripcion
        descripcion = ""
        descripcion += " Los datos fueron obtenidos mediante una funcion lineal brindada por sklearn \n"
        descripcion += " Las funciones que se presentan son las predicciones de numero de infectados y numero de muertes\n"                   
        descripcion += " Estas funciones presentaron los siguientes resultados:\n"                   
        descripcion += " Tasa de crecimiento de Muertes:"+str(tasaInf) + "%\n"     
        descripcion += " Tasa de crecimiento de casos: "+ str(tasaMuer) + "%\n"    
        descripcion += " Para calcular esta tasa se utilizo la siguiente formula: \n"    
        descripcion += " (TotalCasos-TotalCasos dia anterior)/TotalCasos dia anterior\n"            
        descripcion += " Lo que resta ahi es multiplicarlo por 100 para obtener un porcentaje.\n"            

        arrReturn[1] = descripcion         

        return arrReturn

#Predicciones de casos y muertes en todo el mundo - Neural Network MLPRegressor
class Analisis21():
    nombrePais = ''
    campoPaises = ''
    campodia = ''
    camponum = ''
    camponum2 = ''
    archivoEn = any    


    def __init__(self,nombrePais,campoPaises,campodia,camponum,camponum2,archivoEn):
        self.nombrePais = nombrePais
        self.campoPaises = campoPaises
        self.campodia = campodia
        self.camponum = camponum
        self.camponum2 = camponum2
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

        #Crear un array del largo de los dias y que represente las fechas en su valor

        lbl_enc = preprocessing.LabelEncoder()
        diasLimpios = lbl_enc.fit_transform(df[self.campodia])


        X = np.array(diasLimpios).reshape(-1,1)        
        Y1 = df[self.camponum]
        Y2 = df[self.camponum2]

        #Obtener el mayor dia y el menor
        menorDia = np.amin(X)
        mayorDia = np.amax(X)
        #Entrenar el modelo

        mlp = MLPRegressor(hidden_layer_sizes=(100,100,100),solver='lbfgs',activation='relu',max_iter=70000).fit(X,Y1)

        mlp2 = MLPRegressor( hidden_layer_sizes=(100,100,100),solver='lbfgs',activation='relu',max_iter=70000).fit(X,Y2)

        training_cases = mlp.predict(X)

        training_deaths = mlp2.predict(X)

        pred1Casos = mlp.predict(mayorDia+1)
        pred2Casos = mlp.predict(mayorDia+30)
        pred3Casos = mlp.predict(mayorDia+365)
        
        pred1Muertes = mlp2.predict(mayorDia+1)
        pred2Muertes = mlp2.predict(mayorDia+30)
        pred3Muertes = mlp2.predict(mayorDia+365)

        fig, axs = plt.subplots(2)

        axs[0].set_title('Infectados')
        axs[0].set_ylabel('Casos')
        axs[0].set_xlabel('Dia')
        axs[0].plot(X, Y1)
        axs[0].plot(X, training_cases)

        axs[1].set_title('Muertes')
        axs[1].set_ylabel('Muertos')
        axs[1].set_xlabel('Dia')
        axs[1].plot(X, Y2)
        axs[1].plot(X, training_deaths)

        #Generar imagen y retornarla                                             
        flike = io.BytesIO()
        plt.savefig(flike)
        b64 = base64.b64encode(flike.getvalue()).decode()
        #plt.clf()
        plt.cla()

        #Retornar un arreglo que contenga la descripcion y el grafico
        arrReturn =[any]*2
        arrReturn[0] = b64

        #Generar una descripcion
        descripcion = ""
        descripcion += " Los datos fueron obtenidos mediante una red neural brindada por sklearn llamada MLBPRegressor\n"
        descripcion += " Esta funcion presento los siguientes resultados:\n"                
        descripcion += " Prediccion para 1 dia despues Casos:"+str(pred1Casos)+"\n"
        descripcion += " Prediccion para 1 dia despues Muertes:"+str(pred1Muertes)+"\n"
        descripcion += " Prediccion para 30 dias despues Casos:"+str(pred2Casos)+"\n"           
        descripcion += " Prediccion para 30 dias despues Muertes:"+str(pred2Muertes)+"\n" 
        descripcion += " Prediccion para 365 dias despues del ultimo Casos:"+str(pred3Casos)+"\n"                
        descripcion += " Prediccion para 365 dias despues del ultimo Muertes:"+str(pred3Muertes)+"\n"                       

        arrReturn[1] = descripcion         

        return arrReturn

#Tasa de mortalidad por coronavirus (COVID-19) en un país.
class Analisis22(): 
    nombrePais = ''
    campoPaises = ''    
    campodia = ''
    camponumInf = ''
    camponumMuer = ''
    archivoEn = any    


    def __init__(self,nombrePais,campoPaises,campodia,camponumInf,camponumMuer,archivoEn):
        self.nombrePais = nombrePais
        self.campoPaises = campoPaises
        self.campodia = campodia
        self.camponumInf = camponumInf
        self.camponumMuer = camponumMuer
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
        Y1 = dfPais[self.camponumInf]
        Y2 = dfPais[self.camponumMuer]

        #Obtener el mayor dia y el menor
        menorDia = np.amin(X)
        mayorDia = np.amax(X)
        #Obtener el mayor numero de infectados y el menor
        menorInf = np.amin(Y1) 
        mayorInf = np.amax(Y1) 

        #Obtener el mayor numero de muertes y el menor
        menorMuer = np.amin(Y2) 
        mayorMuer = np.amax(Y2) 

        #Definimos el modelo en este caso es lineal ya que es el mas comun en el analisis de 2 datos bastante dispersos

        #Se define la variable para la acumulacion 1 anio despues del primer dia
        predict = [365]
        predict = np.array(predict).reshape(-1,1) 

        fig, axs = plt.subplots(2)

        regr = LinearRegression()

        regr.fit(X,Y1)        

        
        Y_PRED = regr.predict(X)

        prediccion1Inf = regr.predict([[mayorDia+1]])
        prediccion2Inf = regr.predict([[365]])
        prediccionAcumInf = regr.predict(predict)

        r21 = r2_score(Y1,Y_PRED)        
        rmse1 = np.sqrt(mean_squared_error(Y1,Y_PRED))         

        axs[0].scatter(X,Y1,color="black")
        axs[0].plot(X,Y_PRED,color="blue")

        axs[0].ylim(menorInf,mayorInf) 

        #Prediccion de muertes
        regr2 = LinearRegression()

        regr2.fit(X,Y2)        

        Y_PRED2 = regr2.predict(X)

        prediccion1Muer = regr2.predict([[mayorDia+1]])
        prediccion2Muer = regr2.predict([[365]])
        prediccionAcumMuer = regr2.predict(predict)        
        

        r22 = r2_score(Y2,Y_PRED)        
        rmse2 = np.sqrt(mean_squared_error(Y2,Y_PRED))         

        axs[1].scatter(X,Y2,color="black")
        axs[1].plot(X,Y_PRED2,color="blue")

        axs[1].ylim(menorMuer,mayorMuer) 

        #TAsa de mortalidad
        tasa = prediccionAcumMuer/prediccionAcumInf
        
        #Generar imagen y retornarla                                             
        flike = io.BytesIO()
        plt.savefig(flike)
        b64 = base64.b64encode(flike.getvalue()).decode()
        #plt.clf()
        plt.cla()

        #Retornar un arreglo que contenga la descripcion y el grafico
        arrReturn =[any]*2
        arrReturn[0] = b64

        #Generar una descripcion
        descripcion = ""
        descripcion += " Los datos fueron obtenidos mediante una funcion lineal brindada por sklearn\n"
        descripcion += " La primera funcion presento los siguientes resultados para los casos de infectados:\n"
        descripcion += " RMSE : " + str(rmse1) + "\n"
        descripcion += " R2 : " + str(r21) + "\n"

        descripcion += " El modelo que presento mediante el entrenamiento segun los datos brindados es el siguiente: \n"
        descripcion += " Y = " + str(regr.coef_[0][0]) + "X+" + str(regr.intercept_[0]) + "\n"

        descripcion += " La segunda funcion presento los siguientes resultados para los casos de infectados:\n"
        descripcion += " RMSE : " + str(rmse2) + "\n"
        descripcion += " R2 : " + str(r22) + "\n"

        descripcion += " El modelo que presento mediante el entrenamiento segun los datos brindados es el siguiente: \n"
        descripcion += " Y = " + str(regr2.coef_[0][0]) + "X+" + str(regr2.intercept_[0]) + "\n"

        descripcion += "\nEste indice de mortaliadad en el pais: "+ self.nombrePais
        descripcion += ", se realiza mediante varias perspectivas,la de los casos y la de los muertos, ademas de verlos a traves del tiempo,"
        descripcion += " para los casos se predicen algunos datos, el primero es justo al dia siguiente del ultimo ingresado"
        descripcion += " donde se obtiene una prediccion de "+str(prediccion1Inf) + " infectados, el segundo se observa hacia futuro ,año despues del primero ingresado para ser exactos"                
        descripcion += " donde se obtiene una prediccion de "+str(prediccion2Inf) + " infectados"
        descripcion += " asi como tambien se obtiene una prediccion de los casos acumulados de "+str(prediccionAcumInf) + " infectados."
        descripcion += " Y de la misma manera se realiza para los muertos, el primero justo al dia siguiente del ultimo"
        descripcion += " donde se obtiene una prediccion de "+str(prediccion1Muer) + " muertos, el segundo se observa hacia futuro ,año despues del primero ingresado para ser exactos"                
        descripcion += " donde se obtiene una prediccion de "+str(prediccion2Muer) + " muertos"
        descripcion += " asi como tambien se obtiene una prediccion de los muertos acumulados de "+str(prediccionAcumMuer) + " .\n"
        descripcion += " Analizando el modelo que se presento se infiere que: \n"
        if str(regr2.coef_[0][0]) < 0:
            descripcion += " Las muertes en el pais estaran disminuyendo\n"
        else:
            descripcion += " Las muertes en el pais estaran aumentando\n"   

        descripcion += " Asi que de esta manera podemos explicar que la tasa de mortalidad en: " + self.nombrePais + " se calcula de la siguiente manera: \n"
        descripcion += " Muertos / Casos\n"
        descripcion +=  str(prediccionAcumMuer)+"/"+str(prediccionAcumInf)+" = "+str(tasa*100)+"%\n"

        arrReturn[1] = descripcion         

        return arrReturn

#Comparación entre el número de casos detectados y el número de pruebas de un país.
class Analisis24():
    nombrePais = ''
    campoPaises = ''    
    campodia = ''
    camponumInf = ''
    camponumMuer = ''
    archivoEn = any    


    def __init__(self,nombrePais,campoPaises,campodia,camponumInf,camponumMuer,archivoEn):
        self.nombrePais = nombrePais
        self.campoPaises = campoPaises
        self.campodia = campodia
        self.camponumInf = camponumInf
        self.camponumMuer = camponumMuer
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
        Y1 = dfPais[self.camponumInf]
        Y2 = dfPais[self.camponumMuer] #Pruebas realizadas

        #Obtener el mayor dia y el menor
        menorDia = np.amin(X)
        mayorDia = np.amax(X)
        #Obtener el mayor numero de infectados y el menor
        menorInf = np.amin(Y1) 
        mayorInf = np.amax(Y1) 

        #Obtener el mayor numero de muertes y el menor
        menorMuer = np.amin(Y2) 
        mayorMuer = np.amax(Y2) 

        #Definimos el modelo en este caso es lineal ya que es el mas comun en el analisis de 2 datos bastante dispersos

        #Se define la variable para la acumulacion 1 anio despues del primer dia
        predict = [365]
        predict = np.array(predict).reshape(-1,1) 

        fig, axs = plt.subplots(2)

        regr = LinearRegression()

        regr.fit(X,Y1)        

        
        Y_PRED = regr.predict(X)

        prediccion1Inf = regr.predict([[mayorDia+1]])
        prediccion2Inf = regr.predict([[365]])
        prediccionAcumInf = regr.predict(predict)

        r21 = r2_score(Y1,Y_PRED)        
        rmse1 = np.sqrt(mean_squared_error(Y1,Y_PRED))         

        axs[0].scatter(X,Y1,color="black")
        axs[0].plot(X,Y_PRED,color="blue")

        axs[0].ylim(menorInf,mayorInf) 

        #Prediccion de muertes
        regr2 = LinearRegression()

        regr2.fit(X,Y2)        

        Y_PRED2 = regr2.predict(X)

        prediccion1Muer = regr2.predict([[mayorDia+1]])
        prediccion2Muer = regr2.predict([[365]])
        prediccionAcumMuer = regr2.predict(predict)        
        

        r22 = r2_score(Y2,Y_PRED)        
        rmse2 = np.sqrt(mean_squared_error(Y2,Y_PRED))         

        axs[1].scatter(X,Y2,color="black")
        axs[1].plot(X,Y_PRED2,color="blue")

        axs[1].ylim(menorMuer,mayorMuer) 

        #Tasa de Pruebas
        tasa = round((prediccionAcumMuer/prediccionAcumInf)*100,2)
        
        #Generar imagen y retornarla                                             
        flike = io.BytesIO()
        plt.savefig(flike)
        b64 = base64.b64encode(flike.getvalue()).decode()
        #plt.clf()
        plt.cla()

        #Retornar un arreglo que contenga la descripcion y el grafico
        arrReturn =[any]*2
        arrReturn[0] = b64

        #Generar una descripcion
        descripcion = ""
        descripcion += " Los datos fueron obtenidos mediante una funcion lineal brindada por sklearn\n"
        descripcion += " El modelo que presento mediante el entrenamiento segun los datos brindados es el siguiente: \n"
        descripcion += " Y = " + str(regr.coef_[0][0]) + "X+" + str(regr.intercept_[0]) + "\n"

        descripcion += " Y el segundo modelo que presento mediante el entrenamiento segun los datos brindados es el siguiente: \n"
        descripcion += " Y = " + str(regr2.coef_[0][0]) + "X+" + str(regr2.intercept_[0]) + "\n"

        descripcion += "\nLas graficas representan una prediccion de como se ven los casos frente a las pruebas que se estan realizando"
        descripcion += " para aclarar la primer grafica representan los infectados y la segunda las pruebas realizadas, asi que se realiza un estudio "
        descripcion += " perspectivas a traves del tiempo,"
        descripcion += " para los casos se predicen algunos datos, el primero es justo al dia siguiente del ultimo ingresado"
        descripcion += " donde se obtiene una prediccion de "+str(prediccion1Inf) + " infectados, el segundo se observa hacia futuro ,año despues del primero ingresado para ser exactos"                
        descripcion += " donde se obtiene una prediccion de "+str(prediccion2Inf) + " infectados"
        descripcion += " asi como tambien se obtiene una prediccion de los casos acumulados de "+str(prediccionAcumInf) + " infectados."
        descripcion += " Y de la misma manera se realiza para las pruebas, el primero justo al dia siguiente del ultimo"
        descripcion += " donde se obtiene una prediccion de "+str(prediccion1Muer) + " muertos, el segundo se observa hacia futuro ,año despues del primero ingresado para ser exactos"                
        descripcion += " donde se obtiene una prediccion de "+str(prediccion2Muer) + " muertos"
        descripcion += " asi como tambien se obtiene una prediccion de los pruebas acumulados de "+str(prediccionAcumMuer) + " .\n"                 

        descripcion += " Asi que de esta manera podemos explicar que la tasa de mortalidad en: " + self.nombrePais + " se calcula de la siguiente manera: \n"
        descripcion += " Pruebas / Casos\n"
        descripcion +=  str(prediccionAcumMuer)+"/"+str(prediccionAcumInf)+" = "+str(tasa)+"%\n"

        arrReturn[1] = descripcion         

        return arrReturn

#Tasa de mortalidad por coronavirus (COVID-19) en un país.
class Analisis25():             
    campodia = ''
    camponumInf = ''    
    archivoEn = any    


    def __init__(self,campodia,camponumInf,archivoEn):                
        self.campodia = campodia
        self.camponumInf = camponumInf        
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

        #Crear un array del largo de los dias y que represente las fechas en su valor

        lbl_enc = preprocessing.LabelEncoder()
        diasLimpios = lbl_enc.fit_transform(df[self.campodia])

        
        X = np.array(diasLimpios).reshape(-1,1)
        Y1 = df[self.camponumInf]
        

        #Obtener el mayor dia y el menor
        menorDia = np.amin(X)
        mayorDia = np.amax(X)
        #Obtener el mayor numero de infectados y el menor
        menorInf = np.amin(Y1) 
        mayorInf = np.amax(Y1) 
        

        #Definimos el modelo en este caso es lineal ya que es el mas comun en el analisis de 2 datos bastante dispersos        

        regr = LinearRegression()

        regr.fit(X,Y1)        

        
        Y_PRED = regr.predict(X)

        prediccion1Inf = regr.predict([[mayorDia+1]])
        prediccion2Inf = regr.predict([[mayorDia+365]])        

        r21 = r2_score(Y1,Y_PRED)        
        rmse1 = np.sqrt(mean_squared_error(Y1,Y_PRED))         

        plt.scatter(X,Y1,color="black")
        plt.plot(X,Y_PRED,color="blue")

        plt.ylim(menorInf,mayorInf) 
        
        #Generar imagen y retornarla                                             
        flike = io.BytesIO()
        plt.savefig(flike)
        b64 = base64.b64encode(flike.getvalue()).decode()
        #plt.clf()
        plt.cla()

        #Retornar un arreglo que contenga la descripcion y el grafico
        arrReturn =[any]*2
        arrReturn[0] = b64

        #Generar una descripcion
        descripcion = ""
        descripcion += " Los datos fueron obtenidos mediante una funcion lineal brindada por sklearn\n"
        descripcion += " La primera funcion presento los siguientes resultados para los casos de infectados:\n"
        descripcion += " RMSE : " + str(rmse1) + "\n"
        descripcion += " R2 : " + str(r21) + "\n"

        descripcion += " El modelo que presento mediante el entrenamiento segun los datos brindados es el siguiente: \n"
        descripcion += " Y = " + str(regr.coef_[0][0]) + "X+" + str(regr.intercept_[0]) + "\n"

        descripcion += " Se realizan dos predicciones la primera es al dia siguiente al ultimo, que da "+prediccion1Inf + "casos y la otra"
        descripcion += " es a 365 dias despues del ultimo que da "+prediccion2Inf + "casos.\n"



        if str(regr.coef_[0][0]) < 0:
            descripcion += " Los casos de infecciones por coronavirus estaran disminuyendo\n"
        else:
            descripcion += " Las casos de infecciones por coronavirus estaran aumentando\n"           

        arrReturn[1] = descripcion

        return arrReturn    

