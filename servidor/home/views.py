import base64
from django.shortcuts import render

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import AnalizarForm, ParametrizarForm

from .analizadores.analisis1 import Analisis1, Analisis2,Analisis3,Analisis4,Analisis5,Analisis6,Analisis7,Analisis8,Analisis9,Analisis10
from .analizadores.analisis1 import Analisis11, Analisis12,Analisis13,Analisis15,Analisis16,Analisis17,Analisis19,Analisis20
from .analizadores.analisis1 import Analisis21, Analisis22,Analisis24,Analisis25


# Imports de generacion de PDF
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from datetime import datetime


TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR,"templates"),'
)


def index(request):
    contexto = any
    descripcion = any
    print("Se tiene que analizar")
    if request.method == 'POST' and request.FILES['archivoEn']:
        print('Analizando Post')

        form = AnalizarForm(request.POST, request.FILES)

        if form.is_valid():
            numAnalisis = form.cleaned_data['tipoAnalisis']

            if numAnalisis == '1':
                nombrePais = form.cleaned_data['nombrePais']
                campoPaises = form.cleaned_data['campoPaises']
                campodia = form.cleaned_data['campodia']
                camponum = form.cleaned_data['camponum']
                archivoEn = request.FILES['archivoEn']
                analisis1 = Analisis1(nombrePais=nombrePais, campoPaises=campoPaises,
                                      campodia=campodia, camponum=camponum, archivoEn=archivoEn)

                contextoTotal = analisis1.analizar()
                contexto = contextoTotal[0]
                descripcion = contextoTotal[1]
                request.session['imagen'] = contextoTotal[0]
                request.session['descripcion'] = descripcion
                request.session['nombreAnalisis'] = 'Tendencia de la infección por Covid-19 en un País.'

            elif numAnalisis == '2':
                nombrePais = form.cleaned_data['nombrePais']
                campoPaises = form.cleaned_data['campoPaises']
                campodia = form.cleaned_data['campodia']
                camponum = form.cleaned_data['camponum']
                archivoEn = request.FILES['archivoEn']
                analisis1 = Analisis2(nombrePais=nombrePais, campoPaises=campoPaises,
                                      campodia=campodia, camponum=camponum, archivoEn=archivoEn)

                contextoTotal = analisis1.analizar()
                contexto = contextoTotal[0]
                descripcion = contextoTotal[1]
                request.session['imagen'] = contextoTotal[0]
                request.session['descripcion'] = descripcion
                request.session['nombreAnalisis'] = 'Predicción de Infertados en un País.'

            # Analisis No.3
            elif numAnalisis == '3':
                nombrePais = form.cleaned_data['nombrePais']
                campoPaises = form.cleaned_data['campoPaises']
                campodia = form.cleaned_data['campodia']
                camponum = form.cleaned_data['camponum']
                diasProyeccion = form.cleaned_data['diasProyeccion']
                camponumIsopado = form.cleaned_data['camponumIsopado']
                archivoEn = request.FILES['archivoEn']
                analisis1 = Analisis3(nombrePais=nombrePais, campoPaises=campoPaises,
                                      campodia=campodia, camponum=camponum, archivoEn=archivoEn, camponumIsopado=camponumIsopado, cantidadDias=diasProyeccion)
                descripcion = analisis1.analizar()
                #request.session['imagen'] = contextoTotal[0]
                request.session['descripcion'] = descripcion
                request.session['nombreAnalisis'] = 'Predicción de Infertados en un País.'

            elif numAnalisis == '4':                
                nombrePais = form.cleaned_data['nombrePais']
                campoPaises = form.cleaned_data['campoPaises']
                campodia = form.cleaned_data['campodia']
                camponum = form.cleaned_data['camponum']
                campoDepartamento = form.cleaned_data['diasProyeccion']
                nombreDep = form.cleaned_data['camponumIsopado']
                archivoEn = request.FILES['archivoEn']
                                
                analisis1 = Analisis4(nombrePais=nombrePais, campoPaises=campoPaises,campodia=campodia, camponum=camponum, archivoEn=archivoEn,campoDepartamento=campoDepartamento,nombreDep=nombreDep)

                contextoTotal = analisis1.analizar()
                contexto = contextoTotal[0]
                descripcion = contextoTotal[1]
                request.session['imagen'] = contextoTotal[0]
                request.session['descripcion'] = descripcion
                request.session['nombreAnalisis'] = 'Predicción de Infertados en un País.'
            elif numAnalisis == '5':                
                nombrePais = form.cleaned_data['nombrePais']
                campoPaises = form.cleaned_data['campoPaises']
                campodia = form.cleaned_data['campodia']
                camponum = form.cleaned_data['camponum']
                archivoEn = request.FILES['archivoEn']
                                
                analisis1 = Analisis5(nombrePais=nombrePais, campoPaises=campoPaises,campodia=campodia, camponum=camponum, archivoEn=archivoEn)

                contextoTotal = analisis1.analizar()
                contexto = contextoTotal[0]
                descripcion = contextoTotal[1]
                request.session['imagen'] = contextoTotal[0]
                request.session['descripcion'] = descripcion
                request.session['nombreAnalisis'] = 'Predicción de Infertados en un País.'
            elif numAnalisis == '6':                
                nombrePais = form.cleaned_data['nombrePais']
                campoPaises = form.cleaned_data['campoPaises']
                campodia = form.cleaned_data['campodia']
                camponum = form.cleaned_data['camponum']
                archivoEn = request.FILES['archivoEn']
                                
                analisis1 = Analisis6(nombrePais=nombrePais, campoPaises=campoPaises,campodia=campodia, camponum=camponum, archivoEn=archivoEn)

                contextoTotal = analisis1.analizar()
                contexto = contextoTotal[0]
                descripcion = contextoTotal[1]
                request.session['imagen'] = contextoTotal[0]
                request.session['descripcion'] = descripcion
                request.session['nombreAnalisis'] = 'Predicción de Infertados en un País.'
            elif numAnalisis == '7':                
                nombrePais = form.cleaned_data['nombrePais']
                campoPaises = form.cleaned_data['campoPaises']
                campodia = form.cleaned_data['campodia']
                camponum = form.cleaned_data['camponum']
                archivoEn = request.FILES['archivoEn']
                                
                analisis1 = Analisis7(nombrePais=nombrePais, campoPaises=campoPaises,campodia=campodia, camponum=camponum, archivoEn=archivoEn)

                contextoTotal = analisis1.analizar()
                contexto = contextoTotal[0]
                descripcion = contextoTotal[1]
                request.session['imagen'] = contextoTotal[0]
                request.session['descripcion'] = descripcion
                request.session['nombreAnalisis'] = 'Tendencia del número de infectados por día de un País.'
            elif numAnalisis == '8':                
                nombrePais = form.cleaned_data['nombrePais']
                campoPaises = form.cleaned_data['campoPaises']
                campodia = form.cleaned_data['campodia']
                camponum = form.cleaned_data['camponum']
                archivoEn = request.FILES['archivoEn']
                                
                analisis1 = Analisis8(nombrePais=nombrePais, campoPaises=campoPaises,campodia=campodia, camponum=camponum, archivoEn=archivoEn)

                contextoTotal = analisis1.analizar()
                contexto = contextoTotal[0]
                descripcion = contextoTotal[1]
                request.session['imagen'] = contextoTotal[0]
                request.session['descripcion'] = descripcion
                request.session['nombreAnalisis'] = 'Predicción de casos de un país para un año.'
            elif numAnalisis == '9':                
                nombrePais = form.cleaned_data['nombrePais']
                campoPaises = form.cleaned_data['campoPaises']
                campodia = form.cleaned_data['campodia']
                camponum = form.cleaned_data['camponum']
                archivoEn = request.FILES['archivoEn']
                                
                analisis1 = Analisis9(nombrePais=nombrePais, campoPaises=campoPaises,campodia=campodia, camponum=camponum, archivoEn=archivoEn)

                contextoTotal = analisis1.analizar()
                contexto = contextoTotal[0]
                descripcion = contextoTotal[1]
                request.session['imagen'] = contextoTotal[0]
                request.session['descripcion'] = descripcion
                request.session['nombreAnalisis'] = 'Tendencia de la vacunación en un País.'
            elif numAnalisis == '10':          
                      
                nombrePais = form.cleaned_data['nombrePais']
                nombrePais2 = form.cleaned_data['diasProyeccion']
                campoPaises = form.cleaned_data['campoPaises']
                campodia = form.cleaned_data['campodia']
                camponum = form.cleaned_data['camponum']
                archivoEn = request.FILES['archivoEn']
                                
                analisis1 = Analisis10(nombrePais=nombrePais, campoPaises=campoPaises,campodia=campodia, camponum=camponum, archivoEn=archivoEn,nombrePais2=nombrePais2)

                contextoTotal = analisis1.analizar()
                contexto = contextoTotal[0]
                descripcion = contextoTotal[1]
                request.session['imagen'] = contextoTotal[0]
                request.session['descripcion'] = descripcion
                request.session['nombreAnalisis'] = 'Tendencia de la vacunación en un País.'
            elif numAnalisis == '11':          
                      
                nombrePais = form.cleaned_data['nombrePais']                
                campoPaises = form.cleaned_data['campoPaises']
                campodia = form.cleaned_data['campodia']
                camponum = form.cleaned_data['camponum']
                genero = form.cleaned_data['camponumIsopado']
                campoGenero = form.cleaned_data['diasProyeccion']
                archivoEn = request.FILES['archivoEn']
                                
                analisis1 = Analisis11(nombrePais=nombrePais, campoPaises=campoPaises,campodia=campodia, camponum=camponum, archivoEn=archivoEn,genero=genero,campoGenero=campoGenero)

                contextoTotal = analisis1.analizar()
                contexto = contextoTotal[0]
                descripcion = contextoTotal[1]
                request.session['imagen'] = contextoTotal[0]
                request.session['descripcion'] = descripcion
                request.session['nombreAnalisis'] = 'Tendencia de la vacunación en un País.'
            elif numAnalisis == '12':          
                      
                nombrePais = form.cleaned_data['nombrePais']
                nombrePais2 = form.cleaned_data['diasProyeccion']
                campoPaises = form.cleaned_data['campoPaises']
                campodia = form.cleaned_data['campodia']
                camponum = form.cleaned_data['camponum']
                archivoEn = request.FILES['archivoEn']
                                
                analisis1 = Analisis12(nombrePais=nombrePais, campoPaises=campoPaises,campodia=campodia, camponum=camponum, archivoEn=archivoEn,nombrePais2=nombrePais2)

                contextoTotal = analisis1.analizar()
                contexto = contextoTotal[0]
                descripcion = contextoTotal[1]
                request.session['imagen'] = contextoTotal[0]
                request.session['descripcion'] = descripcion
                request.session['nombreAnalisis'] = 'Tendencia de la vacunación en un País.'
            elif numAnalisis == '13':          
                      
                nombrePais = form.cleaned_data['nombrePais']
                campoEdad = form.cleaned_data['diasProyeccion']
                campoPaises = form.cleaned_data['campoPaises']
                campodia = form.cleaned_data['campodia']
                camponum = form.cleaned_data['camponum']
                archivoEn = request.FILES['archivoEn']
                                
                analisis1 = Analisis13(nombrePais=nombrePais, campoPaises=campoPaises,campodia=campodia, camponum=camponum, archivoEn=archivoEn,campoEdad=campoEdad)

                contextoTotal = analisis1.analizar()
                contexto = contextoTotal[0]
                descripcion = contextoTotal[1]
                request.session['imagen'] = contextoTotal[0]
                request.session['descripcion'] = descripcion
                request.session['nombreAnalisis'] = 'Tendencia de la vacunación en un País.'
            elif numAnalisis == '15':          
                      
                nombrePais = form.cleaned_data['nombrePais']
                campoDep = form.cleaned_data['diasProyeccion']
                campoPaises = form.cleaned_data['campoPaises']
                campodia = form.cleaned_data['campodia']
                camponum = form.cleaned_data['camponum']
                nombreDep = form.cleaned_data['camponumIsopado']                
                archivoEn = request.FILES['archivoEn']
                                
                analisis1 = Analisis15(nombrePais=nombrePais, campoPaises=campoPaises,campodia=campodia, camponum=camponum, archivoEn=archivoEn,nombreDep=nombreDep,campoDep=campoDep)

                contextoTotal = analisis1.analizar()
                contexto = contextoTotal[0]
                descripcion = contextoTotal[1]
                request.session['imagen'] = contextoTotal[0]
                request.session['descripcion'] = descripcion
                request.session['nombreAnalisis'] = 'Tendencia de la vacunación en un País.'
            elif numAnalisis == '16':
                      
                nombrePais = form.cleaned_data['nombrePais']
                camponum2 = form.cleaned_data['diasProyeccion']
                campoPaises = form.cleaned_data['campoPaises']
                campodia = form.cleaned_data['campodia']
                camponum = form.cleaned_data['camponum']
                archivoEn = request.FILES['archivoEn']
                                
                analisis1 = Analisis16(nombrePais=nombrePais, campoPaises=campoPaises,campodia=campodia, archivoEn=archivoEn,camponumInf=camponum,camponumMuer=camponum2)

                contextoTotal = analisis1.analizar()
                contexto = contextoTotal[0]
                descripcion = contextoTotal[1]
                request.session['imagen'] = contextoTotal[0]
                request.session['descripcion'] = descripcion
                request.session['nombreAnalisis'] = 'Tendencia de la vacunación en un País.'
            elif numAnalisis == '17':
                      
                nombrePais = form.cleaned_data['nombrePais']
                camponum2 = form.cleaned_data['diasProyeccion']
                campoPaises = form.cleaned_data['campoPaises']
                campodia = form.cleaned_data['campodia']
                camponum = form.cleaned_data['camponum']
                archivoEn = request.FILES['archivoEn']
                                
                analisis1 = Analisis17(nombreContinente=nombrePais, campoPaises=campoPaises,campodia=campodia, archivoEn=archivoEn,camponum=camponum,camponum2=camponum2)

                contextoTotal = analisis1.analizar()
                contexto = contextoTotal[0]
                descripcion = contextoTotal[1]
                request.session['imagen'] = contextoTotal[0]
                request.session['descripcion'] = descripcion
                request.session['nombreAnalisis'] = 'Tendencia de la vacunación en un País.'
            elif numAnalisis == '19':                
                nombrePais = form.cleaned_data['nombrePais']
                campoPaises = form.cleaned_data['campoPaises']
                campodia = form.cleaned_data['campodia']
                camponum = form.cleaned_data['camponum']
                archivoEn = request.FILES['archivoEn']
                                
                analisis1 = Analisis19(nombrePais=nombrePais, campoPaises=campoPaises,campodia=campodia, camponum=camponum, archivoEn=archivoEn)

                contextoTotal = analisis1.analizar()
                contexto = contextoTotal[0]
                descripcion = contextoTotal[1]
                request.session['imagen'] = contextoTotal[0]
                request.session['descripcion'] = descripcion
                request.session['nombreAnalisis'] = 'Predicción de muertes en el último día del primer año de infecciones en un país.'
            elif numAnalisis == '20':                                
                campodia = form.cleaned_data['campodia']
                camponum = form.cleaned_data['camponum']
                camponum2 = form.cleaned_data['nombrePais']
                archivoEn = request.FILES['archivoEn']
                                
                analisis1 = Analisis20(campodia=campodia, archivoEn=archivoEn,camponum=camponum, camponum2=camponum2)

                contextoTotal = analisis1.analizar()
                contexto = contextoTotal[0]
                descripcion = contextoTotal[1]
                request.session['imagen'] = contextoTotal[0]
                request.session['descripcion'] = descripcion
                request.session['nombreAnalisis'] = 'Predicción de muertes en el último día del primer año de infecciones en un país.'
            elif numAnalisis == '21':                                
                campodia = form.cleaned_data['campodia']
                camponum = form.cleaned_data['camponum']
                camponum2 = form.cleaned_data['nombrePais']
                archivoEn = request.FILES['archivoEn']
                                
                analisis1 = Analisis21(campodia=campodia, archivoEn=archivoEn,camponum=camponum, camponum2=camponum2)

                contextoTotal = analisis1.analizar()
                contexto = contextoTotal[0]
                descripcion = contextoTotal[1]
                request.session['imagen'] = contextoTotal[0]
                request.session['descripcion'] = descripcion
                request.session['nombreAnalisis'] = 'Predicción de muertes en el último día del primer año de infecciones en un país.'
            elif numAnalisis == '22':
                      
                nombrePais = form.cleaned_data['nombrePais']
                camponum2 = form.cleaned_data['diasProyeccion']
                campoPaises = form.cleaned_data['campoPaises']
                campodia = form.cleaned_data['campodia']
                camponum = form.cleaned_data['camponum']
                archivoEn = request.FILES['archivoEn']
                                
                analisis1 = Analisis22(nombrePais=nombrePais, campoPaises=campoPaises,campodia=campodia, archivoEn=archivoEn,camponumInf=camponum,camponumMuer=camponum2)

                contextoTotal = analisis1.analizar()
                contexto = contextoTotal[0]
                descripcion = contextoTotal[1]
                request.session['imagen'] = contextoTotal[0]
                request.session['descripcion'] = descripcion
                request.session['nombreAnalisis'] = 'Tendencia de la vacunación en un País.'
            elif numAnalisis == '24':
                      
                nombrePais = form.cleaned_data['nombrePais']
                camponum2 = form.cleaned_data['diasProyeccion']
                campoPaises = form.cleaned_data['campoPaises']
                campodia = form.cleaned_data['campodia']
                camponum = form.cleaned_data['camponum']
                archivoEn = request.FILES['archivoEn']
                                
                analisis1 = Analisis24(nombrePais=nombrePais, campoPaises=campoPaises,campodia=campodia, archivoEn=archivoEn,camponumInf=camponum,camponumMuer=camponum2)

                contextoTotal = analisis1.analizar()
                contexto = contextoTotal[0]
                descripcion = contextoTotal[1]
                request.session['imagen'] = contextoTotal[0]
                request.session['descripcion'] = descripcion
                request.session['nombreAnalisis'] = 'Tendencia de la vacunación en un País.'
            elif numAnalisis == '25':                                
                campodia = form.cleaned_data['campodia']
                camponum = form.cleaned_data['camponum']                
                archivoEn = request.FILES['archivoEn']
                                
                analisis1 = Analisis25(campodia=campodia, camponumInf=camponum,archivoEn=archivoEn)

                contextoTotal = analisis1.analizar()
                contexto = contextoTotal[0]
                descripcion = contextoTotal[1]
                request.session['imagen'] = contextoTotal[0]
                request.session['descripcion'] = descripcion
                request.session['nombreAnalisis'] = 'Predicción de muertes en el último día del primer año de infecciones en un país.'
        else:
            print('No es valido')

            # Retornar al mismo index
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AnalizarForm()

    # Retornar a index al terminar
    return render(request, "index.html", {'form': form, 'graph': contexto, 'descripcion': descripcion})


def descargar(request):

    # Obtencion de datos
    imagen = request.session['imagen']
    descripcion = request.session['descripcion']
    nombreAnalisis = request.session['nombreAnalisis']
    


    image_64_decode = base64.b64decode(imagen) 
    image_result = open('grafico.png', 'wb') # create a writable image and write the decoding result
    image_result.write(image_64_decode)
    image_result.close()

    #obtener fecha actual

    fecha = datetime.today().strftime('%d/%m/%Y')

    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)
    
    
    p.setLineWidth(.3)
    p.setFont('Helvetica', 12)
    p.drawString(30,750,'UNIVERSIDAD SAN CARLOS DE GUATEMALA')
    p.drawString(30,735,'ORGANIZACION DE LENGUAJES Y COMPILADORES 2')

    p.drawString(500,750,fecha)
    p.line(480,747,580,747)
    p.drawString(30,703,'TIPO DE ANALISIS:')
    p.line(160,700,580,700)
    p.drawString(160,703,nombreAnalisis)

    p.drawString(30,690,'DESCRIPCION:')

    descripcion1 = descripcion.split("\n")
    cont1 = 676
    for element in descripcion1:        
        if len(element) >= 96:
            #Segundo split
            descr2 = element.split()            
            descr3 = ''
            cont2 = 0
            for el2 in descr2:
                if cont2 >= 11:
                    p.drawString(30,cont1,descr3)
                    descr3 = ''
                    cont2 = 0
                    cont1 -= 14
                else:
                    descr3 += el2 + ' '
                    cont2 +=1
        else:
            p.drawString(30,cont1,element)
            cont1 -= 14
    p.drawString(30,cont1,'GRAFICO:')    

    p.drawImage('grafico.png',30,0,300,300)


    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='Analisis.pdf')

def seleccionar(request):
    valPar = 0
    if request.method == 'POST':
        form = ParametrizarForm(request.POST)

        if form.is_valid():            
            valPar = form.cleaned_data['inputGroupSelect01']


    return render(request, "index.html", {'valorParametro': valPar})