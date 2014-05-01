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
#from gestor.forms import *

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
    postulados = Postulacion.objects.filter(estadoPostulacion='Postulado. Revisado por coordinacion')
    if opcion == '1':
        for postulado in postulados:
            lista.append((postulado.username, postulado.username.primeraOpcion.univ))

    elif opcion == '2':
        for postulado in postulados:
            lista.append((postulado.username, postulado.username.segundaOpcion.univ))
    else:
        print 3
    return render_to_response('gestor/ver_tabla_postulados.html', {'lista': lista}, context_instance=RequestContext(request))