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
from postulante.models import *
from countries.models import *
from gestor.models import *
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
#from postulante.forms import *
from gestor.forms import *
from django.db.models import Q

def perfilDecanato(request):
    user = request.user
    gestor = Gestor.objects.get(usuario=user)
    if request.method == 'POST':
        formulario = Gestor_Edit_Form(request.POST)
        if formulario.is_valid():
            username = formulario.cleaned_data['username']
            nombre = formulario.cleaned_data['nombre']

            if user.username != username:
                aux = User.objects.filter(username=username)
                if len(aux) != 0:
                    UsuarioRepetido = "El nombre de usuario ya existe **"
                    return render_to_response('postulante/perfilPostulante.html', {'formulario': formulario,'UsuarioRepetido':UsuarioRepetido},context_instance=RequestContext(request))
            if formulario.cleaned_data['cambiarContra']:
                contrasena1 = formulario.cleaned_data['contrasena1']
                contrasena2 = formulario.cleaned_data['contrasena2']

                if contrasena1 != contrasena2:
                    ContrasenaDist = "Las contrasenas deben coincidir **"
                    return render_to_response('postulante/perfilPostulante.html', {'formulario': formulario,'ContrasenaDist':ContrasenaDist},context_instance=RequestContext(request))
                user.set_password(contrasena1)
            user.username = username
            gestor.nombre = nombre
            user.save()
            gestor.save()

            return render_to_response('index.html', {'perfilGestorCambiado':True},context_instance=RequestContext(request))
    else:
        formulario = Gestor_Edit_Form(initial={'username':user.username,'nombre':gestor.nombre})
    return render_to_response('gestor/verPerfilGestor.html', {'formulario':formulario},context_instance=RequestContext(request))

def cargarIndices(request):
    user = request.user
    gestor = Gestor.objects.get(usuario=user)
    carreras = CarreraUsb.objects.all()
    indicesCargados = False
    if request.method == 'POST':
        print 'post'
        listaIndices = request.POST.getlist('listaIndices')
        for lista in listaIndices:
            carrera = CarreraUsb.objects.get(id=int(lista))
            indice = request.POST.get(lista)
            carrera.indiceCarrera = indice
            carrera.save()
        indicesCargados = True
    return render_to_response('gestor/cargarIndices.html', {'carreras':carreras,'indicesCargados':indicesCargados},context_instance=RequestContext(request))

@login_required(login_url='/')
def decanato_ver_log(request):
    log = Log.objects.all().order_by('fecha')
    return render_to_response('gestor/log.html', {'log': log}, context_instance=RequestContext(request))

@login_required(login_url='/')
def ver_tabla_postulados(request, opcion):
    lista = []
    postulados = Postulacion.objects.filter(Q(estadoPostulacion='Postulado. Revisado por coordinación') | Q(estadoPostulacion__contains='Aceptado'))
    uni_aux = "&&&&&&"
    if opcion == '1':
        for postulado in postulados:
            if UniversidadAsignada.objects.filter(nombreEstud=postulado.username, nombreUniv=postulado.username.primeraOpcion.univ):
                existe=1
            elif UniversidadAsignada.objects.filter(nombreEstud=postulado.username, nombreUniv=postulado.username.segundaOpcion.univ):
                existe=3
            else:
                existe=0
            if postulado.username.primeraOpcion.univ.nombre == uni_aux:
                lista.append((postulado, postulado.username.primeraOpcion.univ, "estudiante",existe))
            else:
                lista.append((postulado, postulado.username.primeraOpcion.univ, "universidad",existe))
                lista.append((postulado, postulado.username.primeraOpcion.univ, "estudiante",existe))
                uni_aux = postulado.username.primeraOpcion.univ.nombre
    elif opcion == '2':
        for postulado in postulados:
            if UniversidadAsignada.objects.filter(nombreEstud=postulado.username, nombreUniv=postulado.username.segundaOpcion.univ):
                existe=1
            elif UniversidadAsignada.objects.filter(nombreEstud=postulado.username, nombreUniv=postulado.username.primeraOpcion.univ):
                existe=3
            else:
                existe=0
            if postulado.username.segundaOpcion.univ.nombre == uni_aux:
                lista.append((postulado, postulado.username.segundaOpcion.univ, "estudiante",existe))
            else:
                lista.append((postulado, postulado.username.segundaOpcion.univ, "universidad",existe))
                lista.append((postulado, postulado.username.segundaOpcion.univ, "estudiante",existe))
                uni_aux = postulado.username.segundaOpcion.univ.nombre
    else:
        print 3
    return render_to_response('gestor/ver_tabla_postulados.html', {'lista': lista, 'opcion': opcion}, context_instance=RequestContext(request))

def verDetallePostulacionDRIC(request,id_user):
    estudiante = Estudiante.objects.get(id=int(id_user))
    postulacion = Postulacion.objects.get(username=estudiante)
    return render_to_response('postulante/verDetallePostulacion.html', {'estudiante':estudiante,'postulacion':postulacion},context_instance=RequestContext(request))

def ajax_aceptar_postulado(request):
    estudiante = Estudiante.objects.get(id=request.GET['id_estudiante'])
    universidad = Universidad.objects.get(id=request.GET['id_universidad'])
    if universidad.cupo > 0:
        if UniversidadAsignada.objects.filter(nombreEstud=estudiante):
            old = UniversidadAsignada.objects.get(nombreEstud=estudiante)
            if  old.nombreUniv == universidad:
                return False
            else:
                print "entre bien"
                old_uni = old.nombreUniv
                old.delete()
                old_uni.cupo = old_uni.cupo + 1
                old_uni.save()
                universidad.cupo = universidad.cupo - 1
                universidad.save()
                asignada_aux = UniversidadAsignada.objects.create(nombreEstud=estudiante, nombreUniv=universidad)
        else:
            universidad.cupo = universidad.cupo - 1
            universidad.save()
            asignada_aux = UniversidadAsignada.objects.create(nombreEstud=estudiante, nombreUniv=universidad)
        asignada = []
        asignada.append(asignada_aux)
        postulacion = Postulacion.objects.get(username=estudiante)
        postulacion.estadoPostulacion = "Aceptado en " + universidad.nombre
        postulacion.save()
        estudiante.user.last_name = 'aceptado'
        estudiante.user.save()
        data = serializers.serialize('json', asignada, fields =('nombreEstud', 'nombreUniv'))
        asunto = "Sistema de Gestion de Intercambio"
        mensaje = "Hola ya tiene universidad asignada para su intercambio por favor ingrese al sistema para mas informacion sobre su postulacion. \n"
        #correo = EmailMessage(asunto, mensaje, to=['contacto@asuntopais.com'])
        correo = EmailMessage(asunto, mensaje, to=[estudiante.email])
        try:
            print "enviando"
            #correo.send()
        except:
            mensaje="error al enviar el mensaje"
        return HttpResponse(data, mimetype='application/json')
    else:
        return False

def ajax_deshacer_postulado(request):
    estudiante = Estudiante.objects.get(id=request.GET['id_estudiante'])
    universidad = Universidad.objects.get(id=request.GET['id_universidad'])
    if UniversidadAsignada.objects.filter(nombreEstud=estudiante):
        old = UniversidadAsignada.objects.get(nombreEstud=estudiante).delete()
        universidad.cupo =universidad.cupo + 1
        universidad.save()
    asignada = []
    asignada.append(universidad)
    postulacion = Postulacion.objects.get(username=estudiante)
    postulacion.estadoPostulacion = "Postulado. Revisado por coordinación"
    postulacion.save()
    data = serializers.serialize('json', asignada, fields =('nombre'))
    return HttpResponse(data, mimetype='application/json')

def sin_asignar(request, creado):
    universidades = Universidad.objects.filter(cupo__gt=0)
    asignados = UniversidadAsignada.objects.all().values('nombreEstud')
    auxiliar = UniversidadAsignada.objects.all()
    lista = []
    for asignado in auxiliar:
        if asignado.nombreEstud.primeraOpcion.univ == asignado.nombreUniv:
            pass
        else:
            if asignado.nombreEstud.segundaOpcion.univ == asignado.nombreUniv:
                pass
            else:
                postu = Postulacion.objects.get(username=asignado.nombreEstud)
                lista.append((postu, True))
    sin_asignar = Postulacion.objects.filter(Q(estadoPostulacion='Postulado. Revisado por coordinación')).exclude(username__in=asignados)
    for sin in sin_asignar:
        lista.append((sin,False))
    print sin_asignar
    return render_to_response('postulante/sin_asignar.html', {'lista':lista, 'universidades': universidades, 'creado': creado},context_instance=RequestContext(request))

def seleccionar_universidad(request,id_estudiante):
    universidades = Universidad.objects.filter(cupo__gt=0)
    estudiante = Estudiante.objects.get(id=id_estudiante)
    return render_to_response('postulante/seleccionar_universidad.html', {'universidades': universidades, 'estudiante': estudiante}, context_instance=RequestContext(request))

def asignar_universidad(request, id_universidad, id_estudiante):
    universidad = Universidad.objects.get(id=id_universidad)
    estudiante = Estudiante.objects.get(id=id_estudiante)
    if UniversidadAsignada.objects.filter(nombreEstud=estudiante):
            old = UniversidadAsignada.objects.get(nombreEstud=estudiante)
            old_uni = old.nombreUniv
            old.delete()
            old_uni.cupo = old_uni.cupo + 1
            old_uni.save()
    universidad.cupo = universidad.cupo - 1
    universidad.save()
    postulacion = Postulacion.objects.get(username=estudiante)
    postulacion.estadoPostulacion = "Aceptado en " + universidad.nombre +". Como esta no era ninguna de sus opciones principales comuniquese con la coordinacion para informacion de como seguir adelante con su postulacion."
    postulacion.save()
    estudiante.user.last_name = 'aceptado'
    estudiante.user.save()

    asunto = "Sistema de Gestion de Intercambio"
    mensaje = "Hola ya tiene universidad asignada para su intercambio por favor ingrese al sistema para mas informacion sobre su postulacion. \n"
    #correo = EmailMessage(asunto, mensaje, to=['contacto@asuntopais.com'])
    correo = EmailMessage(asunto, mensaje, to=[estudiante.email])
    try:
        print "enviando"
        correo.send()

    except:
        mensaje="error al enviar el mensaje"
    asignada_aux = UniversidadAsignada.objects.create(nombreEstud=estudiante, nombreUniv=universidad)
    return HttpResponseRedirect("/sin_asignar/1")

def verCasosExcepcionales(request):
    estudiantes = Estudiante.objects.filter(tieneCasosExc = True,vistoCasoCoord=True,vistoCasoDeca=False)

    return render_to_response('gestor/verCasosExcepcionales.html', {'estudiantes':estudiantes}, context_instance=RequestContext(request))

def verDetalleCasosExcGestor(request,id_user):
    estudiante = Estudiante.objects.get(id=int(id_user))
    postulacion = Postulacion.objects.get(username=estudiante)
    return render_to_response('gestor/verDetalleCasosExcGestor.html', {'estudiante':estudiante,'postulacion':postulacion},context_instance=RequestContext(request))

def aceptarCasoExc(request,id_user):
    estudiante = Estudiante.objects.get(id=int(id_user))

    email_est = estudiante.user.email

    razon = ''
    if estudiante.casosExc.pasantia:
        razon = 'cursar la pasantia'
    else:
        if estudiante.casosExc.proyecto:
            razon = 'cursar el proyecto de grado'
        else:
            if estudiante.casosExc.trimestre:
                razon = 'quedarse de intercambio un trimestre mas'
            else:
                if estudiante.casosExc.planEstudio:
                    razon = 'modificar el plan de estudio'

    titulo = 'Respuesta de solicitud para ' + razon

    contenido = 'Buenos dias ' + estudiante.nombre1 + ' ' + estudiante.apellido1 + '\n'
    contenido += 'Le informamos que su solicitud para ' + razon + ' '
    contenido += 'ha sido aprobada'

    correo = EmailMessage(titulo, contenido, to=[email_est])
    try:
        correo.send()
    except:
        'no se envio el correo'
    estudiante.aprobadoCasoDeca = True
    estudiante.vistoCasoDeca = True
    estudiante.save()

    estudiantes = Estudiante.objects.filter(tieneCasosExc = True,vistoCasoCoord=True,vistoCasoDeca=False)
    aceptadoCaso = True
    return render_to_response('gestor/verCasosExcepcionales.html', {'estudiantes':estudiantes,'aceptadoCaso':aceptadoCaso}, context_instance=RequestContext(request))

def noAceptarCasoExc(request,id_user):
    estudiante = Estudiante.objects.get(id=int(id_user))
    email_est = estudiante.user.email
    razon = ''
    if estudiante.casosExc.pasantia:
        razon = 'cursar la pasantia'
    else:
        if estudiante.casosExc.proyecto:
            razon = 'cursar el proyecto de grado'
        else:
            if estudiante.casosExc.trimestre:
                razon = 'quedarse de intercambio un trimestre mas'
            else:
                if estudiante.casosExc.planEstudio:
                    razon = 'modificar el plan de estudio'

    titulo = 'Respuesta de solicitud para ' + razon

    contenido = 'Buenos dias ' + estudiante.nombre1 + ' ' + estudiante.apellido1 + '\n'
    contenido += 'Le informamos que su solicitud para ' + razon + ' '
    contenido += 'ha sido negada. Lo sentimos'

    correo = EmailMessage(titulo, contenido, to=[email_est])
    try:
        correo.send()
    except:
        'no se envio el correo'
    estudiante.aprobadoCasoDeca = False
    estudiante.vistoCasoDeca = True
    estudiante.save()

    estudiantes = Estudiante.objects.filter(tieneCasosExc = True,vistoCasoCoord=True,vistoCasoDeca=False)
    rechazadoCaso = True
    return render_to_response('gestor/verCasosExcepcionales.html', {'estudiantes':estudiantes,'rechazadoCaso':rechazadoCaso}, context_instance=RequestContext(request))

@login_required(login_url='/')
def ver_tabla_postuladosEXT(request):
    lista = Estudiante.objects.filter(estudUsb=False)
    print lista

    return render_to_response('gestor/ver_tabla_postuladosEXT.html', {'lista': lista}, context_instance=RequestContext(request))
