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
    carrera = forms.ModelChoiceField(queryset=CarreraUsb.objects.all())

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
    nombre1 = forms.CharField(max_length=50, label="Primer nombre", required=False)
    nombre2 = forms.CharField(max_length=50, label="Segundo nombre", required=False)
    apellido1 = forms.CharField(max_length=50, label="Primer apellido" , required=False)
    apellido2 = forms.CharField(max_length=50, label="Segundo apellido", required=False)
    genero = forms.ChoiceField(choices=genero_choices)
    fecha = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}),label='Fecha de nacimiento')
    nacionalidad = forms.ModelChoiceField(queryset=Country.objects.all())
    cedula = forms.IntegerField(widget=forms.TextInput(attrs={'onkeypress':'return numero(event)','onkeyup':'return numero(event)'}))
    carnet = forms.CharField(max_length=8 , required=False)

class formularioUNO_formExt(forms.Form):
    genero_choices = (
        ('femenino', 'Femenino'),
        ('masculino', 'Masculino'),
    )
    nombre1 = forms.CharField(max_length=50, label="Primer nombre" , required=False)
    nombre2 = forms.CharField(max_length=50, label="Segundo nombre", required=False )
    apellido1 = forms.CharField(max_length=50, label="Primer apellido" , required=False)
    apellido2 = forms.CharField(max_length=50, label="Segundo apellido", required=False)
    genero = forms.ChoiceField(choices=genero_choices)
    fecha = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}),label='Fecha de nacimiento')
    nacionalidad = forms.ModelChoiceField(queryset=Country.objects.all())
    pasaporte = forms.CharField(max_length=50, required=False)

class formularioDOS_form(forms.Form):
    urbanizacion = forms.CharField(max_length=100, label='Urb / Sector / Barrio')
    calle = forms.CharField(max_length=50)
    edificio  = forms.CharField(max_length=50, label='Edificio / Casa')
    apartamento = forms.CharField(max_length=50, label="Apartamento/Nro Casa")
    codigo_postal = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'onkeypress':'return numero(event)','onkeyup':'return numero(event)'}))

class formularioTRES_form(forms.Form):
    cel = forms.IntegerField(widget=forms.TextInput(attrs={'onkeypress':'return numero(event)','onkeyup':'return numero(event)'}), label="Telefono celular")
    tel_casa = forms.IntegerField(widget=forms.TextInput(attrs={'onkeypress':'return numero(event)','onkeyup':'return numero(event)'}), label="Telefono casa")
    email = forms.EmailField()

class formularioCUATRO_formUSB(forms.Form):
    programa= forms.ModelChoiceField(queryset=ProgramaIntercambio.objects.all())

class formularioCUATRO_formExt(forms.Form):
    programa= forms.ModelChoiceField(queryset=ProgramaIntercambio.objects.all())

class formularioCINCO_formUSB(forms.Form):
    carrera = forms.ModelChoiceField(queryset=CarreraUsb.objects.all())
    creditos = forms.IntegerField(widget=forms.TextInput(attrs={'onkeypress':'return numero(event)','onkeyup':'return numero(event)'}), label="Numero de créditos aprobados hasta el momento")
    indice = forms.FloatField(widget=forms.TextInput(attrs={'onkeypress':'return numero(event)','onkeyup':'return numero(event)'}), label="Indice academico")

class formularioCINCO_formExt(forms.Form):
    anoIngreso = forms.IntegerField(widget=forms.TextInput(attrs={'onkeypress':'return numero(event)','onkeyup':'return numero(event)'}), label="Ano ingreso a la carrera")
    anosAprob = forms.IntegerField(widget=forms.TextInput(attrs={'onkeypress':'return numero(event)','onkeyup':'return numero(event)'}), label="Cantidad de años aprobados hasta la fecha")

class formularioSEIS_form(forms.Form):
    ingreso_choices = (
        ('personal', 'Personal'),
        ('familiar', 'Familiar'),
        ('otro', 'Otro'),
        )
    ayuda_choices = (
        ('si','Si'),
        ('no','No'),
    )
    fuente_ingreso= forms.ChoiceField(choices=ingreso_choices,label='Principal fuente de ingresos:')
    detalle_fuente = forms.CharField(max_length=50,label='Especifique')
    ayuda = forms.ChoiceField(choices=ayuda_choices,label='¿Recibe algún tipo de ayuda económica?:')
    detalle_ayuda = forms.CharField(max_length=50,label='Especifique')

class formularioSIETE_form(forms.Form):
    apellidos = forms.CharField(max_length=50)
    nombres = forms.CharField(max_length=50)
    cel = forms.IntegerField(widget=forms.TextInput(attrs={'onkeypress':'return numero(event)','onkeyup':'return numero(event)'}), label="Telefono celular")
    tel_casa = forms.IntegerField(widget=forms.TextInput(attrs={'onkeypress':'return numero(event)','onkeyup':'return numero(event)'}), label="Telefono casa")
    email = forms.EmailField()
    rel_estudiante = forms.CharField(max_length=50, label="Relacion con el estudiante")
    direccion = forms.CharField(max_length=500)

class documentosRequeridosUSB_form(forms.Form):
    foto = forms.ImageField()
    informe = forms.FileField(label='Informe académico')
    carta = forms.FileField(label='Carta de motivación')
    planilla = forms.FileField(required=False,label='*Planilla CINDA/SMILE')
    certificado = forms.FileField(required=False,label='**Certificado de idiomas')

class documentosRequeridosExt_form(forms.Form):
    foto = forms.ImageField()
    informe = forms.FileField(label='Informe académico')
    carta = forms.FileField(label='Carta de motivación')
    planilla = forms.FileField(required=False,label='*Planilla CINDA/SMILE')
    certificado = forms.FileField(required=False,label='**Certificado de idiomas')