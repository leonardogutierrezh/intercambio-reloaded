from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context, Template
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from administrador.models import *
from administrador.forms import *
import os, random, string
import datetime
# Create your views here.

def inicio(request):
    return render_to_response('inicio.html', {}, context_instance=RequestContext(request))

def crear_cuenta(request):
    formularioUsuario = NuevoUsuarioForm()
    formularioCoordinacion = NuevaCoordinacionForm()
    formularioEstudiante = NuevoEstudianteForm()
    formularioEstudianteExtranjero = NuevoEstudianteExtranjeroForm()
    formularioUniversidad = NuevaUniversidadExtrangeraForm()
    if request.method == 'POST':
        seleccionado = request.POST.get('opcion')
        print seleccionado
        formulario = NuevoUsuarioForm()
        if seleccionado == "gestor":
            formulario = NuevoUsuarioForm(request.POST)
            formularioUsuario = formulario
        elif seleccionado == "coordinacion":
            formulario = NuevaCoordinacionForm(request.POST)
            formularioCoordinacion = formulario
        elif seleccionado == "estudiante":
            formulario = NuevoEstudianteForm(request.POST)
            formularioEstudiante = formulario
        elif seleccionado == "extranjero":
            formulario = NuevoEstudianteExtranjeroForm(request.POST)
            formularioEstudianteExtranjero = formulario
        elif seleccionado == "universidad":
            formulario = NuevaUniversidadExtrangeraForm(request.POST)
            formularioUniversidad = formulario
        if formulario.is_valid():
            if seleccionado == "gestor":
                nombreUsu = formulario.cleaned_data['nombre_usuario']
                email = formulario.cleaned_data['email']
                nombre = formulario.cleaned_data['nombre']
                length = 13
                chars = string.ascii_letters + string.digits + '!@#$%^&*()'
                random.seed = (os.urandom(1024))
                password = ''.join(random.choice(chars) for i in range(length))
                user = User.objects.create_user(nombreUsu, email, password)
                user.save()
                tipo = Usuario.objects.create(usuario=user, tipo="gestor")
            elif seleccionado == "coordinacion":
                nombreUsu = formulario.cleaned_data['nombre_usuarioCoordinacion']
                email = formulario.cleaned_data['emailCoordinacion']
                carrera = formulario.cleaned_data['carreraCoordinacion']
                length = 13
                chars = string.ascii_letters + string.digits + '!@#$%^&*()'
                random.seed = (os.urandom(1024))
                password = ''.join(random.choice(chars) for i in range(length))
                user = User.objects.create_user(nombreUsu, email, password)
                user.save()
                tipo = Usuario.objects.create(usuario=user, tipo="postulante")
            elif seleccionado == "estudiante":
                nombreUsu = formulario.cleaned_data['nombre_usuarioEstudiante']
                email = formulario.cleaned_data['emailEstudiante']
                nombre = formulario.cleaned_data['nombreEstudiante']
                apellido = formulario.cleaned_data['apellidoEstudiante']
                carrera = formulario.cleaned_data['carreraEstudiante']
                length = 13
                chars = string.ascii_letters + string.digits + '!@#$%^&*()'
                random.seed = (os.urandom(1024))
                password = ''.join(random.choice(chars) for i in range(length))
                user = User.objects.create_user(nombreUsu, email, password)
                user.save()
                tipo = Usuario.objects.create(usuario=user, tipo="estudiante")
            elif seleccionado == "extranjero":
                nombreUsu = formulario.cleaned_data['nombre_usuarioExtranjero']
                email = formulario.cleaned_data['emailExtranjero']
                nombre = formulario.cleaned_data['nombreExtranjero']
                apellido = formulario.cleaned_data['apellidoExtranjero']
                pasaporte = formulario.cleaned_data['pasaporteExtranjero']
                length = 13
                chars = string.ascii_letters + string.digits + '!@#$%^&*()'
                random.seed = (os.urandom(1024))
                password = ''.join(random.choice(chars) for i in range(length))
                user = User.objects.create_user(nombreUsu, email, password)
                user.save()
                tipo = Usuario.objects.create(usuario=user, tipo="extranjero")
            elif seleccionado == "universidad":
                nombreUsu= formulario.cleaned_data['nombre_usuarioExtranjera']
                email = formulario.cleaned_data['emailExtranjera']
                nombre = formulario.cleaned_data['nombreExtranjera']
                length = 13
                chars = string.ascii_letters + string.digits + '!@#$%^&*()'
                random.seed = (os.urandom(1024))
                password = ''.join(random.choice(chars) for i in range(length))
                user = User.objects.create_user(nombreUsu, email, password)
                user.save()
                tipo = Usuario.objects.create(usuario=user, tipo="universidad")
                return  HttpResponseRedirect("/administrador_listar_usuarios/1")
    else:
        seleccionado = "gestor"
    return render_to_response('administrador/crear_cuenta.html', {'formularioUsuario': formularioUsuario,
                                                                  'formularioCoordinacion': formularioCoordinacion,
                                                                  'formularioEstudiante': formularioEstudiante,
                                                                  'formularioEstudianteExtranjero': formularioEstudianteExtranjero,
                                                                  'formularioUniversidad': formularioUniversidad,
                                                                  'seleccionado': seleccionado}, context_instance=RequestContext(request))

def listar_usuarios(request, creado):
    lista_usuarios = []
    usuarios = User.objects.filter(is_staff=False)
    for usuario in usuarios:
        tipo = Usuario.objects.get(usuario=usuario)
        tupla = (usuario, tipo)
    return render_to_response('administrador/listar_usuarios.html', {'usuarios', lista_usuarios}, context_instance=RequestContext(request))