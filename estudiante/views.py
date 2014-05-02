#coding: utf-8
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
from countries.models import *
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage, EmailMultiAlternatives
import os, random, string
from django.template.loader import render_to_string
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Image
from django.core import serializers
from administrador.models import Universidad, Log
from postulante.models import Postulacion

def index(request):
    return render_to_response('index.html', context_instance=RequestContext(request))

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
            carrera = formulario.cleaned_data['carrera']

            aux = User.objects.filter(username=username)
            if len(aux) != 0:
                UsuarioRepetido = "El nombre de usuario ya existe **"
                return render_to_response('estudiante/registrarEstudianteUSB.html', {'formulario': formulario,'UsuarioRepetido':UsuarioRepetido},context_instance=RequestContext(request))

            if contrasena1 != contrasena2:
                ContrasenaDist = "Las contrasenas deben coincidir **"
                return render_to_response('estudiante/registrarEstudianteUSB.html', {'formulario': formulario,'ContrasenaDist':ContrasenaDist},context_instance=RequestContext(request))

            nacionalidad = Country.objects.get(iso='VE')

            user = User.objects.create_user(username,email,contrasena1)
            user.first_name = "estudianteUSB"
            estudiante = Estudiante.objects.create(user=user,nombre1=nombre1,nombre2=nombre2,apellido1=apellido1,apellido2=apellido2,email=email,carnet=carnet,estudUsb=True,carrera_usb=carrera,nacionalidad=nacionalidad)
            user.save()
            estudiante.save()

            postulacion = Postulacion.objects.create(username=estudiante,estadoPostulacion='Sin postular')
            postulacion.save()

            log = Log.objects.create(suceso = "Nuevo usuario creado",usuario = user)
            log.save()
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

            postulacion = Postulacion.objects.create(username=estudiante,estadoPostulacion='Sin postular')
            postulacion.save()
            log = Log.objects.create(suceso = "Nuevo usuario creado",usuario = user)
            log.save()
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
                    print 'hice login'
                    return HttpResponseRedirect('/index')
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
    postulacion = Postulacion.objects.get(username=estudiante)

    print postulacion.estadoPostulacion
    return render_to_response('estudiante/estadoPostulacion.html', {'estudiante':estudiante,'postulacion':postulacion}, context_instance=RequestContext(request))

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
            carrera = formulario.cleaned_data['carrera']

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
            estudiante.carrera_usb = carrera

            user.save()
            estudiante.save()
            return render_to_response('index.html', {'perfilEstudianteCambiado':True}, context_instance=RequestContext(request))
    else:
        formulario = EstudianteUSB_Edit_Form(initial={'nombre1':estudiante.nombre1,'nombre2':estudiante.nombre2,'apellido1':estudiante.apellido1,'apellido2':estudiante.apellido2,
                                                'email':user.email,'carnet':estudiante.carnet,'username':user.username,
                                                'carrera':estudiante.carrera_usb})
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
    postulacion = Postulacion.objects.get(username=estudiante)
    if postulacion.estadoPostulacion != 'Sin postular':
        yaPostulado = True
    else:
        yaPostulado = False
    return render_to_response('estudiante/postularse.html',{'yaPostulado':yaPostulado,'estudiante':estudiante},context_instance=RequestContext(request))

def formularioUNO(request):
    estudiante = Estudiante.objects.get(user=request.user)
    if request.method == 'POST':
        ## Si se trata de un estudianteUSB
        if estudiante.estudUsb:
            formulario = formularioUNO_formUSB(request.POST)
            if formulario.is_valid():
                genero = formulario.cleaned_data['genero']
                nacionalidad = formulario.cleaned_data['nacionalidad']
                cedula = formulario.cleaned_data['cedula']
                fecha = formulario.cleaned_data['fecha']
                estudiante.nacionalidad = nacionalidad
                estudiante.cedula = cedula
                estudiante.sexo = genero
                estudiante.fechaNacimiento = fecha
                estudiante.save()

                return HttpResponseRedirect('/formularioDOS')
        ## Si se trata de un estudiante Extranjero
        else:
            formulario = formularioUNO_formExt(request.POST)
            if formulario.is_valid():
                genero = formulario.cleaned_data['genero']
                nacionalidad = formulario.cleaned_data['nacionalidad']
                fecha = formulario.cleaned_data['fecha']
                estudiante.nacionalidad = nacionalidad
                estudiante.sexo = genero
                estudiante.fechaNacimiento = fecha
                estudiante.save()

                return HttpResponseRedirect('/formularioDOS')
    else:
        if estudiante.estudUsb:
            formulario = formularioUNO_formUSB(initial={'nombre1':estudiante.nombre1,'nombre2':estudiante.nombre2,'apellido1':estudiante.apellido1,
                                                        'apellido2':estudiante.apellido2,'carnet':estudiante.carnet,'genero':estudiante.sexo,
                                                        'nacionalidad':estudiante.nacionalidad,'cedula':estudiante.cedula,'fecha':estudiante.fechaNacimiento})
        else:
            formulario = formularioUNO_formExt(initial={'nombre1':estudiante.nombre1,'nombre2':estudiante.nombre2,'apellido1':estudiante.apellido1,
                                                        'apellido2':estudiante.apellido2,'pasaporte':estudiante.pasaporte,'genero':estudiante.sexo,
                                                        'nacionalidad':estudiante.nacionalidad,'fecha':estudiante.fechaNacimiento})
    return render_to_response('estudiante/formularioUNO.html',{'formulario':formulario,'estudiante':estudiante},context_instance=RequestContext(request))

def formularioDOS(request):
    estudiante = Estudiante.objects.get(user=request.user)
    if request.method == 'POST':
        formulario = formularioDOS_form(request.POST)
        if formulario.is_valid():
            urbanizacion = formulario.cleaned_data['urbanizacion']
            calle = formulario.cleaned_data['calle']
            edificio = formulario.cleaned_data['edificio']
            apartamento = formulario.cleaned_data['apartamento']
            codigopostal = formulario.cleaned_data['codigo_postal']

            estudiante.urbanizacion = urbanizacion
            estudiante.calle = calle
            estudiante.edificio = edificio
            estudiante.apartamento = apartamento
            estudiante.codigopostal = codigopostal
            estudiante.save()

            if 'atras' in request.POST:
                return HttpResponseRedirect('/formularioUNO')
            if 'siguiente' in request.POST:
                return HttpResponseRedirect('/formularioTRES')
    else:
        formulario = formularioDOS_form(initial={'urbanizacion':estudiante.urbanizacion,'calle':estudiante.calle,'edificio':estudiante.edificio,'apartamento':estudiante.apartamento,
                                                        'codigo_postal':estudiante.codigopostal})
    return render_to_response('estudiante/formularioDOS.html',{'formulario':formulario,'estudiante':estudiante},context_instance=RequestContext(request))

def formularioTRES(request):
    estudiante = Estudiante.objects.get(user=request.user)
    if request.method == 'POST':
        formulario = formularioTRES_form(request.POST)
        if formulario.is_valid():
            cel = formulario.cleaned_data['cel']
            tel_casa = formulario.cleaned_data['tel_casa']

            estudiante.telfCel = cel
            estudiante.telfCasa = tel_casa
            estudiante.save()

            if 'atras' in request.POST:
                return HttpResponseRedirect('/formularioDOS')
            if 'siguiente' in request.POST:
                return HttpResponseRedirect('/formularioCUATRO')
    else:
        formulario = formularioTRES_form(initial={'cel':estudiante.telfCel,'tel_casa':estudiante.telfCasa,'email':request.user.email})
    return render_to_response('estudiante/formularioTRES.html',{'formulario':formulario,'estudiante':estudiante},context_instance=RequestContext(request))

def formularioCUATRO(request):
    estudiante = Estudiante.objects.get(user=request.user)

    if request.method == 'POST':
        if estudiante.estudUsb:
            formulario = formularioCUATRO_formUSB(request.POST)
            if formulario.is_valid():

                prog1 = formulario.cleaned_data['programaUno']
                uni1 = request.POST.get('uni1')
                tipoProgramaUno = formulario.cleaned_data['tipoProgramaUno']
                fechaInicioUno = formulario.cleaned_data['fechaInicioUno']
                anoInicioUno = formulario.cleaned_data['anoInicioUno']
                fechaFinUno = formulario.cleaned_data['fechaFinUno']
                anoFinUno = formulario.cleaned_data['anoFinUno']
                duracionUno = formulario.cleaned_data['duracionUno']

                prog2 = formulario.cleaned_data['programaDos']
                uni2 = request.POST.get('uni2')
                tipoProgramaDos = formulario.cleaned_data['tipoProgramaDos']
                fechaInicioDos = formulario.cleaned_data['fechaInicioDos']
                anoInicioDos = formulario.cleaned_data['anoInicioDos']
                fechaFinDos = formulario.cleaned_data['fechaFinDos']
                anoFinDos = formulario.cleaned_data['anoFinDos']
                duracionDos = formulario.cleaned_data['duracionDos']


                if estudiante.primeraOpcion == None:
                    universidad = Universidad.objects.get(id=int(uni1))
                    primeraOpcion = OpcionUNO.objects.create(programa=prog1,univ=universidad,
                                                            tipoPrograma=tipoProgramaUno,fechaInicio=fechaInicioUno,anoInicio=anoInicioUno,
                                                            fechaFin=fechaFinUno,anoFin=anoFinUno,duracion=duracionUno)
                    primeraOpcion.save()
                    universidad = Universidad.objects.get(id=int(uni2))
                    segundaOpcion = OpcionDOS.objects.create(programa=prog2,univ=universidad,
                                                            tipoPrograma=tipoProgramaDos,fechaInicio=fechaInicioDos,anoInicio=anoInicioDos,
                                                            fechaFin=fechaFinDos,anoFin=anoFinDos,duracion=duracionDos)
                    segundaOpcion.save()
                    estudiante.primeraOpcion = primeraOpcion
                    estudiante.segundaOpcion = segundaOpcion
                else:
                    universidad = Universidad.objects.get(id=int(uni1))
                    estudiante.primeraOpcion.programa = prog1
                    estudiante.primeraOpcion.univ = universidad
                    estudiante.primeraOpcion.tipoPrograma = tipoProgramaUno
                    estudiante.primeraOpcion.fechaInicio = fechaInicioUno
                    estudiante.primeraOpcion.anoInicio = anoInicioUno
                    estudiante.primeraOpcion.fechaFin = fechaFinUno
                    estudiante.primeraOpcion.anoFin = anoFinUno
                    estudiante.primeraOpcion.duracion = duracionUno
                    estudiante.primeraOpcion.save()
                    estudiante.segundaOpcion.programa = prog2
                    universidad = Universidad.objects.get(id=int(uni2))
                    estudiante.segundaOpcion.univ = universidad
                    estudiante.segundaOpcion.tipoPrograma = tipoProgramaDos
                    estudiante.segundaOpcion.fechaInicio = fechaInicioDos
                    estudiante.segundaOpcion.anoInicio = anoInicioDos
                    estudiante.segundaOpcion.fechaFin = fechaFinDos
                    estudiante.segundaOpcion.anoFin = anoFinDos
                    estudiante.segundaOpcion.duracion = duracionDos
                    estudiante.segundaOpcion.save()
                estudiante.save()

                if 'atras' in request.POST:
                    return HttpResponseRedirect('/formularioTRES')
                if 'siguiente' in request.POST:
                    return HttpResponseRedirect('/formularioCINCO')
        else:
            formulario = formularioCUATRO_formExt(request.POST)
            if 'atras' in request.POST:
                return HttpResponseRedirect('/formularioTRES')
            if 'siguiente' in request.POST:
                return HttpResponseRedirect('/formularioCINCO')
    else:
        if estudiante.estudUsb:
            if estudiante.primeraOpcion == None:
                formulario = formularioCUATRO_formUSB()
            else:
                formulario = formularioCUATRO_formUSB(initial={'programaUno':estudiante.primeraOpcion.programa,'tipoProgramaUno':estudiante.primeraOpcion.tipoPrograma,
                                                               'fechaInicioUno':estudiante.primeraOpcion.fechaInicio,
                                                               'anoInicioUno':estudiante.primeraOpcion.anoInicio,
                                                               'fechaFinUno':estudiante.primeraOpcion.fechaFin,
                                                               'anoFinUno':estudiante.primeraOpcion.anoFin,
                                                               'duracionUno':estudiante.primeraOpcion.duracion,
                                                               'programaDos':estudiante.segundaOpcion.programa,'tipoProgramaDos':estudiante.segundaOpcion.tipoPrograma,
                                                               'fechaInicioDos':estudiante.segundaOpcion.fechaInicio,
                                                               'anoInicioDos':estudiante.segundaOpcion.anoInicio,
                                                               'fechaFinDos':estudiante.segundaOpcion.fechaFin,
                                                               'anoFinDos':estudiante.segundaOpcion.anoFin,
                                                               'duracionDos':estudiante.segundaOpcion.duracion})
                hayOpcion = True
                universidades1 = Universidad.objects.filter(programa = estudiante.primeraOpcion.programa)
                paises1 = []
                for uni in universidades1:
                    if not(uni.pais in paises1):
                        paises1.append(uni.pais)
                universidades2 = Universidad.objects.filter(programa = estudiante.segundaOpcion.programa)
                paises2 = []
                for uni in universidades2:
                    if not(uni.pais in paises2):
                        paises2.append(uni.pais)
                return render_to_response('estudiante/formularioCUATRO.html',{'formulario':formulario,'estudiante':estudiante,'hayOpcion':hayOpcion,'universidades1':universidades1,'paises1':paises1,'universidades2':universidades2,'paises2':paises2},context_instance=RequestContext(request))
        else:
            formulario = formularioCUATRO_formExt()
    return render_to_response('estudiante/formularioCUATRO.html',{'formulario':formulario,'estudiante':estudiante},context_instance=RequestContext(request))

def formularioCINCO(request):
    estudiante = Estudiante.objects.get(user=request.user)
    if request.method == 'POST':
        if estudiante.estudUsb:
            formulario = formularioCINCO_formUSB(request.POST)
            if formulario.is_valid():
                indice = formulario.cleaned_data['indice']
                creditos = formulario.cleaned_data['creditos']

                if estudiante.antecedente == None:
                    antecedente = AntecedenteAcad.objects.create(indice=indice,creditosAprobados=creditos,anoIngreso=0,anosAprob=0)
                    antecedente.save()
                    estudiante.antecedente = antecedente
                else:
                    estudiante.antecedente.indice = indice
                    estudiante.antecedente.creditosAprobados = creditos
                    estudiante.antecedente.save()
                estudiante.save()

                if 'atras' in request.POST:
                    return HttpResponseRedirect('/formularioCUATRO')
                if 'siguiente' in request.POST:
                    return HttpResponseRedirect('/formularioSEIS')
        else:
            formulario = formularioCINCO_formExt(request.POST)
            if formulario.is_valid():
                anoIngreso = formulario.cleaned_data['anoIngreso']
                anosAprob = formulario.cleaned_data['anosAprob']

                if estudiante.antecedente == None:
                    antecedente = AntecedenteAcad.objects.create(indice=0,creditosAprobados=0,anoIngreso=anoIngreso,anosAprob=anosAprob)
                    antecedente.save()
                    estudiante.antecedente = antecedente
                else:
                    estudiante.antecedente.anoIngreso = anoIngreso
                    estudiante.antecedente.anosAprob = anosAprob
                    estudiante.antecedente.save()
                estudiante.save()

                if 'atras' in request.POST:
                    return HttpResponseRedirect('/formularioCUATRO')
                if 'siguiente' in request.POST:
                    return HttpResponseRedirect('/formularioSEIS')
    else:
        if estudiante.estudUsb:
            if estudiante.antecedente == None:
                formulario = formularioCINCO_formUSB(initial={'carrera':estudiante.carrera_usb})
            else:
                formulario = formularioCINCO_formUSB(initial={'carrera':estudiante.carrera_usb,'indice':estudiante.antecedente.indice,'creditos':estudiante.antecedente.creditosAprobados})
        else:
            if estudiante.antecedente == None:
                formulario = formularioCINCO_formExt()
            else:
                formulario = formularioCINCO_formExt(initial={'anoIngreso':estudiante.antecedente.anoIngreso,'anosAprob':estudiante.antecedente.anosAprob})
    return render_to_response('estudiante/formularioCINCO.html',{'formulario':formulario,'estudiante':estudiante},context_instance=RequestContext(request))

def formularioSEIS(request):
    estudiante = Estudiante.objects.get(user=request.user)
    if request.method == 'POST':
        formulario = formularioSEIS_form(request.POST)
        if formulario.is_valid():
            fuente_ingreso = formulario.cleaned_data['fuente_ingreso']
            detalle_fuente = formulario.cleaned_data['detalle_fuente']
            ayuda = formulario.cleaned_data['ayuda']
            detalle_ayuda = formulario.cleaned_data['detalle_ayuda']

            if estudiante.financiamiento == None:
                financiamiento = Financiamiento.objects.create(fuente=fuente_ingreso,descripcionFuente=detalle_fuente,ayuda=ayuda,descripcionAyuda=detalle_ayuda)
                financiamiento.save()
                estudiante.financiamiento = financiamiento
            else:
                estudiante.financiamiento.fuente = fuente_ingreso
                estudiante.financiamiento.descripcionFuente = detalle_fuente
                estudiante.financiamiento.ayuda = ayuda
                estudiante.financiamiento.descripcionAyuda = detalle_ayuda
                estudiante.financiamiento.save()
            estudiante.save()

            if 'atras' in request.POST:
                return HttpResponseRedirect('/formularioCINCO')
            if 'siguiente' in request.POST:
                return HttpResponseRedirect('/formularioSIETE')
    else:
        if estudiante.financiamiento == None:
            formulario = formularioSEIS_form()
        else:
            formulario = formularioSEIS_form(initial={'fuente_ingreso':estudiante.financiamiento.fuente,'detalle_fuente':estudiante.financiamiento.descripcionFuente,
                                                      'ayuda':estudiante.financiamiento.ayuda,'detalle_ayuda':estudiante.financiamiento.descripcionAyuda})
    return render_to_response('estudiante/formularioSEIS.html',{'formulario':formulario,'estudiante':estudiante},context_instance=RequestContext(request))

def formularioSIETE(request):
    estudiante = Estudiante.objects.get(user=request.user)
    if request.method == 'POST':
        formulario = formularioSIETE_form(request.POST)
        if formulario.is_valid():
            apellidos = formulario.cleaned_data['apellidos']
            nombres = formulario.cleaned_data['nombres']
            cel = formulario.cleaned_data['cel']
            tel_casa = formulario.cleaned_data['tel_casa']
            email = formulario.cleaned_data['email']
            rel_estudiante = formulario.cleaned_data['rel_estudiante']
            direccion = formulario.cleaned_data['direccion']

            representante = Representante.objects.create(apellido=apellidos,nombre=nombres,telefCasa=tel_casa,telefCel=cel,email=email,tipoRelacion=rel_estudiante,direccion=direccion)
            representante.save()

            estudiante.representante = representante
            estudiante.primerPaso = True

            if estudiante.primerPaso and estudiante.segundoPaso and estudiante.tercerPaso and estudiante.cuartoPaso:
                postulacion = Postulacion.objects.get(username=estudiante)
                if postulacion.estadoPostulacion == 'Sin postular':
                    postulacion.estadoPostulacion = 'Postulado'
                    postulacion.save()
                    log = Log.objects.create(suceso = "Usuario se postula al intercambio",usuario = request.user)
                    log.save()

            estudiante.save()
            if 'atras' in request.POST:
                return HttpResponseRedirect('/formularioSEIS')
            if 'siguiente' in request.POST:
                if estudiante.primerPaso and estudiante.segundoPaso and estudiante.tercerPaso and estudiante.cuartoPaso:
                    return HttpResponseRedirect('/postularse')
                else:
                    return HttpResponseRedirect('/documentosRequeridos')
    else:
        if estudiante.representante == None:
            formulario = formularioSIETE_form()
        else:
            formulario = formularioSIETE_form(initial={'apellidos':estudiante.representante.apellido,'nombres':estudiante.representante.nombre,
                                                       'cel':estudiante.representante.telefCel,'tel_casa':estudiante.representante.telefCasa,
                                                       'email':estudiante.representante.email,'rel_estudiante':estudiante.representante.tipoRelacion,
                                                       'direccion':estudiante.representante.direccion})
    return render_to_response('estudiante/formularioSIETE.html',{'formulario':formulario,'estudiante':estudiante},context_instance=RequestContext(request))

def documentosRequeridos(request):
    estudiante = Estudiante.objects.get(user=request.user)
    if request.method == 'POST':
        if estudiante.estudUsb:
            formulario = documentosRequeridosUSB_form(request.POST,request.FILES)
            if estudiante.documentos == None:
                if formulario.is_valid():
                    foto = formulario.cleaned_data['foto']
                    informe = formulario.cleaned_data['informe']
                    carta = formulario.cleaned_data['carta']
                    planilla = formulario.cleaned_data['planilla']
                    certificado = formulario.cleaned_data['certificado']

                    if estudiante.documentos == None:
                        doc = DocumentosRequeridos.objects.create(foto=foto,informe=informe,carta=carta,planilla=planilla,certificado=certificado)
                        doc.save()
                        estudiante.documentos = doc
                    else:
                        estudiante.documentos.foto = foto
                        estudiante.documentos.informe = informe
                        estudiante.documentos.carta = carta
                        estudiante.documentos.planilla = planilla
                        estudiante.documentos.certificado = certificado
                        estudiante.documentos.save()

                    estudiante.segundoPaso = True
                    if estudiante.primerPaso and estudiante.segundoPaso and estudiante.tercerPaso and estudiante.cuartoPaso:
                        postulacion = Postulacion.objects.get(username=estudiante)
                        if postulacion.estadoPostulacion == 'Sin postular':
                            postulacion.estadoPostulacion = 'Postulado'
                            postulacion.save()
                            log = Log.objects.create(suceso = "Usuario se postula al intercambio",usuario = request.user)
                            log.save()

                    estudiante.save()

                    if estudiante.primerPaso and estudiante.segundoPaso and estudiante.tercerPaso and estudiante.cuartoPaso:
                        return HttpResponseRedirect('/postularse')
                    else:
                        return HttpResponseRedirect('/planEstudio')
            else:
                foto = formulario.cleaned_data['foto']
                informe = formulario.cleaned_data['informe']
                carta = formulario.cleaned_data['carta']
                planilla = formulario.cleaned_data['planilla']
                certificado = formulario.cleaned_data['certificado']

                if estudiante.documentos == None:
                    doc = DocumentosRequeridos.objects.create(foto=foto,informe=informe,carta=carta,planilla=planilla,certificado=certificado)
                    doc.save()
                    estudiante.documentos = doc
                else:
                    estudiante.documentos.foto = foto
                    estudiante.documentos.informe = informe
                    estudiante.documentos.carta = carta
                    estudiante.documentos.planilla = planilla
                    estudiante.documentos.certificado = certificado
                    estudiante.documentos.save()

                estudiante.segundoPaso = True
                if estudiante.primerPaso and estudiante.segundoPaso and estudiante.tercerPaso and estudiante.cuartoPaso:
                    postulacion = Postulacion.objects.get(username=estudiante)
                    if postulacion.estadoPostulacion == 'Sin postular':
                        postulacion.estadoPostulacion = 'Postulado'
                        postulacion.save()
                        log = Log.objects.create(suceso = "Usuario se postula al intercambio",usuario = request.user)
                        log.save()

                estudiante.save()

                if estudiante.primerPaso and estudiante.segundoPaso and estudiante.tercerPaso and estudiante.cuartoPaso:
                    return HttpResponseRedirect('/postularse')
                else:
                    return HttpResponseRedirect('/planEstudio')
        else:
            formulario = documentosRequeridosExt_form(request.POST,request.FILES)
    else:
        if estudiante.estudUsb:
            if estudiante.documentos == None:
                formulario = documentosRequeridosUSB_form()
            else:
                formulario =  documentosRequeridosUSB_form(initial={'foto':estudiante.documentos.foto,'informe':estudiante.documentos.informe,
                                                                    'carta':estudiante.documentos.carta,'planilla':estudiante.documentos.planilla,
                                                                    'certificado':estudiante.documentos.certificado})
        else:
            formulario = documentosRequeridosExt_form()
    return render_to_response('estudiante/documentosRequeridos.html',{'formulario':formulario,'estudiante':estudiante},context_instance=RequestContext(request))

def planEstudio(request):
    estudiante = Estudiante.objects.get(user=request.user)
    materias = MateriaUSB.objects.all()
    if request.method == 'POST':
        if len(estudiante.planDeEstudio.all()) != 0:
            for planEst in estudiante.planDeEstudio.all():
                planEst.delete()
            estudiante.tercerPaso = False
        lista_materias = request.POST.getlist('lista_materias')
        contador = int(request.POST.get('count'))

        aux = 0
        num = 0

        for lista in lista_materias:
            materia = MateriaUSB.objects.get(id=int(lista))
            ## Encontrando el numero de fila fila
            check = 'check_' + str(aux)
            if not(request.POST.get(check)):
                existe = True
                while existe:
                    aux = aux + 1
                    check = 'check_' + str(aux)
                    if request.POST.get(check):
                        existe = False
            cod_destino = "cod_des_" + str(aux)
            nom_destino = "nom_des_" + str(aux)
            cred_destino = "cred_des_" + str(aux)

            codigoUniv = request.POST.get(cod_destino)
            nombreMateriaUniv = request.POST.get(nom_destino)
            creditosUniv = int(request.POST.get(cred_destino))

            plan = PlanDeEstudio.objects.create(materiaUsb = materia, codigoUniv=codigoUniv, nombreMateriaUniv=nombreMateriaUniv, creditosUniv=creditosUniv, auxiliar =num)
            plan.save()
            estudiante.planDeEstudio.add(plan)
            num = num + 1
            aux = aux + 1

            estudiante.tercerPaso = True

        if estudiante.primerPaso and estudiante.segundoPaso and estudiante.tercerPaso and estudiante.cuartoPaso:
            postulacion = Postulacion.objects.get(username=estudiante)
            if postulacion.estadoPostulacion == 'Sin postular':
                postulacion.estadoPostulacion = 'Postulado'
                postulacion.save()
                log = Log.objects.create(suceso = "Usuario se postula al intercambio",usuario = request.user)
                log.save()

        estudiante.save()

        if estudiante.primerPaso and estudiante.segundoPaso and estudiante.tercerPaso and estudiante.cuartoPaso:
            return  HttpResponseRedirect('/postularse')
        else:
            return HttpResponseRedirect('/dominioIdiomas')
    if len(estudiante.planDeEstudio.all()) == 0:
        hayPlan = False
    else:
        hayPlan = True
    return render_to_response('estudiante/planEstudio.html',{'materias':materias,'estudiante':estudiante,'hayPlan':hayPlan,'tamano':len(estudiante.planDeEstudio.all())-1},context_instance=RequestContext(request))

def dominioIdiomas(request):
    estudiante = Estudiante.objects.get(user=request.user)
    idiomas = Idioma.objects.all()
    if request.method == 'POST':
        if len(estudiante.idiomas.all()) != 0:
            for idioma in estudiante.idiomas.all():
                idioma.delete()
            estudiante.cuartoPaso = False

        lista_idiomas = request.POST.getlist('lista_idiomas')
        contador = int(request.POST.get('count'))

        aux = 0
        num = 0

        for lista in lista_idiomas:
            print 'id ', lista
            idioma = Idioma.objects.get(id=int(lista))
            ## Encontrando el numero de fila fila
            check = 'check_' + str(aux)
            if not(request.POST.get(check)):
                existe = True
                while existe:
                    aux = aux + 1
                    check = 'check_' + str(aux)
                    if request.POST.get(check):
                        existe = False
            verbal = "verbal_" + str(aux)
            escrito = "escrito_" + str(aux)
            auditivo = "auditivo_" + str(aux)

            verbal_idioma = request.POST.get(verbal)
            escrito_idioma = request.POST.get(escrito)
            auditivo_idioma = request.POST.get(auditivo)

            domIdioma = ManejoIdiomas.objects.create(idioma=idioma,verbal=verbal_idioma,escrito=escrito_idioma,auditivo=auditivo_idioma,auxiliar=num)
            domIdioma.save()
            estudiante.idiomas.add(domIdioma)
            num = num + 1
            aux = aux + 1

            estudiante.cuartoPaso = True

        if estudiante.primerPaso and estudiante.segundoPaso and estudiante.tercerPaso and estudiante.cuartoPaso:
            postulacion = Postulacion.objects.get(username=estudiante)
            if postulacion.estadoPostulacion == 'Sin postular':
                postulacion.estadoPostulacion = 'Postulado'
                postulacion.save()
                log = Log.objects.create(suceso = "Usuario se postula al intercambio",usuario = request.user)
                log.save()


        estudiante.save()

        return  HttpResponseRedirect('/postularse')

    tam = len(estudiante.idiomas.all())
    if tam == 0:
        hayIdioma = False
    else:
        hayIdioma = True
    return render_to_response('estudiante/dominioIdiomas.html',{'estudiante':estudiante,'idiomas':idiomas,'hayIdioma':hayIdioma,'tamano':tam-1},context_instance=RequestContext(request))

def descargar(request):
    estudiante = Estudiante.objects.get(user=request.user)
    # if not(estudiante.primerPaso and estudiante.segundoPaso and estudiante.tercerPaso and estudiante.cuartoPaso):
    #    return render_to_response('estudiante/noPostuladoAun.html',context_instance=RequestContext(request))

def ajaxConvenio(request):
    modo = request.GET['modo']
    if modo == 'convenio':
        id_convenio = request.GET['id']
        universidades = Universidad.objects.filter(programa__id=id_convenio)
        paises = []
        for uni in universidades:
            if not(uni.pais in paises):
                paises.append(uni.pais)
        data = serializers.serialize('json',paises,fields=('printable_name','name'))
        return HttpResponse(data,mimetype='application/json')
    if modo == 'pais':
        id_pais = request.GET['name']
        pais =Country.objects.get(iso=id_pais)
        universidades = Universidad.objects.filter(pais=pais)
        data = serializers.serialize('json',universidades,fields=('nombre'))
        return HttpResponse(data,mimetype='application/json')

def ajaxConvenioPais(request):
    id_pais = request.GET['name']
    pais =Country.objects.get(iso=id_pais)
    universidades = Universidad.objects.filter(pais=pais)
    data = serializers.serialize('json',universidades,fields=('nombre'))
    return HttpResponse(data,mimetype='application/json')

def nombreMaterias(request):
    id_materia = request.GET['id']
    materia = MateriaUSB.objects.filter(id=int(id_materia))
    data = serializers.serialize('json',materia,fields=('creditos','nombre'))
    return HttpResponse(data,mimetype='application/json')

def descargarPlanilla(request):
    estudiante = Estudiante.objects.get(user=request.user)
    if estudiante.primerPaso and estudiante.segundoPaso and  estudiante.tercerPaso and estudiante.cuartoPaso:
        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Planilla Postulacion.pdf"'

        # Create the PDF object, using the response object as its "file."
        p = canvas.Canvas(response)

        p.drawInlineImage("./intercambio/static/img/cebollaUSB.jpg", 110, 780, 0.8*inch, 0.5*inch)
        p.setFont("Helvetica",11)
        p.drawString( 60, 765, "UNIVERSIDAD SIMON BOLIVAR")

        p.setFont("Helvetica",7)
        p.drawString( 283, 785, "Dirección de Relaciones Internacionales y de Cooperación")
        p.drawString( 291, 775, "Coordinación de Apoyo a los Programas de Intercambio ")
        p.drawString( 338, 765, "Programa de Intercambio de Estudiantes")

        p.setFont("Helvetica",11)
        p.drawString( 70, 745, "SOLICITUD DE INCORPORACIÓN AL PROGRAMA DE INTERCAMBIO DE ESTUDIANTES")

        p.setFont("Helvetica",9)
        p.drawString( 65, 720, "DATOS PERSONALES:")
        p.setFont("Helvetica",7)
        p.drawString(60,710,"1.")
        p.drawString(80,710,"Apellidos:")
        p.drawString(80,690,"__________________________________________")
        if estudiante.apellido2 != None:
            p.drawString(80,695,estudiante.apellido1 + " " + estudiante.apellido2)
        else:
            p.drawString(80,795,estudiante.apellido1 )
        p.drawString(310,710,"Nombres:")
        p.drawString(310,690,"____________________________________________")
        if estudiante.nombre2 != None:
            p.drawString(310,695,estudiante.nombre1 + " " + estudiante.nombre2)
        else:
            p.drawString(310,695,estudiante.nombre1 )
        p.rect(50,685,6.8*inch,50)                                  #Cuadro
        p.drawString(60,670,"2.")
        p.drawString(80,670,"Género:")
        p.drawString(110,660,"F _____ ")
        p.drawString(140,660,"M _____ ")
        if estudiante.sexo == 'femenino':
            p.drawString(120,660," X ")
        else:
            p.drawString(150,660," X ")
        p.drawString(300,670,"7.")
        p.drawString(320,670,"Domicilio Actual:")
        p.drawString(320,660,"____________________________________________")
        p.drawString(320,650,"____________________________________________")
        p.drawString(320,640,"____________________________________________")
        p.drawString(320,630,"____________________________________________")

        p.drawString(320,660,"Urb: " + estudiante.urbanizacion)
        p.drawString(320,650,"Calle: " + estudiante.calle)
        p.drawString(320,640,"Nombre (Edificio/Casa): " + estudiante.edificio)
        p.drawString(320,630,"Apartamento/Nro.Casa: " + estudiante.apartamento + " Cod.Postal: " + estudiante.codigopostal)
        p.drawString(60,640,"3.")
        p.drawString(80,640,"Nacionalidad:")
        p.drawString(80,630,"_______________________________________")
        p.drawString(80,630,estudiante.nacionalidad.printable_name)
        p.drawString(60,610,"4.")
        p.drawString(80,610,"Número de Cédula de Identidad:")
        p.drawString(80,600,"_______________________________________")
        p.drawString(300,610,"8.")
        p.drawString(320,610,"Datos de Contacto:")
        p.drawString(320,590,"Telf. Hab: ______________________________________")
        p.drawString(360,590,str(estudiante.telfCasa))
        p.drawString(320,570,"Telf. Cel: ______________________________________")
        p.drawString(360,570,str(estudiante.telfCel))
        p.drawString(320,550,"E-mail: ________________________________________")
        p.drawString(360,550,request.user.email)
        p.drawString(80,600,str(estudiante.cedula))
        p.drawString(60,580,"5.")
        p.drawString(80,580,"N° Carnet Estudiantil USB:")
        p.drawString(80,570,"_______________________________________")
        p.drawString(60,550,"6.")
        p.drawString(80,550,"N° Pasaporte vigente:")
        p.drawString(80,540,"_______________________________________")

        p.rect(50,520,240,165)                                  #Cuadro segundo izquierdo
        p.rect(290,520,250,165)                                  #Cuadro segundo derecho

        p.drawString(60,500,"9.")
        p.drawString(80,500,"Datos de una persona a contactar en caso de emergencias:")
        p.drawString(80,490,"Apellidos y Nombres: ___________________________________________________________________________________________")
        p.drawString(160,490,estudiante.representante.nombre + " " + estudiante.representante.apellido)
        p.drawString(80,470,"Relación con el estudiante: ______________________________________________________________________________________")
        p.drawString(180,470,estudiante.representante.tipoRelacion)
        p.drawString(80,450,"Direccion: ____________________________________________________________________________________________________")
        p.drawString(120,450, estudiante.representante.direccion)
        p.drawString(80,430,"Teléfonos: ________________________________________")
        p.drawString(120,430, str(estudiante.representante.telefCasa) + " / " + str(estudiante.representante.telefCel))
        p.drawString(290,430,"E-mail: ________________________________________________")
        p.drawString(320,430, estudiante.representante.email)

        p.rect(50,425,6.8*inch,95)                                  #Cuadro

        p.drawString(60,410,"10.")
        p.drawString(80,410," Idioma a emplear en la universidad destino: ")
        p.drawString(60,390,"11.")
        p.drawString(80,390," Nivel de suficiencia del idioma a emplear verbal y escrito: ")

        p.drawString(80,370," Oral: ")
        p.drawString(150,370," Básico: _______ ")
        p.drawString(250,370," Intermedio: _______ ")
        p.drawString(370,370," Avanzado: _______ ")

        p.drawString(80,360," Escrito: ")
        p.drawString(150,360," Básico: _______ ")
        p.drawString(250,360," Intermedio: _______ ")
        p.drawString(370,360," Avanzado: _______ ")

        p.drawString(80,350," Lectura: ")
        p.drawString(150,350," Básico: _______ ")
        p.drawString(250,350," Intermedio: _______ ")
        p.drawString(370,350," Avanzado: _______ ")

        p.rect(50,340,6.8*inch,85)                                  #Cuadro

        p.drawString(50,330,"Documentos que deben acompañar a esta solicitud: ")
        p.drawString(50,310,"- Curriculum Vitae que resuma sus actividades académicas, profesionales, de extensión universitaria y desarrollo personal (etapa universitaria).")
        p.drawString(50,300,"- Fotocopia de cedula y carnet USB.")
        p.drawString(50,290,"- Informe académico actualizado emitido por la Dirección de Admisión y Control de Estudios (DACE), y flujograma de asignaturas ya cursadas.")
        p.drawString(50,280,"- Comprobante de Inscripción del trimestre en curso. ")
        p.drawString(50,270,"- Carta de motivación para cursar estudios en la universidad seleccionada, dirigida al el/la Coordinador (a) Docente de la carrera respectiva.")
        p.drawString(50,260,"- Flujograma de asignaturas cursadas hasta la fecha de postulación; asignaturas pendientes por cursar antes de iniciar el Programa de Intercambio y asignaturas ")
        p.drawString(50,250,"que cursaría en la USB una vez regrese a Venezuela al finalizar el Intercambio. ")
        p.drawString(50,240,"- Certificados de estudios de lengua extranjera en caso de postularse a una universidad no hispanohablante (ver Normas de Intercambio, Artículo 7, parágrafo D). ")
        p.drawString(50,230,"- Fotocopia de las constancias que respalden el contenido del Currículum Vitae (Solo etapa universitaria). ")
        p.drawString(50,220,"- Programas sinópticos de las asignaturas a cursar en la universidad de destino.")

        p.setFont("Helvetica",9)
        p.drawString(65, 200, "IDENTIFICACIÓN DEL PROGRAMA, ACTIVIDAD ACADÉMICA Y LAPSO DE ESTUDIO EN INTERCAMBIO ")
        p.setFont("Helvetica",7)
        p.drawString(60,190,"12.")
        p.drawString(80,190," País: _________________________________________")
        p.drawString(110,190,estudiante.primeraOpcion.univ.pais.printable_name)
        p.drawString(60,170,"13.")
        p.drawString(80,170," Universidad de Destino: _________________________________________")
        p.drawString(170,170,estudiante.primeraOpcion.univ.nombre)
        p.drawString(60,150,"14.")
        p.drawString(80,150," Nombre del Programa: ")
        p.drawString(160,150,"Convenio Bilateral: _______")
        p.drawString(260,150,"Programa SMILE: _______")
        p.drawString(360,150,"Programa de Movilidad Estudiantil CINDA: _______")

        if estudiante.primeraOpcion.programa.nombre == 'Convenio Bilateral':
            p.drawString(230,150," X ")
        if estudiante.primeraOpcion.programa.nombre == 'Programa SMILE':
            p.drawString(325,150," X ")
        if estudiante.primeraOpcion.programa.nombre == 'Programa de Movilidad Estudiantil CINDA':
            p.drawString(495,150," X ")

        p.drawString(60,130,"15.")
        p.drawString(80,130," Actividad Académica: ")
        p.drawString(160,130,"Solo Asignaturas: _____")
        p.drawString(245,130,"Asignaturas + Proyecto de Grado: _____")
        p.drawString(380,130,"Asignaturas + Pasantía Internacional: _____")

        p.drawString(60,110,"16.")
        p.drawString(80,110," Fechas tentativas de Inicio y Fin, según calendario de la Universidad de Destino:")
        p.drawString(180,100,"INICIO:________________________")
        p.drawString(210,100,estudiante.primeraOpcion.fechaInicio + " " + estudiante.primeraOpcion.anoInicio)
        p.drawString(360,100,"FIN:___________________________")
        p.drawString(390,100,estudiante.primeraOpcion.fechaFin + " " + estudiante.primeraOpcion.anoFin)

        p.rect(50,80,6.8*inch,135)                                  #Cuadro

        p.drawString(280,60,"Página 1 de 2")
        p.showPage()

        ## SEGUNDA PAGINA
        p.setFont("Helvetica",9)
        p.drawString(65, 810, "INFORMACIÓN ACADÉMICA ")
        p.setFont("Helvetica",7)

        p.drawString(60,800,"17.")
        p.drawString(80,800," Carrera que estudia en la USB:")
        p.drawString(80,780,"_______________________________________")
        if estudiante.estudUsb:
            p.drawString(90,780,estudiante.carrera_usb.nombre)
        p.drawString(300,800,"18.")
        p.drawString(320,800," Mención (en caso que aplique):")
        p.drawString(320,780,"_______________________________________")
        p.drawString(60,760,"19.")
        p.drawString(80,760," N° de créditos aprobados a la fecha: :")
        p.drawString(80,745,"_______________________________________")
        p.drawString(90,745,str(estudiante.antecedente.creditosAprobados))
        p.drawString(300,760,"20.")
        p.drawString(320,760," Índice académico a la fecha: ")
        p.drawString(320,745,"_______________________________________")
        p.drawString(330,745,str(estudiante.antecedente.indice))

        p.rect(50,735,6.8*inch,90)                                  #Cuadro

        p.drawString( 70, 720, "Asignaturas del Plan de Estudio USB que aspira " )
        p.drawString( 70, 710, "sean convalidadas u otorgadas en equivalencia " )
        p.drawString( 320, 720, "Asignaturas a cursar en la Universidad de  " )
        p.drawString( 320, 710, "Destino " )
        p.rect(50,520,6.8*inch,3*inch)
        p.drawString( 60, 690, "Codigo  " )
        p.drawString( 135, 690, "Denominacion  " )
        p.drawString( 250, 690, "Creditos  " )
        p.drawString( 305, 690, "Codigo  " )
        p.drawString( 380, 690, "Denominacion  " )
        p.drawString( 495, 690, "Creditos  " )
        p.rect(50,520,3.4*inch,3*inch)
        p.rect(50,680,6.8*inch,20)
        p.rect(50,520,55,180)
        p.rect(240,520,55,180)      #Cuadro de denominacion a credito USB
        p.rect(295,520,55,180)       #Cuadro de codigo a denominacion Ext
        p.rect(485,520,55,180)      #Cuadro de denominacion a credito Ext
        p.setFont("Helvetica",8)
        y=670
        for plan in estudiante.planDeEstudio.all():
            p.drawString( 55, y, plan.materiaUsb.codigo )
            p.drawString( 110, y, plan.materiaUsb.nombre )
            p.drawString( 250, y, str(plan.materiaUsb.creditos) )
            p.drawString( 300, y, plan.codigoUniv )
            p.drawString( 355, y, plan.nombreMateriaUniv )
            p.drawString( 495, y, str(plan.creditosUniv) )
            y = y - 10
        p.setFont("Helvetica",6.5)
        p.drawString(50,510,"Nota: De acuerdo a las Normas del Pr ogr am a d e In t er c ambi o d e Es tud ian tes , los participantes en dicho programa deben cursar al menos un trimestre en la")
        p.drawString(50,500,"USB al regresar del I ntercambio. La presentación y defensa de la Pasantía Larga o Proyectos de Grado debe ajustarse a la \"Normativa para aceptación y evaluación")
        p.drawString(50,490,"de los trabajos de grado y pasantías largas de los estudiantes de Intercambio de la Universidad Simón Bolívar\" y la publicación del documento debe ajustarse a las")
        p.drawString(50,480,"normas de presentación de Proyectos de Grado establecidas por la Coordinación Docente de Carrera respectiva")

        p.setFont("Helvetica",8)
        p.drawString(50,450,"Firma del Solicitante:  _________________________________")
        p.drawString(300,450,"Fecha de la Solicitud: : __________/__________/__________")

        p.setFont("Helvetica",8)
        p.drawString(65, 420, "EN CASO DE NO SER ACEPTADO EN LA UNIVERSIDAD SELECCIONADA FAVOR INDIQUE UNA SEGUNDA OPCIÓN ")
        p.setFont("Helvetica",7)
        p.drawString(60,410,"23.")
        p.drawString(80,410," País: _________________________________________")
        p.drawString(110,410,estudiante.segundaOpcion.univ.pais.printable_name)
        p.drawString(60,390,"24.")
        p.drawString(80,390," Universidad de Destino: _________________________________________")
        p.drawString(170,390,estudiante.segundaOpcion.univ.nombre)
        p.drawString(60,370,"25.")
        p.drawString(80,370," Nombre del Programa: ")
        p.drawString(160,370,"Convenio Bilateral: _______")
        p.drawString(260,370,"Programa SMILE: _______")
        p.drawString(360,370,"Programa de Movilidad Estudiantil CINDA: _______")

        if estudiante.segundaOpcion.programa.nombre == 'Convenio Bilateral':
            p.drawString(230,370," X ")
        if estudiante.segundaOpcion.programa.nombre == 'Programa SMILE':
            p.drawString(325,370," X ")
        if estudiante.segundaOpcion.programa.nombre == 'Programa de Movilidad Estudiantil CINDA':
            p.drawString(495,370," X ")

        p.drawString(60,350,"26.")
        p.drawString(80,350," Actividad Académica: ")
        p.drawString(160,350,"Solo Asignaturas: _____")
        p.drawString(245,350,"Asignaturas + Proyecto de Grado: _____")
        p.drawString(380,350,"Asignaturas + Pasantía Internacional: _____")

        p.drawString(60,330,"27.")
        p.drawString(80,330," Fechas tentativas de Inicio y Fin, según calendario de la Universidad de Destino:")
        p.drawString(180,320,"INICIO:________________________")
        p.drawString(210,320,estudiante.segundaOpcion.fechaInicio + " " + estudiante.segundaOpcion.anoInicio)
        p.drawString(360,320,"FIN:___________________________")
        p.drawString(390,320,estudiante.segundaOpcion.fechaFin + " " + estudiante.segundaOpcion.anoFin)

        p.rect(50,300,6.8*inch,135)                                  #Cuadro

        p.setFont("Helvetica",8)
        p.drawString( 130, 270, "**Esta sección debe ser llenada exclusivamente por la Coordinación Docente de Carrera*")
        p.drawString( 150, 260, "Opinión de la Coordinación Docente de Carrera sobre esta solicitud: ")
        p.setFont("Helvetica",7)
        p.drawString( 70, 240, "Muy favorable: ____________ " )
        p.drawString( 230, 240, "Favorable: _______________" )
        p.drawString( 400, 240, "Con reservas: ________________" )
        p.drawString( 70, 220, "______________________________________________________________________________________________________________________ " )
        p.drawString( 70, 200, "______________________________________________________________________________________________________________________ " )
        p.drawString( 70, 180, "______________________________________________________________________________________________________________________ " )
        p.drawString( 70, 150, "Índice normalizado: _____________ " )
        p.drawString( 70, 130, "Firma y Sello de la Coordinación Docente de Carrera: _____________________ " )

        p.drawString(280,60,"Página 2 de 2")

        p.showPage()
        p.save()

        return response
    else:
        return render_to_response('estudiante/noPostuladoAun.html',{},context_instance=RequestContext(request))
