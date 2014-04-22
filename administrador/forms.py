from django.forms import ModelForm
from django import forms
from django.db import models
from administrador.models import *
from postulante.models import Universidad, Carrera, CarreraUsb

class NuevoUsuarioForm(forms.Form):
    nombre_usuario = forms.CharField(label='Nombre de usuario')
    email = forms.EmailField()
    nombre = forms.CharField()

class NuevaCoordinacionForm(forms.Form):
    nombre_usuarioCoordinacion = forms.CharField(label='Nombre de usuario')
    emailCoordinacion = forms.EmailField(label='Email')
    carreraCoordinacion = forms.ModelChoiceField(queryset= CarreraUsb.objects.all(), label="Carrera")

class NuevaUniversidadExtrangeraForm(forms.Form):
    nombre_usuarioExtranjera = forms.CharField(label='Nombre de usuario')
    emailExtranjera = forms.EmailField(label='Email')
    nombreExtranjera = forms.CharField(label='Nombre de la universidad')
    pais = forms.ModelChoiceField(queryset= Pais.objects.all())

class NuevoEstudianteForm(forms.Form):
    nombre_usuarioEstudiante = forms.CharField(label='Nombre de usuario')
    emailEstudiante = forms.EmailField(label='Email')
    nombreEstudiante = forms.CharField(label='Primer nombre')
    apellidoEstudiante = forms.CharField(label='Primer apellido')
    carnet = forms.CharField(label='Carnet')
    carreraEstudiante = forms.ModelChoiceField(queryset= CarreraUsb.objects.all(), label="Carrera")

class NuevoEstudianteExtranjeroForm(forms.Form):
    nombre_usuarioExtranjero = forms.CharField(label='Nombre de usuario')
    emailExtranjero = forms.EmailField(label='Email')
    nombreExtranjero = forms.CharField(label='Primer nombre')
    apellidoExtranjero = forms.CharField(label='Primer apellido')
    pasaporteExtranjero = forms.CharField(label='Pasaporte')

class EditarPerfilForm(forms.Form):
    nombre = forms.CharField(label='Nombre Completo')
    email = forms.EmailField()
    usuario = forms.CharField()

class CrearUniversidadForm(forms.ModelForm):
    class Meta:
        model = Universidad