
import pandas as pd
from matplotlib import pyplot as plt
from sklearn import preprocessing
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
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
        descripcion += " donde se obtiene una prediccion de "+str(prediccion1) + " infectados, la segunda se observa hacia futuro, para ser exactos un año adelante"

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
        axs[0].ylim(menorInf1,mayorInf1) 

        #Realizar prediccion En pais 2
        Y_PRED = regr.predict(X)

        prediccion12 = regr.predict([[mayorDia+1]])
        prediccion22 = regr.predict([[mayorDia+365]])

        r22 = r2_score(Y,Y_PRED)        
        rmse2 = np.sqrt(mean_squared_error(Y,Y_PRED))         

        axs[1].scatter(X,Y,color="black")
        axs[1].plot(X,Y_PRED,color="blue")
        axs[1].ylim(menorInf2,mayorInf2) 

        
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

#Tendencia de la infección por Covid-19 en un País.
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