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

class Gestor_Edit_Form(forms.Form):
    username = forms.CharField(max_length=50, label="Nombre de usuario")
    cambiarContra = forms.BooleanField(label="Cambiar contraseña", widget=forms.CheckboxInput(attrs={'onClick':'cambiarContrasena()'}), required=False)
    contrasena1 = forms.CharField(widget=forms.PasswordInput(attrs={'disabled':'disabled'}),label="Contraseña", required=False)
    contrasena2 = forms.CharField(widget=forms.PasswordInput(attrs={'disabled':'disabled'}),label="Contraseña de nuevo", required=False)
    nombre = forms.CharField(max_length=50)