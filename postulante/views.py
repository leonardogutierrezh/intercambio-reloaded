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
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage, EmailMultiAlternatives
import os, random, string
from django.template.loader import render_to_string
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Image
from django.core import serializers
from administrador.models import Universidad
from postulante.forms import *

def listar_solicitudes_coord(request):
    user = request.user
    postulante = Postulante.objects.get(usuario=user)
    postulacion = Postulacion.objects.filter(estadoPostulacion='Postulado')

    postulaciones = []
    for post in postulacion:
        if post.username.carrera_usb == postulante.carrera:
            postulaciones.append(post)

    return render_to_response('postulante/listar_solicitudes_coord.html',{'postulante':postulante,'postulaciones':postulaciones},context_instance=RequestContext(request))

def perfilCoordinacion(request):
    user = request.user
    postulante = Postulante.objects.get(usuario=user)
    if request.method == 'POST':
        formulario = Postulante_Edit_Form(request.POST)
        if formulario.is_valid():
            email = formulario.cleaned_data['email']
            username = formulario.cleaned_data['username']
            carrera = formulario.cleaned_data['carrera']

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
            user.email = email
            postulante.carrera = carrera
            user.save()
            postulante.save()

            return render_to_response('index.html', {'perfilPostulanteCambiado':True},context_instance=RequestContext(request))
    else:
        formulario = Postulante_Edit_Form(initial={'email':user.email,'username':user.username,'carrera':postulante.carrera})
    return render_to_response('postulante/perfilPostulante.html', {'formulario':formulario},context_instance=RequestContext(request))

def verDetallePostulacion(request,id_user):
    estudiante = Estudiante.objects.get(id=int(id_user))
    postulacion = Postulacion.objects.get(username=estudiante)
    return render_to_response('postulante/verDetallePostulacion.html', {'estudiante':estudiante,'postulacion':postulacion},context_instance=RequestContext(request))