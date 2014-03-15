from django.forms import ModelForm
from django import forms
from django.db import models
from administrador.models import *
from postulante.models import Universidad, Carrera

class NuevoUsuarioForm(forms.Form):
    nombre_usuario = forms.CharField(label='Nombre de usuario')
    email = forms.EmailField()
    nombre = forms.CharField()

class NuevaCoordinacionForm(forms.Form):
    nombre_usuarioCoordinacion = forms.CharField(label='Nombre de usuario')
    emailCoordinacion = forms.EmailField(label='Email')
    carreraCoordinacion = forms.ModelChoiceField(queryset= Carrera.objects.filter(universidad__nombre = 'Universidad Simon Bolivar'))

class NuevaUniversidadExtrangeraForm(forms.Form):
    nombre_usuarioExtranjera = forms.CharField(label='Nombre de usuario')
    emailExtranjera = forms.EmailField(label='Email')
    nombreExtranjera = forms.CharField(label='Nombre de la universidad')

class NuevoEstudianteForm(forms.Form):
    nombre_usuarioEstudiante = forms.CharField(label='Nombre de usuario')
    emailEstudiante = forms.EmailField(label='Email')
    nombreEstudiante = forms.CharField(label='Primer nombre')
    apellidoEstudiante = forms.CharField(label='Primer apellido')
    carreraEstudiante = forms.ModelChoiceField(queryset= Carrera.objects.filter(universidad__nombre = 'Universidad Simon Bolivar'))

class NuevoEstudianteExtranjeroForm(forms.Form):
    nombre_usuarioExtranjero = forms.CharField(label='Nombre de usuario')
    emailExtranjero = forms.EmailField(label='Pmail')
    nombreExtranjero = forms.CharField(label='Primer nombre')
    apellidoExtranjero = forms.CharField(label='Primer apellido')
    pasaporteExtranjero = forms.CharField(label='Pasaporte')