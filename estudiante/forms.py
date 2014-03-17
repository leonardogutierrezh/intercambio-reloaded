#encoding:utf-8
from django.forms import ModelForm
from django.db import models
from django import forms
from django.contrib.auth.models import User
from estudiante.models import *
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import CheckboxSelectMultiple

class EstudianteUSB_Form(forms.Form):
    nombre1 = forms.CharField(max_length=50, label="Primer nombre")
    nombre2 = forms.CharField(max_length=50, label="Segundo nombre", required=False)
    apellido1 = forms.CharField(max_length=50, label="Primer apellido")
    apellido2 = forms.CharField(max_length=50, label="Segundo apellido", required=False)
    email = forms.EmailField()
    carnet = forms.CharField(max_length=8)
    username = forms.CharField(max_length=50, label="Nombre de usuario")
    contrasena1 = forms.CharField(widget=forms.PasswordInput,label="Contrasena")
    contrasena2 = forms.CharField(widget=forms.PasswordInput,label="Contrasena de nuevo")

class EstudianteExt_Form(forms.Form):
    nombre1 = forms.CharField(max_length=50, label="Primer nombre")
    nombre2 = forms.CharField(max_length=50, label="Segundo nombre", required=False)
    apellido1 = forms.CharField(max_length=50, label="Primer apellido")
    apellido2 = forms.CharField(max_length=50, label="Segundo apellido", required=False)
    email = forms.EmailField()
    pasaporte = forms.CharField(max_length=50)
    username = forms.CharField(max_length=50, label="Nombre de usuario")
    contrasena1 = forms.CharField(widget=forms.PasswordInput,label="Contrasena")
    contrasena2 = forms.CharField(widget=forms.PasswordInput,label="Contrasena de nuevo")

class EstudianteUSB_Edit_Form(forms.Form):
    nombre1 = forms.CharField(max_length=50, label="Primer nombre")
    nombre2 = forms.CharField(max_length=50, label="Segundo nombre", required=False)
    apellido1 = forms.CharField(max_length=50, label="Primer apellido")
    apellido2 = forms.CharField(max_length=50, label="Segundo apellido", required=False)
    email = forms.EmailField(label="aqui")
    carnet = forms.CharField(max_length=8)
    username = forms.CharField(max_length=50, label="Nombre de usuario")
    cambiarContra = forms.BooleanField(label="Cambiar contrasena", widget=forms.CheckboxInput(attrs={'onClick':'cambiarContrasena()'}), required=False)
    contrasena1 = forms.CharField(widget=forms.PasswordInput(attrs={'disabled':'disabled'}),label="Contrasena", required=False)
    contrasena2 = forms.CharField(widget=forms.PasswordInput(attrs={'disabled':'disabled'}),label="Contrasena de nuevo", required=False)

class EstudianteExt_Edit_Form(forms.Form):
    nombre1 = forms.CharField(max_length=50, label="Primer nombre")
    nombre2 = forms.CharField(max_length=50, label="Segundo nombre", required=False)
    apellido1 = forms.CharField(max_length=50, label="Primer apellido")
    apellido2 = forms.CharField(max_length=50, label="Segundo apellido", required=False)
    email = forms.EmailField(label="aqui")
    pasaporte = forms.CharField(max_length=50)
    username = forms.CharField(max_length=50, label="Nombre de usuario")
    cambiarContra = forms.BooleanField(label="Cambiar contrasena", widget=forms.CheckboxInput(attrs={'onClick':'cambiarContrasena()'}), required=False)
    contrasena1 = forms.CharField(widget=forms.PasswordInput(attrs={'disabled':'disabled'}),label="Contrasena", required=False)
    contrasena2 = forms.CharField(widget=forms.PasswordInput(attrs={'disabled':'disabled'}),label="Contrasena de nuevo", required=False)

class formularioUNO_formUSB(forms.Form):
    genero_choices = (
        ('femenino', 'Femenino'),
        ('masculino', 'Masculino'),
    )
    nombre1 = forms.CharField(max_length=50, label="Primer nombre" ,widget=forms.TextInput(attrs={'disabled':'disabled'}))
    nombre2 = forms.CharField(max_length=50, label="Segundo nombre", required=False ,widget=forms.TextInput(attrs={'disabled':'disabled'}))
    apellido1 = forms.CharField(max_length=50, label="Primer apellido" ,widget=forms.TextInput(attrs={'disabled':'disabled'}))
    apellido2 = forms.CharField(max_length=50, label="Segundo apellido", required=False ,widget=forms.TextInput(attrs={'disabled':'disabled'}))
    genero = forms.ChoiceField(choices=genero_choices)
    nacionalidad = forms.CharField(max_length=50)
    cedula = forms.IntegerField(widget=forms.TextInput(attrs={'onkeypress':'return numero(event)','onkeyup':'return numero(event)'}))
    carnet = forms.CharField(max_length=8 ,widget=forms.TextInput(attrs={'disabled':'disabled'}))

class formularioUNO_formExt(forms.Form):
    genero_choices = (
        ('femenino', 'Femenino'),
        ('masculino', 'Masculino'),
    )
    nombre1 = forms.CharField(max_length=50, label="Primer nombre" ,widget=forms.TextInput(attrs={'disabled':'disabled'}))
    nombre2 = forms.CharField(max_length=50, label="Segundo nombre", required=False ,widget=forms.TextInput(attrs={'disabled':'disabled'}))
    apellido1 = forms.CharField(max_length=50, label="Primer apellido" ,widget=forms.TextInput(attrs={'disabled':'disabled'}))
    apellido2 = forms.CharField(max_length=50, label="Segundo apellido", required=False ,widget=forms.TextInput(attrs={'disabled':'disabled'}))
    genero = forms.ChoiceField(choices=genero_choices)
    nacionalidad = forms.CharField(max_length=50)
    pasaporte = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'disabled':'disabled'}))
