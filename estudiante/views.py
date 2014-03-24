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
            carrera = formulario.cleaned_data['carrera']

            aux = User.objects.filter(username=username)
            if len(aux) != 0:
                UsuarioRepetido = "El nombre de usuario ya existe **"
                return render_to_response('estudiante/registrarEstudianteUSB.html', {'formulario': formulario,'UsuarioRepetido':UsuarioRepetido},context_instance=RequestContext(request))

            if contrasena1 != contrasena2:
                ContrasenaDist = "Las contrasenas deben coincidir **"
                return render_to_response('estudiante/registrarEstudianteUSB.html', {'formulario': formulario,'ContrasenaDist':ContrasenaDist},context_instance=RequestContext(request))

            user = User.objects.create_user(username,email,contrasena1)
            user.first_name = "estudianteUSB"
            estudiante = Estudiante.objects.create(user=user,nombre1=nombre1,nombre2=nombre2,apellido1=apellido1,apellido2=apellido2,email=email,carnet=carnet,estudUsb=True,carrera_usb=carrera)
            user.save()
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
    print 'esta postulado' + estudiante.estadoPostulacion
    if estudiante.estadoPostulacion != 'Sin postular':
        print 'true'
        yaPostulado = True
    else:
        yaPostulado = False
        print 'false'
    return render_to_response('estudiante/postularse.html',{'yaPostulado':yaPostulado},context_instance=RequestContext(request))

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
                estudiante.nacionalidad = nacionalidad
                estudiante.cedula = cedula
                estudiante.sexo = genero
                estudiante.save()

                return HttpResponseRedirect('/formularioDOS')
        ## Si se trata de un estudiante Extranjero
        else:
            formulario = formularioUNO_formExt(request.POST)
            if formulario.is_valid():
                genero = formulario.cleaned_data['genero']
                nacionalidad = formulario.cleaned_data['nacionalidad']
                estudiante.nacionalidad = nacionalidad
                estudiante.sexo = genero
                estudiante.save()

                return HttpResponseRedirect('/formularioDOS')
    else:
        if estudiante.estudUsb:
            formulario = formularioUNO_formUSB(initial={'nombre1':estudiante.nombre1,'nombre2':estudiante.nombre2,'apellido1':estudiante.apellido1,
                                                        'apellido2':estudiante.apellido2,'carnet':estudiante.carnet,'genero':estudiante.sexo,
                                                        'nacionalidad':estudiante.nacionalidad,'cedula':estudiante.cedula})
        else:
            formulario = formularioUNO_formExt(initial={'nombre1':estudiante.nombre1,'nombre2':estudiante.nombre2,'apellido1':estudiante.apellido1,
                                                        'apellido2':estudiante.apellido2,'pasaporte':estudiante.pasaporte,'genero':estudiante.sexo,
                                                        'nacionalidad':estudiante.nacionalidad})
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
        if 'atras' in request.POST:
            return HttpResponseRedirect('/formularioTRES')
        if 'siguiente' in request.POST:
            return HttpResponseRedirect('/formularioCINCO')
    else:
        if estudiante.estudUsb:
            formulario = formularioCUATRO_formUSB()
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
                    antecedente = AntecedenteAcad.objects.create(indice=indice,creditosAprobados=creditos,anoIngreso='08',anosAprob='20')
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
            formulario = formularioCINCO_formExt()
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
            estudiante.save()
            if 'atras' in request.POST:
                return HttpResponseRedirect('/formularioSEIS')
            if 'siguiente' in request.POST:
                return HttpResponseRedirect('/postularse')
    else:
        if estudiante.representante == None:
            formulario = formularioSIETE_form()
        else:
            formulario = formularioSIETE_form(initial={'apellidos':estudiante.representante.apellido,'nombres':estudiante.representante.nombre,
                                                       'cel':estudiante.representante.telefCel,'tel_casa':estudiante.representante.telefCasa,
                                                       'email':estudiante.representante.email,'rel_estudiante':estudiante.representante.tipoRelacion,
                                                       'direccion':estudiante.representante.direccion})
    return render_to_response('estudiante/formularioSIETE.html',{'formulario':formulario,'estudiante':estudiante},context_instance=RequestContext(request))
