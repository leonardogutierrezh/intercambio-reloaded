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

def descargarPlanilla(request):
    estudiante = Estudiante.objects.get(user=request.user)
    if estudiante.primerPaso and estudiante.segundoPaso and  estudiante.tercerPaso and estudiante.cuartoPaso:
        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Planilla Postulacion.pdf"'

        # Create the PDF object, using the response object as its "file."
        p = canvas.Canvas(response)

        p.setFont("Helvetica",11)
        p.drawString( 68, 690, "FORMULARIO DE POSTULACION AL PROGRAMA DE INTERCAMBIO DE ESTUDIANTES ")
        p.setFont("Helvetica",10)
        p.drawString( 70, 660, "DATOS PERSONALES ")
        p.setFont("Helvetica",8)
        if estudiante.nombre2 != None:
            p.drawString( 70, 630, "- Nombre completo: " + estudiante.nombre1 + estudiante.nombre2 + estudiante.apellido1 + estudiante.apellido2)
        else:
            p.drawString( 70, 630, "- Nombre completo: " + estudiante.nombre1 + estudiante.apellido1 + estudiante.apellido2)
        p.drawString( 70, 610, "- Genero: " + estudiante.sexo )
        p.drawString( 320, 610, "- Fecha de nacimiento: " + estudiante.fechaNacimiento )
        p.drawString( 70, 590, "- Email: " + request.user.email)
        p.drawString( 320, 590, "- Nacionalidad: " + estudiante.nacionalidad.printable_name)
        p.drawString( 70, 570, "- Cedula de identidad: " + str(estudiante.cedula))
        p.drawString( 320, 570, "- Tlf. Celular: " + str(estudiante.telfCel) )
        if estudiante.estudUsb:
            p.drawString( 70, 550, "- Carne estudiantil USB: " + estudiante.carnet)
        else:
            p.drawString( 70, 550, "- Carne estudiantil USB: ")
        p.drawString( 320, 550, "- Tlf. Habitacion: " + str(estudiante.telfCasa))
        p.drawString( 70, 530, "- Domicilio actual: ")

        p.drawString( 90, 520, "- Urb/Sector/Barrio: " + estudiante.urbanizacion)
        p.drawString( 320, 520, "- Nombre (Edificio|Casa): " + estudiante.edificio)
        p.drawString( 90, 500, "- Calle: " + estudiante.calle)
        p.drawString( 320, 500, "- Apartamento|Nro.Casa: " + estudiante.apartamento)
        p.drawString( 90, 480, "- Ciudad: ")
        p.drawString( 320, 480, "- Estado: " )
        p.drawString( 90, 460, "- Codigo postal: " + estudiante.codigopostal )

        p.setFont("Helvetica",11)
        p.drawString( 68, 400, "IDENTIFICACION DEL PROGRAMA Y LAPSO DE ESTUDIO EN INTERCAMBIO:")
        p.drawString( 80, 375, "Primera opcion " )
        p.drawString( 78, 373, "_____________" )

        p.setFont("Helvetica",8)
        p.drawString( 70, 350, "- Pais destino: " )
        p.drawString( 310, 350, "- Duracion del programa: " )
        p.drawString( 70, 330, "- Tipo de programa: " )
        p.drawString( 70, 310, "- Nombre de la universidad destino: " )
        p.drawString( 70, 290, "- Nombre del programa: " )
        p.drawString( 70, 270, "- Fechas tentativas de inicio y fin (segun calendario de la universidad de destino): " )
        p.drawString( 90, 260, "Inicio: ")
        p.drawString( 250, 260, "Fin: ")

        p.setFont("Helvetica",11)
        p.drawString( 80, 230, "Segunda opcion " )
        p.drawString( 78, 228, "______________" )
        p.setFont("Helvetica",8)
        p.drawString( 70, 205, "- Pais destino: " )
        p.drawString( 310, 205, "- Duracion del programa: " )
        p.drawString( 70, 185, "- Tipo de programa: " )
        p.drawString( 70, 165, "- Nombre de la universidad destino: " )
        p.drawString( 70, 145, "- Nombre del programa: " )
        p.drawString( 70, 125, "- Fechas tentativas de inicio y fin (segun calendario de la universidad de destino): " )
        p.drawString( 90, 115, "Inicio: ")
        p.drawString( 250, 115, "Fin: ")


        p.rect(50,450,6.8*inch,3.2*inch)
        p.rect(50,80,6.8*inch,4.8*inch)

        p.drawInlineImage("./intercambio/static/img/cebollaUSB.jpg", 110, 770, 0.8*inch, 0.5*inch)
        p.setFont("Helvetica",7)
        p.drawString( 90, 755, "UNIVERSIDAD SIMON BOLIVAR")
        p.drawString( 120, 745, "RECTORADO")
        p.drawString( 60, 735, "Direccion de relaciones internacionales y de cooperacion")
        p.drawString( 283, 745, "Coordinacion de apoyo a los programas de intercambio")
        p.drawString( 330, 735, "Programa de intercambio de estudiantes")

        p.showPage()

        if estudiante.estudUsb:
            ## Segunda pagina
            p.setFont("Helvetica",11)
            p.drawString( 68, 770, "INFORMACION ACADEMICA:")
            p.setFont("Helvetica",8)
            p.drawString( 70, 740, "Nro de creditos aprobados a la fecha de postulacion: " + str(estudiante.antecedente.creditosAprobados))
            p.drawString( 320, 740, "Decanato: " + estudiante.carrera_usb.decanato)
            p.drawString( 70, 720, "Carrera que estudia en la universidad: " + estudiante.carrera_usb.nombre)
            p.drawString( 70, 700, "Area de estudio: " + estudiante.carrera_usb.areaDeEstudio)
            p.drawString( 320, 700, "Indice academico a la fecha de postulacion: " + str(estudiante.antecedente.indice))
            p.setFont("Helvetica",10)
            p.drawString( 70, 670, "Asignaturas del Plan de Estudio USB que aspira " )
            p.drawString( 70, 660, "sean convalidadas u otorgadas en equivalencia " )
            p.drawString( 320, 670, "Asignaturas a cursar en la Universidad de  " )
            p.drawString( 320, 660, "Destino " )
            p.rect(50,470,6.8*inch,3*inch)
            p.drawString( 60, 640, "Codigo  " )
            p.drawString( 135, 640, "Denominacion  " )
            p.drawString( 250, 640, "Creditos  " )
            p.drawString( 305, 640, "Codigo  " )
            p.drawString( 380, 640, "Denominacion  " )
            p.drawString( 495, 640, "Creditos  " )
            p.rect(50,470,3.4*inch,3*inch)
            p.rect(50,630,6.8*inch,20)
            p.rect(50,470,55,180)
            p.rect(240,470,55,180)      #Cuadro de denominacion a credito USB
            p.rect(295,470,55,180)       #Cuadro de codigo a denominacion Ext
            p.rect(485,470,55,180)      #Cuadro de denominacion a credito Ext
            p.setFont("Helvetica",8)
            y=620
            for plan in estudiante.planDeEstudio.all():
                p.drawString( 55, y, plan.materiaUsb.codigo )
                p.drawString( 110, y, plan.materiaUsb.nombre )
                p.drawString( 250, y, str(plan.materiaUsb.creditos) )
                p.drawString( 300, y, plan.codigoUniv )
                p.drawString( 355, y, plan.nombreMateriaUniv )
                p.drawString( 495, y, str(plan.creditosUniv) )
                y = y - 10
            p.drawString( 100, 435, "Aprobacion coordinacion carrera:               ________________________________  " )
            p.rect(50,420,6.8*inch,375)      #Cuadro completo informacion academica
        else:
            ## Segunda pagina
            p.setFont("Helvetica",11)
            p.drawString( 68, 750, "INFORMACION ACADEMICA:")
            p.setFont("Helvetica",8)
            p.drawString( 70, 720, "Nro de creditos aprobados a la fecha de postulacion: " )
            p.drawString( 320, 720, "Decanato: " )
            p.drawString( 70, 700, "Carrera que estudia en la universidad: " )
            p.drawString( 70, 680, "Area de estudio: " )
            p.drawString( 320, 680, "Indice academico a la fecha de postulacion: " )
            p.setFont("Helvetica",10)
            p.drawString( 70, 650, "Asignaturas del Plan de Estudio USB que aspira " )
            p.drawString( 70, 640, "sean convalidadas u otorgadas en equivalencia: " )
            p.drawString( 320, 650, "Asignaturas a cursar en la Universidad de  " )
            p.drawString( 320, 640, "Destino " )
            p.rect(50,450,6.8*inch,3*inch)
            p.drawString( 60, 620, "Codigo  " )
            p.drawString( 135, 620, "Denominacion  " )
            p.drawString( 250, 620, "Creditos  " )
            p.drawString( 305, 620, "Codigo  " )
            p.drawString( 380, 620, "Denominacion  " )
            p.drawString( 495, 620, "Creditos  " )
            p.rect(50,450,3.4*inch,3*inch)
            p.rect(50,610,6.8*inch,20)
            p.rect(50,450,55,180)
            p.rect(240,450,55,180)      #Cuadro de denominacion a credito USB
            p.rect(295,450,55,180)       #Cuadro de codigo a denominacion Ext
            p.rect(485,450,55,180)      #Cuadro de denominacion a credito Ext
            p.drawString( 100, 435, "Aprobacion coordinacion carrera:               ________________________________  " )
            p.rect(50,420,6.8*inch,375)      #Cuadro completo informacion academica

        p.setFont("Helvetica",11)
        p.drawString( 68, 390, "FUENTE DE FINANCIAMIENTO DEL ESTUDIANTE" )
        p.setFont("Helvetica",8)
        p.drawString( 70, 370, "- Principal fuente de ingresos: " + estudiante.financiamiento.fuente )
        p.drawString( 320, 370, "- Otros: " + estudiante.financiamiento.descripcionFuente)
        p.drawString( 70, 350, "- Recibe ayuda economica por: " )
        if estudiante.financiamiento.ayuda:
            p.drawString( 70, 340, "parte de la universidad u otro organismo?: Si")
        else:
            p.drawString( 70, 340, "parte de la universidad u otro organismo?: No")
        p.drawString( 320, 350, "- Especifique: " + estudiante.financiamiento.descripcionAyuda)
        p.rect(50,320,6.8*inch,95)      #Cuadro completo de fuente financiamiento

        p.setFont("Helvetica",11)
        p.drawString( 68, 300, "CONOCIMIENTO DE IDIOMAS" )
        p.setFont("Helvetica",10)
        p.drawString( 60, 280, "Idioma a emplear  " )
        p.drawString( 270, 280, "Verbal  " )
        p.drawString( 360, 280, "Escrito  " )
        p.drawString( 460, 280, "Auditivo  " )
        p.rect(50,170,6.8*inch,145)      #Cuadro completo de conocimiento idiomas
        p.rect(50,270,6.8*inch,23)
        p.rect(50,170,190,123)
        p.rect(240,170,90,123)
        p.rect(240,170,195,123)
        y = 260
        p.setFont("Helvetica",8)
        for idioma in estudiante.idiomas.all():
            p.drawString( 60, y, idioma.idioma.nombre )
            p.drawString( 250, y, idioma.verbal)
            p.drawString( 340, y, idioma.escrito)
            p.drawString( 445, y, idioma.auditivo)
            y = y-10

        p.setFont("Helvetica",11)
        p.drawString( 68, 150, "DATOS DE CONTACTO EN CASO DE EMERGENCIA" )
        p.setFont("Helvetica",8)
        p.drawString( 70, 130, "- Nombre contacto: " + estudiante.representante.nombre + " " + estudiante.representante.apellido)
        p.drawString( 70, 110, "- Tlf. Habitacion contacto: " + str(estudiante.representante.telefCasa))
        p.drawString( 70, 90, "- Relacion con el estudiante: " + estudiante.representante.tipoRelacion)
        p.drawString( 70, 70, "- Domicilio contacto: " + estudiante.representante.direccion)
        p.rect(50,50,6.8*inch,115)      #Cuadro completo de contacto emergencia
        p.showPage()

        ## Proxima pagina
        p.setFont("Helvetica",8)
        p.drawString( 100, 690, "Firma del solicitante: ____________________ ")
        p.drawString( 320, 690, "Fecha del solicitud: ")
        p.setFont("Helvetica",7)
        p.drawString( 140, 660, "El estudiante firmante declara que los datos y documentos suministrados son veridicos y asume cumplir ")
        p.drawString( 190, 650, "cabalmente con las normas del programa de intercambio estudiantil.")
        p.rect(50,610,6.8*inch,2*inch)

        p.setFont("Helvetica",11)
        p.drawString( 100, 560, "**Esta seccion debe ser llenada exclusivamente por la coordinacion docente**")
        p.drawString( 110, 510, "Opinion de la coordinacion Docente sobre esta solicitud (explicacion breve):")
        p.setFont("Helvetica",8)
        p.drawString( 70, 475, "Muy favorable: " )
        p.drawString( 70, 455, "Favorable: " )
        p.drawString( 70, 435, "Con reservas: " )
        p.rect(50,415,6.8*inch,1.7*inch)
        p.showPage()
        p.save()

        return response
    else:
        return render_to_response('estudiante/noPostuladoAun.html',{},context_instance=RequestContext(request))

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

