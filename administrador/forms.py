from django.forms import ModelForm
from django import forms
from django.db import models
from administrador.models import *

class NuevoUsuarioForm(forms.Form):
    nombre_usuario = forms.CharField(label='Nombre de usuario')
    email = forms.EmailField()
    nombre = forms.CharField()