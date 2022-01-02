from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('descargar',views.descargar,name='descargar')
]