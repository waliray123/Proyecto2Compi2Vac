
from django import forms

class AnalizarForm(forms.Form):
    tipoAnalisis = forms.CharField(label='tipoAnalisis', max_length=100);    
    nombrePais = forms.CharField(label='nombrePais', max_length=100)    
    campoPaises = forms.CharField(label='campoPaises', max_length=100)    
    campodia = forms.CharField(label='campodia', max_length=100)
    camponum = forms.CharField(label='camponum', max_length=100)
    nombreContinente = forms.CharField(label='nombreContinente', max_length=100)
    archivoEn = forms.FileField(label='archivoEn')
    
        
        

    

