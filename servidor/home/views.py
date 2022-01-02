from django.shortcuts import render

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import AnalizarForm

from django.core.files.storage import FileSystemStorage
from .analizadores.analisis1 import Analisis1

TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR,"templates"),'
)


def index(request):
    contexto = any
    if request.method == 'POST' and request.FILES['archivoEn']:
        print('Analizando Post')

        form = AnalizarForm(request.POST, request.FILES)

        if form.is_valid():
            numAnalisis = form.cleaned_data['tipoAnalisis']

            if numAnalisis == '1':
                tipoAnalisis = form.cleaned_data['tipoAnalisis']
                nombrePais = form.cleaned_data['nombrePais']
                campoPaises = form.cleaned_data['campoPaises']
                campodia = form.cleaned_data['campodia']
                camponum = form.cleaned_data['camponum']
                archivoEn = request.FILES['archivoEn']                
                #filename = fs.save(archivoEn.name, archivoEn)
                #uploaded_file_url = fs.url(filename)
                # print(uploaded_file_url)

                analisis1 = Analisis1(nombrePais=nombrePais, campoPaises=campoPaises,
                                  campodia=campodia, camponum=camponum, archivoEn=archivoEn)
                
                
                contexto = analisis1.analizar()

            elif numAnalisis == '17':
                print('El analisis es 17')
        else:
            print('No es valido')

            # Retornar al mismo index
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AnalizarForm()

    # Retornar a index al terminar
    return render(request, "index.html", {'form': form,'graph':contexto})


def prueba(request):
    if request.method == 'POST':
        print('Analizando Post Prueba')

        form = AnalizarForm(request.POST)

        if form.is_valid():

            # Retornar al mismo index
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AnalizarForm()

    # Retornar a index al terminar
    return render(request, "index.html", {'form': form})
