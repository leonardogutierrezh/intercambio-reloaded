from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context, Template
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.core.mail import EmailMessage, EmailMultiAlternatives
from administrador.models import *
from estudiante.models import *
from administrador.forms import *
from gestor.models import *
from postulante.models import *
import os, random, string
import datetime
# Create your views here.

def inicio(request):
    return render_to_response('inicio.html', {}, context_instance=RequestContext(request))

def crear_cuenta(request):
    logueado = request.user
    error=0
    formularioUsuario = NuevoUsuarioForm()
    formularioCoordinacion = NuevaCoordinacionForm()
    formularioEstudiante = NuevoEstudianteForm()
    formularioEstudianteExtranjero = NuevoEstudianteExtranjeroForm()
    formularioUniversidad = NuevaUniversidadExtrangeraForm()
    if request.method == 'POST':
        seleccionado = request.POST.get('opcion')
        formulario = NuevoUsuarioForm()
        if seleccionado == "decanato" or seleccionado == "dric":
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
            if seleccionado == "decanato" or seleccionado == "dric":
                nombreUsu = formulario.cleaned_data['nombre_usuario']
                email = formulario.cleaned_data['email']
                nombre = formulario.cleaned_data['nombre']
                length = 13
                chars = string.ascii_letters + string.digits + '!@#$%^&*()'
                random.seed = (os.urandom(1024))
                password = ''.join(random.choice(chars) for i in range(length))
                try:
                    user = User.objects.create_user(nombreUsu, email, password, first_name=seleccionado)
                    user.save()
                    gestor = Gestor.objects.create(usuario=user, nombre=nombre)
                    gestor.save()

                except:
                    error=1
            elif seleccionado == "coordinacion":
                nombreUsu = formulario.cleaned_data['nombre_usuarioCoordinacion']
                email = formulario.cleaned_data['emailCoordinacion']
                carrera = formulario.cleaned_data['carreraCoordinacion']
                length = 13
                chars = string.ascii_letters + string.digits + '!@#$%^&*()'
                random.seed = (os.urandom(1024))
                password = ''.join(random.choice(chars) for i in range(length))
                try:
                    user = User.objects.create_user(nombreUsu, email, password, first_name=seleccionado)
                    user.save()
                    coordinacion = Postulante.objects.create(usuario=user, tipo="coordinacion", carrera=carrera)
                    coordinacion.save()

                except:
                    error=1
            elif seleccionado == "estudiante":
                nombreUsu = formulario.cleaned_data['nombre_usuarioEstudiante']
                email = formulario.cleaned_data['emailEstudiante']
                nombre = formulario.cleaned_data['nombreEstudiante']
                apellido = formulario.cleaned_data['apellidoEstudiante']
                carrera = formulario.cleaned_data['carreraEstudiante']
                carnet = formulario.cleaned_data['carnet']
                length = 13
                chars = string.ascii_letters + string.digits + '!@#$%^&*()'
                random.seed = (os.urandom(1024))
                password = ''.join(random.choice(chars) for i in range(length))
                try:
                    user = User.objects.create_user(nombreUsu, email, password, first_name=seleccionado)
                    user.save()
                    estudiante = Estudiante.objects.create(user=user, nombre1=nombre,
                                                           nombre2="", apellido1=apellido, apellido2="", carnet=carnet, carrera_usb=carrera, estudUsb=True, email=email)
                    estudiante.save()

                except:
                    error=1
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
                try:
                    user = User.objects.create_user(nombreUsu, email, password, first_name=seleccionado)
                    user.save()
                    extranjero = Estudiante.objects.create(user=user, nombre1=nombre, nombre2="", apellido1=apellido, apellido2="", email=email, pasaporte=pasaporte)
                    extranjero.save()

                except:
                    error=1
            elif seleccionado == "universidad":
                nombreUsu= formulario.cleaned_data['nombre_usuarioExtranjera']
                email = formulario.cleaned_data['emailExtranjera']
                nombre = formulario.cleaned_data['nombreExtranjera']
                pais = formulario.cleaned_data['pais']
                length = 13
                chars = string.ascii_letters + string.digits + '!@#$%^&*()'
                random.seed = (os.urandom(1024))
                password = ''.join(random.choice(chars) for i in range(length))
                try:
                    user = User.objects.create_user(nombreUsu, email, password, first_name=seleccionado)
                    user.save()
                    universidad = Universidad.objects.create(nombre=nombre, pais=pais)
                    universidad.save()
                    postulante = Postulante.objects.create(usuario=user, tipo="uniextranjera", universidad=universidad)

                except:
                    error=1
            asunto = "Sistema de Gestion de Intercambio"
            mensaje = "Hola se ha creado a tu nombre una cuenta para utilizar el sistema de gestion de intercambios de la universidad simon bolivar. \n"
            mensaje = mensaje + "tu usuario es:" + user.username + "\n"
            mensaje = mensaje + "tu clave es" + password + "\n"
            #correo = EmailMessage(asunto, mensaje, to=['contacto@asuntopais.com'])
            correo = EmailMessage(asunto, mensaje, to=[user.email])
            try:
                print "enviando"
                correo.send()
                Log.objects.create(usuario=logueado, suceso='Nuevo usuario creado')
                return HttpResponseRedirect('/administrador_listar_usuarios/1')
            except:
                mensaje="error al enviar el mensaje"

    else:
        seleccionado = "decanato"
    return render_to_response('administrador/crear_cuenta.html', {'formularioUsuario': formularioUsuario,
                                                                  'formularioCoordinacion': formularioCoordinacion,
                                                                  'formularioEstudiante': formularioEstudiante,
                                                                  'formularioEstudianteExtranjero': formularioEstudianteExtranjero,
                                                                  'formularioUniversidad': formularioUniversidad,
                                                                  'seleccionado': seleccionado,
                                                                  'error': error}, context_instance=RequestContext(request))

@login_required(login_url='/')
def listar_usuarios(request, creado):
    lista_usuarios = []
    usuarios = User.objects.filter(is_staff=False)
    return render_to_response('administrador/listar_usuarios.html', {'usuarios': usuarios, 'creado': creado}, context_instance=RequestContext(request))

@login_required(login_url='/')
def ver_usuario(request, id_usuario):
    perfil = ""
    usuario = User.objects.get(id=id_usuario)
    print usuario.first_name

    if usuario.first_name == "decanato" or usuario.first_name == "dric":
        perfil = Gestor.objects.get(usuario=usuario)
    elif usuario.first_name == "coordinacion":
        perfil = Postulante.objects.get(usuario=usuario)
    elif usuario.first_name == "estudiante" or usuario.first_name == "extranjero":
        perfil = Estudiante.objects.get(user=usuario)
    elif usuario.first_name == "universidad":
        perfil = Postulante.objects.get(usuario=usuario)
    return render_to_response('administrador/ver_usuario.html', {'usuario':usuario, 'perfil': perfil}, context_instance=RequestContext(request))

@login_required(login_url='/')
def editar_perfil(request):
    usuario = request.user
    print usuario.check_password('123')
    creado= 0
    if Administrador.objects.filter(usuario=usuario):
        perfil = Administrador.objects.get(usuario=usuario)
    else:
        perfil = Administrador.objects.create(usuario=usuario)
    if request.method == 'POST':
        formulario = EditarPerfilForm(request.POST)
        if formulario.is_valid():
            nombre = formulario.cleaned_data['nombre']
            email = formulario.cleaned_data['email']
            us = formulario.cleaned_data['usuario']
            perfil.nombre = nombre
            perfil.email = email
            usuario.username = us
            perfil.save()
            try:
                usuario.save()
            except:
                creado = "5"
                return render_to_response('administrador/editar_perfil.html', {'formulario': formulario, 'creado': creado}, context_instance=RequestContext(request))
            creado= '2'
            if request.POST.get('vieja') != "":
                creado= '3'
            if usuario.check_password(request.POST.get('vieja')):
                print 'entreeeeeeeeeeeeee'
                nueva = request.POST.get('nueva')
                repetida = request.POST.get('repetida')
                print nueva
                print repetida
                creado = "4"
                if nueva == repetida:
                    print 'iguales'
                    usuario.set_password(nueva)
                    usuario.save()
                    creado= "2"
            Log.objects.create(usuario=usuario, suceso="Perfil modificado")
    else:
        formulario = EditarPerfilForm(initial={'nombre': perfil.nombre, 'email': perfil.email, 'usuario': usuario.username})
    return render_to_response('administrador/editar_perfil.html', {'formulario': formulario, 'creado': creado}, context_instance=RequestContext(request))

def cerrar_sesion(request):
    logout(request)
    return HttpResponseRedirect("/")

def recaudosExt(request):
    parrafo = 'recaudosExt'
    return render_to_response('recaudos.html', {'parrafo':parrafo}, context_instance=RequestContext(request))

def recaudosNac(request):
    parrafo = 'recaudosNac'
    return render_to_response('recaudos.html',{'parrafo':parrafo}, context_instance=RequestContext(request))

def recaudosAdic(request):
    parrafo = 'recaudosAdic'
    return render_to_response('recaudos.html',{'parrafo':parrafo}, context_instance=RequestContext(request))

@login_required(login_url='/')
def eliminar_usuario(request, id_usuario):
    admin = request.user
    if admin.first_name == 'admin':
        usuario = User.objects.get(id=id_usuario)
        Log.objects.create(usuario=admin, suceso='eliminado el usuario ' + usuario.username)
        usuario.delete()
    return HttpResponseRedirect('/administrador_listar_usuarios/3')

@login_required(login_url='/')
def ver_log(request):
    log = Log.objects.all().order_by('fecha')
    return render_to_response('administrador/log.html', {'log': log}, context_instance=RequestContext(request))

def editar_cuenta(request, id_user):
    logueado = request.user
    error=0
    seleccionado = User.objects.get(id=id_user).first_name
    if seleccionado == "decanato" or seleccionado == "dric":
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
    if request.method == 'POST':
        formulario = NuevoUsuarioForm()
        if seleccionado == "decanato" or seleccionado == "dric":
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
            if seleccionado == "decanato" or seleccionado == "dric":
                nombreUsu = formulario.cleaned_data['nombre_usuario']
                email = formulario.cleaned_data['email']
                nombre = formulario.cleaned_data['nombre']
                length = 13
                chars = string.ascii_letters + string.digits + '!@#$%^&*()'
                random.seed = (os.urandom(1024))
                password = ''.join(random.choice(chars) for i in range(length))
                try:
                    user = User.objects.create_user(nombreUsu, email, password, first_name=seleccionado)
                    user.save()
                    gestor = Gestor.objects.create(usuario=user, nombre=nombre)
                    gestor.save()

                except:
                    error=1
            elif seleccionado == "coordinacion":
                nombreUsu = formulario.cleaned_data['nombre_usuarioCoordinacion']
                email = formulario.cleaned_data['emailCoordinacion']
                carrera = formulario.cleaned_data['carreraCoordinacion']
                length = 13
                chars = string.ascii_letters + string.digits + '!@#$%^&*()'
                random.seed = (os.urandom(1024))
                password = ''.join(random.choice(chars) for i in range(length))
                try:
                    user = User.objects.create_user(nombreUsu, email, password, first_name=seleccionado)
                    user.save()
                    coordinacion = Postulante.objects.create(usuario=user, tipo="coordinacion", carrera=carrera)
                    coordinacion.save()

                except:
                    error=1
            elif seleccionado == "estudiante":
                nombreUsu = formulario.cleaned_data['nombre_usuarioEstudiante']
                email = formulario.cleaned_data['emailEstudiante']
                nombre = formulario.cleaned_data['nombreEstudiante']
                apellido = formulario.cleaned_data['apellidoEstudiante']
                carrera = formulario.cleaned_data['carreraEstudiante']
                carnet = formulario.cleaned_data['carnet']
                length = 13
                chars = string.ascii_letters + string.digits + '!@#$%^&*()'
                random.seed = (os.urandom(1024))
                password = ''.join(random.choice(chars) for i in range(length))
                try:
                    user = User.objects.create_user(nombreUsu, email, password, first_name=seleccionado)
                    user.save()
                    estudiante = Estudiante.objects.create(user=user, nombre1=nombre,
                                                           nombre2="", apellido1=apellido, apellido2="", carnet=carnet, carrera_usb=carrera, estudUsb=True, email=email)
                    estudiante.save()

                except:
                    error=1
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
                try:
                    user = User.objects.create_user(nombreUsu, email, password, first_name=seleccionado)
                    user.save()
                    extranjero = Estudiante.objects.create(user=user, nombre1=nombre, nombre2="", apellido1=apellido, apellido2="", email=email, pasaporte=pasaporte)
                    extranjero.save()

                except:
                    error=1
            elif seleccionado == "universidad":
                nombreUsu= formulario.cleaned_data['nombre_usuarioExtranjera']
                email = formulario.cleaned_data['emailExtranjera']
                nombre = formulario.cleaned_data['nombreExtranjera']
                pais = formulario.cleaned_data['pais']
                length = 13
                chars = string.ascii_letters + string.digits + '!@#$%^&*()'
                random.seed = (os.urandom(1024))
                password = ''.join(random.choice(chars) for i in range(length))
                try:
                    user = User.objects.create_user(nombreUsu, email, password, first_name=seleccionado)
                    user.save()
                    universidad = Universidad.objects.create(nombre=nombre, pais=pais)
                    universidad.save()
                    postulante = Postulante.objects.create(usuario=user, tipo="uniextranjera", universidad=universidad)

                except:
                    error=1
            asunto = "Sistema de Gestion de Intercambio"
            mensaje = "Hola se ha creado a tu nombre una cuenta para utilizar el sistema de gestion de intercambios de la universidad simon bolivar. \n"
            mensaje = mensaje + "tu usuario es:" + user.username + "\n"
            mensaje = mensaje + "tu clave es" + password + "\n"
            #correo = EmailMessage(asunto, mensaje, to=['contacto@asuntopais.com'])
            correo = EmailMessage(asunto, mensaje, to=[user.email])
            try:
                print "enviando"
                correo.send()
                Log.objects.create(usuario=logueado, suceso='Nuevo usuario creado')
                return HttpResponseRedirect('/administrador_listar_usuarios/1')
            except:
                mensaje="error al enviar el mensaje"

    else:
        seleccionado = "decanato"
    return render_to_response('administrador/editar_cuenta.html', {'formularioUsuario': formularioUsuario,
                                                                  'formulario': formulario,
                                                                  'seleccionado': seleccionado,
                                                                  'error': error}, context_instance=RequestContext(request))
