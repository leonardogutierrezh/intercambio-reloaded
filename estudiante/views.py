from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context, Template
from django.contrib.auth.decorators import login_required
from estudiante.models import *
from estudiante.forms import *
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage, EmailMultiAlternatives
import os, random, string

def registrarEstudianteUSB(request):
    if request.method == 'POST':
        formulario = EstudianteUSB_Form(request.POST)
        if formulario.is_valid():

            nombre1 = formulario.cleaned_data['nombre1']
            nombre2 = formulario.cleaned_data['nombre2']
            apellido1 = formulario.cleaned_data['apellido1']
            apellido2 = formulario.cleaned_data['apellido2']
            email = formulario.cleaned_data['email']
            carnet = formulario.cleaned_data['carnet']
            username = formulario.cleaned_data['username']
            contrasena1 = formulario.cleaned_data['contrasena1']
            contrasena2 = formulario.cleaned_data['contrasena2']

            aux = User.objects.filter(username=username)
            if len(aux) != 0:
                UsuarioRepetido = "El nombre de usuario ya existe **"
                return render_to_response('estudiante/registrarEstudianteUSB.html', {'formulario': formulario,'UsuarioRepetido':UsuarioRepetido},context_instance=RequestContext(request))

            if contrasena1 != contrasena2:
                ContrasenaDist = "Las contrasenas deben coincidir **"
                return render_to_response('estudiante/registrarEstudianteUSB.html', {'formulario': formulario,'ContrasenaDist':ContrasenaDist},context_instance=RequestContext(request))

            user = User.objects.create_user(username,email,contrasena1)
            user.first_name = "estudianteUSB"
            user.save()
            estudiante = Estudiante.objects.create(user=user,nombre1=nombre1,nombre2=nombre2,apellido1=apellido1,apellido2=apellido2,email=email,carnet=carnet,estudUsb=True)
            estudiante.save()

            return HttpResponseRedirect('/')
    else:
        formulario = EstudianteUSB_Form()
    return render_to_response('estudiante/registrarEstudianteUSB.html', {'formulario': formulario},context_instance=RequestContext(request))

def registrarEstudianteExt(request):
    if request.method == 'POST':
        formulario = EstudianteExt_Form(request.POST)
        if formulario.is_valid():

            nombre1 = formulario.cleaned_data['nombre1']
            nombre2 = formulario.cleaned_data['nombre2']
            apellido1 = formulario.cleaned_data['apellido1']
            apellido2 = formulario.cleaned_data['apellido2']
            email = formulario.cleaned_data['email']
            pasaporte = formulario.cleaned_data['pasaporte']
            username = formulario.cleaned_data['username']
            contrasena1 = formulario.cleaned_data['contrasena1']
            contrasena2 = formulario.cleaned_data['contrasena2']

            aux = User.objects.filter(username=username)
            if len(aux) != 0:
                UsuarioRepetido = "El nombre de usuario ya existe **"
                return render_to_response('estudiante/registrarEstudianteUSB.html', {'formulario': formulario,'UsuarioRepetido':UsuarioRepetido},context_instance=RequestContext(request))

            if contrasena1 != contrasena2:
                ContrasenaDist = "Las contrasenas deben coincidir **"
                return render_to_response('estudiante/registrarEstudianteUSB.html', {'formulario': formulario,'ContrasenaDist':ContrasenaDist},context_instance=RequestContext(request))

            user = User.objects.create_user(username,email,contrasena1)
            user.first_name = "estudianteExt"
            user.save()
            estudiante = Estudiante.objects.create(user=user,nombre1=nombre1,nombre2=nombre2,apellido1=apellido1,apellido2=apellido2,email=email,estudUsb=False,pasaporte=pasaporte)
            estudiante.save()

            return HttpResponseRedirect('/')
    else:
        formulario = EstudianteExt_Form()
    return render_to_response('estudiante/registrarEstudianteExt.html', {'formulario': formulario},context_instance=RequestContext(request))

def iniciarSesion(request):
    if request.method == 'POST':
        if 'iniciar' in request.POST:
            formulario = AuthenticationForm(request.POST)
            if formulario.is_valid:
                usuario = request.POST['username']
                clave = request.POST['password']
                acceso = authenticate(username=usuario, password=clave)
                if acceso is not None:
                    login(request,acceso)
                    #return HttpResponseRedirect('/index')
                    print 'hice login'
                    return render_to_response('index.html', context_instance=RequestContext(request))
                else:
                    formulario = AuthenticationForm()
                    error_log = "Nombre de usuario o contrasena incorrectos **"
                    return render_to_response('iniciarSesion.html',{'formulario':formulario,'error_log':error_log}, context_instance=RequestContext(request))
        if 'recuperar' in request.POST:
            formulario = AuthenticationForm(request.POST)
            usuario = request.POST['username']
            try:
                user = User.objects.get(username=usuario)
            except:
                mensajeRecuperar = "Nombre de usuario no existe. Trate de nuevo"
                return render_to_response('iniciarSesion.html', {'formulario':formulario,'mensajeRecuperar':mensajeRecuperar}, context_instance=RequestContext(request))
            length = 13
            chars = string.ascii_letters + string.digits + '!@#$%^&*()'
            random.seed = (os.urandom(1024))
            password = ''.join(random.choice(chars) for i in range(length))

            titulo = 'Recuperacion contrasena Sistema Intercambio'
            contenido = "Buenos dias, \n"
            contenido += "La nueva contrasena para su usuario: " + user.username + "\n"
            contenido += "es: " + password
            correo = EmailMessage(titulo, contenido, to=['andelnunez@gmail.com'])
            try:
                correo.send()
                mensaje = "Email enviado"
                mensajeCorreo = "Se le ha enviado un correo con su nueva contrasena"
                user.set_password(password)
                user.save()
                return render_to_response('iniciarSesion.html', {'formulario':formulario,'mensajeCorreo':mensajeCorreo}, context_instance=RequestContext(request))
            except:
                mensaje= 'Error enviando email'
                mensajeErrorCorreo = "Ha ocurrido un error. Favor intente de nuevo"
                return render_to_response('iniciarSesion.html', {'formulario':formulario,'mensajeErrorCorreo':mensajeErrorCorreo}, context_instance=RequestContext(request))


    else:
        formulario = AuthenticationForm()
    return render_to_response('iniciarSesion.html', {'formulario':formulario}, context_instance=RequestContext(request))

def estadoPostulacion(request):
    user = request.user
    estudiante = Estudiante.objects.get(user=user)
    print estudiante.estadoPostulacion
    return render_to_response('estudiante/estadoPostulacion.html', {'estudiante':estudiante}, context_instance=RequestContext(request))

def perfilEstudianteUSB(request):
    user = request.user
    estudiante = Estudiante.objects.get(user=user)
    if request.method == 'POST':
        formulario = EstudianteUSB_Edit_Form(request.POST)
        if formulario.is_valid():
            nombre1 = formulario.cleaned_data['nombre1']
            nombre2 = formulario.cleaned_data['nombre2']
            apellido1 = formulario.cleaned_data['apellido1']
            apellido2 = formulario.cleaned_data['apellido2']
            email = formulario.cleaned_data['email']
            carnet = formulario.cleaned_data['carnet']
            username = formulario.cleaned_data['username']

            if user.username != username:
                aux = User.objects.filter(username=username)
                if len(aux) != 0:
                    UsuarioRepetido = "El nombre de usuario ya existe **"
                    return render_to_response('estudiante/perfilEstudiante.html', {'formulario': formulario,'UsuarioRepetido':UsuarioRepetido},context_instance=RequestContext(request))

            if formulario.cleaned_data['cambiarContra']:
                contrasena1 = formulario.cleaned_data['contrasena1']
                contrasena2 = formulario.cleaned_data['contrasena2']

                if contrasena1 != contrasena2:
                    ContrasenaDist = "Las contrasenas deben coincidir **"
                    return render_to_response('estudiante/perfilEstudiante.html', {'formulario': formulario,'ContrasenaDist':ContrasenaDist},context_instance=RequestContext(request))
                user.set_password(contrasena1)

            user.username = username
            user.email = email
            estudiante.nombre1 = nombre1
            estudiante.nombre2 = nombre2
            estudiante.apellido1 = apellido1
            estudiante.apellido2 = apellido2
            estudiante.carnet = carnet

            user.save()
            estudiante.save()

            return render_to_response('index.html', context_instance=RequestContext(request))
    else:
        formulario = EstudianteUSB_Edit_Form(initial={'nombre1':estudiante.nombre1,'nombre2':estudiante.nombre2,'apellido1':estudiante.apellido1,'apellido2':estudiante.apellido2,
                                                'email':user.email,'carnet':estudiante.carnet,'username':user.username})
    return render_to_response('estudiante/perfilEstudiante.html', {'formulario':formulario},context_instance=RequestContext(request))

def perfilEstudianteExt(request):
    user = request.user
    estudiante = Estudiante.objects.get(user=user)
    if request.method == 'POST':
        formulario = EstudianteExt_Edit_Form(request.POST)
        if formulario.is_valid():
            nombre1 = formulario.cleaned_data['nombre1']
            nombre2 = formulario.cleaned_data['nombre2']
            apellido1 = formulario.cleaned_data['apellido1']
            apellido2 = formulario.cleaned_data['apellido2']
            email = formulario.cleaned_data['email']
            pasaporte = formulario.cleaned_data['pasaporte']
            username = formulario.cleaned_data['username']

            if user.username != username:
                aux = User.objects.filter(username=username)
                if len(aux) != 0:
                    UsuarioRepetido = "El nombre de usuario ya existe **"
                    return render_to_response('estudiante/perfilEstudiante.html', {'formulario': formulario,'UsuarioRepetido':UsuarioRepetido},context_instance=RequestContext(request))

            if formulario.cleaned_data['cambiarContra']:
                contrasena1 = formulario.cleaned_data['contrasena1']
                contrasena2 = formulario.cleaned_data['contrasena2']

                if contrasena1 != contrasena2:
                    ContrasenaDist = "Las contrasenas deben coincidir **"
                    return render_to_response('estudiante/perfilEstudiante.html', {'formulario': formulario,'ContrasenaDist':ContrasenaDist},context_instance=RequestContext(request))
                user.set_password(contrasena1)

            user.username = username
            user.email = email
            estudiante.nombre1 = nombre1
            estudiante.nombre2 = nombre2
            estudiante.apellido1 = apellido1
            estudiante.apellido2 = apellido2
            estudiante.pasaporte = pasaporte

            user.save()
            estudiante.save()

            return render_to_response('index.html', context_instance=RequestContext(request))
    else:
        formulario = EstudianteExt_Edit_Form(initial={'nombre1':estudiante.nombre1,'nombre2':estudiante.nombre2,'apellido1':estudiante.apellido1,'apellido2':estudiante.apellido2,
                                                'email':user.email,'pasaporte':estudiante.pasaporte,'username':user.username})
    return render_to_response('estudiante/perfilEstudiante.html', {'formulario':formulario},context_instance=RequestContext(request))

def postularse(request):
    estudiante = Estudiante.objects.get(user=request.user)
    if estudiante.estadoPostulacion != "Sin postular":
        yaPostulado = True
    else:
        yaPostulado = False
    return render_to_response('estudiante/postularse.html',{'yaPostulado':yaPostulado},context_instance=RequestContext(request))

def formularioUNO(request):
    estudiante = Estudiante.objects.get(user=request.user)
    if request.method == 'POST':
        if estudiante.estudUsb:
            formulario = formularioUNO_formUSB(request.POST)
            if formulario.is_valid():
                genero = formulario.cleaned_data['genero']
                nacionalidad = formulario.cleaned_data['nacionalidad']
                cedula = formulario.cleaned_data['cedula']
                estudiante.nacionalidad = nacionalidad
                estudiante.cedula = cedula
                estudiante.sexo = genero
                estudiante.save()
        else:
            formulario = formularioUNO_formExt(request.POST)
            if formulario.is_valid():
                genero = formulario.cleaned_data['genero']
                nacionalidad = formulario.cleaned_data['nacionalidad']
                estudiante.nacionalidad = nacionalidad
                estudiante.sexo = genero
                estudiante.save()

    else:
        if estudiante.estudUsb:
            formulario = formularioUNO_formUSB(initial={'nombre1':estudiante.nombre1,'nombre2':estudiante.nombre2,'apellido1':estudiante.apellido1,
                                                        'apellido2':estudiante.apellido2,'carnet':estudiante.carnet})
        else:
            formulario = formularioUNO_formExt(initial={'nombre1':estudiante.nombre1,'nombre2':estudiante.nombre2,'apellido1':estudiante.apellido1,
                                                        'apellido2':estudiante.apellido2,'pasaporte':estudiante.pasaporte})
    return render_to_response('estudiante/formularioUNO.html',{'formulario':formulario,'estudiante':estudiante},context_instance=RequestContext(request))