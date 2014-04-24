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
from countries.models import *
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
                length = 13
                chars = string.ascii_letters + string.digits + '!@#$%^&*()'
                random.seed = (os.urandom(1024))
                password = ''.join(random.choice(chars) for i in range(length))
                try:
                    user = User.objects.create_user(nombreUsu, email, password, first_name=seleccionado)
                    user.save()
                    postulante = Postulante.objects.create(usuario=user, tipo="uniextranjera")
                    postulante.save()

                except:
                    error=1
            asunto = "Sistema de Gestion de Intercambio"
            mensaje = "Hola se ha creado a tu nombre una cuenta para utilizar el sistema de gestion de intercambios de la universidad simon bolivar. \n"
            mensaje = mensaje + "tu usuario es:" + user.username + "\n"
            mensaje = mensaje + "tu clave es " + password + "\n"
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

@login_required(login_url='/')
def editar_cuenta(request, id_user):
    logueado = request.user
    error=0
    seleccionado = User.objects.get(id=id_user)
    if request.method == 'POST':
        formulario = NuevoUsuarioForm()
        if seleccionado.first_name == "decanato" or seleccionado.first_name == "dric":
            formulario = NuevoUsuarioForm(request.POST)
            formularioUsuario = formulario
        elif seleccionado.first_name == "coordinacion":
            formulario = NuevaCoordinacionForm(request.POST)
            formularioCoordinacion = formulario
        elif seleccionado.first_name == "estudiante":
            formulario = NuevoEstudianteForm(request.POST)
            formularioEstudiante = formulario
        elif seleccionado.first_name == "extranjero":
            formulario = NuevoEstudianteExtranjeroForm(request.POST)
            formularioEstudianteExtranjero = formulario
        elif seleccionado.first_name == "universidad":
            formulario = NuevaUniversidadExtrangeraForm(request.POST)
            formularioUniversidad = formulario
        if formulario.is_valid():
            if seleccionado.first_name == "decanato" or seleccionado.first_name == "dric":
                #length = 13
                #chars = string.ascii_letters + string.digits + '!@#$%^&*()'
                #random.seed = (os.urandom(1024))
                #password = ''.join(random.choice(chars) for i in range(length))
                try:
                    gestor = Gestor.objects.get(usuario__id=id_user)
                    seleccionado.username = formulario.cleaned_data['nombre_usuario']
                    seleccionado.email = formulario.cleaned_data['email']
                    gestor.nombre = formulario.cleaned_data['nombre']
                    seleccionado.save()
                    gestor.save()
                except:
                    error=1
            elif seleccionado.first_name == "coordinacion":
                nombreUsu = formulario.cleaned_data['nombre_usuarioCoordinacion']
                email = formulario.cleaned_data['emailCoordinacion']
                carrera = formulario.cleaned_data['carreraCoordinacion']
                try:
                    user = User.objects.get(id=id_user)
                    postulante = Postulante.objects.get(usuario=user)
                    user.username=nombreUsu
                    user.email=email
                    user.save()
                    postulante.carrera=carrera
                    postulante.save()

                except:
                    error=1
            elif seleccionado.first_name == "estudiante":
                nombreUsu = formulario.cleaned_data['nombre_usuarioEstudiante']
                email = formulario.cleaned_data['emailEstudiante']
                nombre = formulario.cleaned_data['nombreEstudiante']
                apellido = formulario.cleaned_data['apellidoEstudiante']
                carrera = formulario.cleaned_data['carreraEstudiante']
                carnet = formulario.cleaned_data['carnet']
                try:
                    user = User.objects.get(id=id_user)
                    estudiante = Estudiante.objects.get(user=user)
                    user.username = nombreUsu
                    user.email= email
                    user.save()
                    estudiante.nombre1 = nombre
                    estudiante.apellido1 = apellido
                    estudiante.carnet=carnet
                    estudiante.carrera_usb=carrera
                    estudiante.estudUsb=True
                    estudiante.email=email
                    estudiante.save()

                except:
                    error=1
            elif seleccionado.first_name == "extranjero":
                nombreUsu = formulario.cleaned_data['nombre_usuarioExtranjero']
                email = formulario.cleaned_data['emailExtranjero']
                nombre = formulario.cleaned_data['nombreExtranjero']
                apellido = formulario.cleaned_data['apellidoExtranjero']
                pasaporte = formulario.cleaned_data['pasaporteExtranjero']
                try:
                    user = User.objects.get(id=id_user)
                    estudiante = Estudiante.objects.get(user=user)
                    user.username = nombreUsu
                    user.email= email
                    user.save()
                    estudiante.nombre1 = nombre
                    estudiante.apellido1 = apellido
                    estudiante.carnet=carnet
                    estudiante.carrera_usb=carrera
                    estudiante.estudUsb=False
                    estudiante.email=email
                    estudiante.pasaporte = pasaporte
                    estudiante.save()

                except:
                    error=1
            elif seleccionado.first_name == "universidad":
                nombreUsu= formulario.cleaned_data['nombre_usuarioExtranjera']
                email = formulario.cleaned_data['emailExtranjera']
                try:
                    seleccionado.username = nombreUsu
                    seleccionado.email = email
                    seleccionado.save()


                except:
                    error=1
            #asunto = "Sistema de Gestion de Intercambio"
            #mensaje = "Hola se ha creado a tu nombre una cuenta para utilizar el sistema de gestion de intercambios de la universidad simon bolivar. \n"
            #mensaje = mensaje + "tu usuario es:" + user.username + "\n"
            #mensaje = mensaje + "tu clave es" + password + "\n"
            #correo = EmailMessage(asunto, mensaje, to=['contacto@asuntopais.com'])
            #correo = EmailMessage(asunto, mensaje, to=[user.email])
            try:
                Log.objects.create(usuario=logueado, suceso='Usuario ' + seleccionado.username + ' editado')
                return HttpResponseRedirect('/administrador_listar_usuarios/2')
            except:
                mensaje="error al enviar el mensaje"

    else:
        if seleccionado.first_name == "decanato" or seleccionado.first_name == "dric":
            gestor = Gestor.objects.get(usuario__id=id_user)
            formulario = NuevoUsuarioForm(initial={'nombre_usuario': seleccionado.username, 'nombre': gestor.nombre, 'email': seleccionado.email})
        elif seleccionado.first_name == "coordinacion":
            coordinacion = Postulante.objects.get(usuario__id=id_user)
            formulario = NuevaCoordinacionForm(initial={'nombre_usuarioCoordinacion': seleccionado.username, 'emailCoordinacion': seleccionado.email, 'carreraCoordinacion': coordinacion.carrera})

        elif seleccionado.first_name == "estudiante":
#            estudiante = Estudiante.objects.create(user=user, nombre1=nombre,
 #                                                          nombre2="", apellido1=apellido, apellido2="", carnet=carnet, carrera_usb=carrera, estudUsb=True, email=email)
            estudiante = Estudiante.objects.get(user__id=id_user)
            formulario = NuevoEstudianteForm(initial={'nombre_usuarioEstudiante': seleccionado.username, 'emailEstudiante': seleccionado.email,
                                                      'nombreEstudiante': estudiante.nombre1 + ' ' + estudiante.nombre2,
                                                      'apellidoEstudiante': estudiante.apellido1 + ' ' + estudiante.apellido2,
                                                      'carnet': estudiante.carnet, 'carreraEstudiante': estudiante.carrera_usb})
        elif seleccionado.first_name == "extranjero":
            estudiante = Estudiante.objects.get(user__id=id_user)
            formulario = NuevoEstudianteExtranjeroForm(initial={'nombre_usuarioExtranjero': seleccionado.username, 'emailExtranjero': seleccionado.email,
                                                      'nombreExtranjero': estudiante.nombre1 + ' ' + estudiante.nombre2,
                                                      'apellidoExtranjero': estudiante.apellido1 + ' ' + estudiante.apellido2,
                                                      'carnet': estudiante.carnet, 'pasaporteExtranjero': estudiante.pasaporte})
        elif seleccionado.first_name == "universidad":
            postulante = Postulante.objects.get(usuario__id=id_user)
            formulario = NuevaUniversidadExtrangeraForm(initial={'nombre_usuarioExtranjera': seleccionado.username,
                                                                 'emailExtranjera': seleccionado.email})
    return render_to_response('administrador/editar_cuenta.html', {'formulario': formulario,
                                                                  'seleccionado': seleccionado.first_name,
                                                                  'error': error}, context_instance=RequestContext(request))

@login_required(login_url='/')
def redactar_anuncio(request):
    carreras = Carrera.objects.all()
    universidades = Universidad.objects.all()
    paises = Country.objects.all()
    for pais in paises:
        print pais.name
    return render_to_response('administrador/redactar_anuncio.html', {'carreras': carreras,
                                                                      'universidades': universidades,
                                                                      'paises': paises}, context_instance=RequestContext(request))
@login_required(login_url='/')
def crear_universidad(request):
    if request.method == 'POST':
        formulario = CrearUniversidadForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/administrador_listar_universidad/1')
    else:
        formulario = CrearUniversidadForm()
    return render_to_response('administrador/crear_universidad.html', {'formulario': formulario}, context_instance=RequestContext(request))

@login_required(login_url='/')
def listar_universidades(request, creado):
    universidades = Universidad.objects.all()
    return render_to_response('administrador/listar_universidad.html', {'universidades': universidades, 'creado': creado}, context_instance=RequestContext(request))

@login_required(login_url='/')
def eliminar_universidad(request, id_universidad):
    if request.user.first_name == 'admin':
        universidad = Universidad.objects.get(id=id_universidad).delete()
        return HttpResponseRedirect('/administrador_listar_universidad/3')
    else:
        return HttpResponseRedirect('/')
