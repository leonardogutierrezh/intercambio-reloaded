#encoding:utf-8
from django.forms import ModelForm
from django.db import models
from django import forms
from django.contrib.auth.models import User
from estudiante.models import *
from postulante.models import *
from administrador.models import *
from countries.models import *
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import CheckboxSelectMultiple
import magic
from datetime import *

class Postulante_Edit_Form(forms.Form):
    email = forms.EmailField()
    username = forms.CharField(max_length=50, label="Nombre de usuario")
    cambiarContra = forms.BooleanField(label="Cambiar contrasena", widget=forms.CheckboxInput(attrs={'onClick':'cambiarContrasena()'}), required=False)
    contrasena1 = forms.CharField(widget=forms.PasswordInput(attrs={'disabled':'disabled'}),label="Contrasena", required=False)
    contrasena2 = forms.CharField(widget=forms.PasswordInput(attrs={'disabled':'disabled'}),label="Contrasena de nuevo", required=False)
    carrera = forms.ModelChoiceField(queryset=CarreraUsb.objects.all())

class Postulante_RecomendarEstudiante(forms.Form):
    indiceVerificado = forms.BooleanField(label='Índice verificado:')
    indice = forms.CharField(max_length=10, label= 'Índice')
    comentarios = forms.CharField(widget=forms.Textarea)

class nuevaMateriaForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    codigo = forms.CharField(max_length=100, label='Código')
    creditos = forms.IntegerField(label='Créditos')

class Postulante_RecomendarCasoEstudiante(forms.Form):
    comentarios = forms.CharField(widget=forms.Textarea)

