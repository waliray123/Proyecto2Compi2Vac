from django.shortcuts import render

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from reportlab.lib.utils import ImageReader
from .forms import AnalizarForm

from django.core.files.storage import FileSystemStorage
from .analizadores.analisis1 import Analisis1
from .analizadores.analisis1 import Analisis3

# Imports de generacion de PDF
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.templatetags.static import static
from .forms import DescargarForm


TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR,"templates"),'
)


def index(request):
    contexto = any
    descripcion = any
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
    grafico = any
    descripcion = any
    if request.method == 'POST':

        form = DescargarForm(request.POST)

        if form.is_valid():
            #grafico = form.cleaned_data['grafico']
            # print(grafico)
            descripcion = form.cleaned_data['descripcion']
            print(descripcion)

        print('Es un post')

    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='Analisis.pdf')
