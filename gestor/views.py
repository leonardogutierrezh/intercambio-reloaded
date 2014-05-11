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
    postulados = Postulacion.objects.filter(estadoPostulacion='Postulado. Revisado por coordinación')
    uni_aux = "&&&&&&"
    if opcion == '1':
        for postulado in postulados:
            if UniversidadAsignada.objects.filter(nombreEstud=postulado.username, nombreUniv=postulado.username.primeraOpcion.univ):
                existe=1
            else:
                existe=0
            if postulado.username.primeraOpcion.univ.nombre == uni_aux:
                lista.append((postulado.username, postulado.username.primeraOpcion.univ, "estudiante",existe))
            else:
                lista.append((postulado.username, postulado.username.primeraOpcion.univ, "universidad",existe))
                lista.append((postulado.username, postulado.username.primeraOpcion.univ, "estudiante",existe))
                uni_aux = postulado.username.primeraOpcion.univ.nombre
    elif opcion == '2':
        for postulado in postulados:
            if UniversidadAsignada.objects.filter(nombreEstud=postulado.username, nombreUniv=postulado.username.segundaOpcion.univ):
                existe=1
            else:
                existe=0
            if postulado.username.segundaOpcion.univ.nombre == uni_aux:
                lista.append((postulado.username, postulado.username.segundaOpcion.univ, "estudiante",existe))
            else:
                lista.append((postulado.username, postulado.username.segundaOpcion.univ, "universidad",existe))
                lista.append((postulado.username, postulado.username.segundaOpcion.univ, "estudiante",existe))
                uni_aux = postulado.username.segundaOpcion.univ.nombre
    else:
        print 3
    return render_to_response('gestor/ver_tabla_postulados.html', {'lista': lista, 'opcion': opcion}, context_instance=RequestContext(request))

def verDetallePostulacionDRIC(request,id_user):
    estudiante = Estudiante.objects.get(id=int(id_user))
    postulacion = Postulacion.objects.get(username=estudiante)
    return render_to_response('postulante/verDetallePostulacion.html', {'estudiante':estudiante,'postulacion':postulacion},context_instance=RequestContext(request))

def ajax_aceptar_postulado(request):
    print "entre al ajax" + request.GET['id_universidad']
    print "opcion" + request.GET['opcion']
    print "estudiante" +  request.GET['id_estudiante']
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
        data = serializers.serialize('json', asignada, fields =('nombreEstud', 'nombreUniv'))
        return HttpResponse(data, mimetype='application/json')
    else:
        return False
