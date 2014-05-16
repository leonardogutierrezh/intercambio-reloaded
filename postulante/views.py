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

def verDetalleCasosExc(request,id_user):
    estudiante = Estudiante.objects.get(id=int(id_user))
    postulacion = Postulacion.objects.get(username=estudiante)
    return render_to_response('postulante/verDetalleCasosExc.html', {'estudiante':estudiante,'postulacion':postulacion},context_instance=RequestContext(request))

def eliminarPostulacion_coord(request,id_user):
    estudiante = Estudiante.objects.get(id=int(id_user))
    postulacion = Postulacion.objects.get(username=estudiante)

    postulacion.estadoPostulacion = 'Sin postular'
    postulacion.save()
    estudiante.primerPaso = False
    estudiante.segundoPaso = False
    estudiante.tercerPaso = False
    estudiante.cuartoPaso = False

    estudiante.sexo = ''
    estudiante.fechaNacimiento = ''
    estudiante.urbanizacion = ''
    estudiante.calle = ''
    estudiante.edificio = ''
    estudiante.apartamento = ''
    estudiante.codigopostal = ''

    for plan in estudiante.planDeEstudio.all():
        plan.delete()
    for idio in estudiante.idiomas.all():
        idio.delete()
    estudiante.save()

    eliminadoPostulacion = True

    user = request.user
    postulante = Postulante.objects.get(usuario=user)
    postulacion = Postulacion.objects.filter(estadoPostulacion='Postulado')

    postulaciones = []
    for post in postulacion:
        if post.username.carrera_usb == postulante.carrera:
            postulaciones.append(post)

    ## Correo
    return render_to_response('postulante/listar_solicitudes_coord.html', {'postulante':postulante,'estudiante':estudiante,'postulaciones':postulaciones,'postulacion':postulacion,'eliminadoPostulacion':eliminadoPostulacion},context_instance=RequestContext(request))

def recomendarCoord(request,id_user):
    user = request.user
    postulante = Postulante.objects.get(usuario=user)
    estudiante = Estudiante.objects.get(id=int(id_user))
    if request.method == 'POST':
        formulario = Postulante_RecomendarEstudiante(request.POST)
        if formulario.is_valid():
            comentarios = formulario.cleaned_data['comentarios']

            postulacion = Postulacion.objects.get(username=estudiante)
            postulacion.comentRecomendacionCoord = comentarios
            postulacion.recomendadoCoordinacion = True
            postulacion.estadoPostulacion = 'Postulado. Revisado por coordinación'
            postulacion.indice_normalizado = float('%.2f'%(estudiante.antecedente.indice/float(postulacion.username.carrera_usb.indiceCarrera)))
            postulacion.save()
            postulacion = Postulacion.objects.filter(estadoPostulacion='Postulado')
            postulaciones = []
            for post in postulacion:
                if post.username.carrera_usb == postulante.carrera:
                    postulaciones.append(post)
            return render_to_response('postulante/listar_solicitudes_coord.html',{'postulante':postulante,'postulaciones':postulaciones,'estudiante':estudiante,
                                                                                  'recomendado':True},context_instance=RequestContext(request))
    else:
        formulario = Postulante_RecomendarEstudiante(initial={'indice':estudiante.antecedente.indice})
    return render_to_response('postulante/recomendarCoord.html', {'formulario':formulario},context_instance=RequestContext(request))

def recomendarCasoCoord(request,id_user):
    user = request.user
    postulante = Postulante.objects.get(usuario=user)
    estudiante = Estudiante.objects.get(id=int(id_user))

    if request.method == 'POST':
        formulario = Postulante_RecomendarCasoEstudiante(request.POST)
        if formulario.is_valid():
            comentarios = formulario.cleaned_data['comentarios']

            estudiante.casosExc.comentRecomendacionCoord = comentarios
            estudiante.casosExc.recomendadoCoordinacion = True

            estudiante.vistoCasoCoord = True

            estudiante.casosExc.save()
            estudiante.save()

            estudiantes_casos = Estudiante.objects.filter(tieneCasosExc = True,vistoCasoCoord=False)
            estudiantes = []
            for est in estudiantes_casos:
                if est.carrera_usb == postulante.carrera:
                    estudiantes.append(est)

            recomendacionCasos = True
            return render_to_response('postulante/listar_casosExc_coord.html',{'estudiantes':estudiantes,'recomendacionCasos':recomendacionCasos},context_instance=RequestContext(request))

    else:
        formulario = Postulante_RecomendarCasoEstudiante()
    return render_to_response('postulante/recomendarCasoCoord.html', {'formulario':formulario},context_instance=RequestContext(request))

def noRecomendarCasoCoord(request,id_user):
    user = request.user
    postulante = Postulante.objects.get(usuario=user)
    estudiante = Estudiante.objects.get(id=int(id_user))

    if request.method == 'POST':
        formulario = Postulante_RecomendarCasoEstudiante(request.POST)
        if formulario.is_valid():
            comentarios = formulario.cleaned_data['comentarios']

            estudiante.casosExc.comentRecomendacionCoord = comentarios
            estudiante.casosExc.recomendadoCoordinacion = False

            estudiante.vistoCasoCoord = True

            estudiante.casosExc.save()
            estudiante.save()

            estudiantes_casos = Estudiante.objects.filter(tieneCasosExc = True,vistoCasoCoord=False)
            estudiantes = []
            for est in estudiantes_casos:
                if est.carrera_usb == postulante.carrera:
                    estudiantes.append(est)

            recomendacionCasos = True
            return render_to_response('postulante/listar_casosExc_coord.html',{'estudiantes':estudiantes,'recomendacionCasos':recomendacionCasos},context_instance=RequestContext(request))

    else:
        formulario = Postulante_RecomendarCasoEstudiante()
    return render_to_response('postulante/noRecomendarCasoCoord.html', {'formulario':formulario},context_instance=RequestContext(request))

def noRecomendarCoord(request,id_user):
    user = request.user
    postulante = Postulante.objects.get(usuario=user)
    estudiante = Estudiante.objects.get(id=int(id_user))
    if request.method == 'POST':
        formulario = Postulante_RecomendarEstudiante(request.POST)
        if formulario.is_valid():
            comentarios = formulario.cleaned_data['comentarios']

            postulacion = Postulacion.objects.get(username=estudiante)
            postulacion.comentRecomendacionCoord = comentarios
            postulacion.recomendadoCoordinacion = False
            postulacion.estadoPostulacion = 'Postulado. Revisado por coordinación'
            postulacion.save()

            postulacion = Postulacion.objects.filter(estadoPostulacion='Postulado')
            postulaciones = []
            for post in postulacion:
                if post.username.carrera_usb == postulante.carrera:
                    postulaciones.append(post)
            return render_to_response('postulante/listar_solicitudes_coord.html',{'postulante':postulante,'postulaciones':postulaciones,'estudiante':estudiante,
                                                                                  'recomendado':True},context_instance=RequestContext(request))
    else:
        formulario = Postulante_RecomendarEstudiante(initial={'indice':estudiante.antecedente.indice})
    return render_to_response('postulante/noRecomendarCasoCoord.html', {'formulario':formulario},context_instance=RequestContext(request))

def agregarMateria(request):
    user = request.user
    postulante = Postulante.objects.get(usuario=user)

    if request.method == 'POST':
        formulario = nuevaMateriaForm(request.POST)
        if formulario.is_valid():
            nombre = formulario.cleaned_data['nombre']
            creditos = formulario.cleaned_data['creditos']
            codigo = formulario.cleaned_data['codigo']

            materias = MateriaUSB.objects.filter(codigo = codigo)
            if len(materias) != 0:
                return render_to_response('postulante/agregarMateria.html',{'formulario':formulario,'repetidoCod':True},context_instance=RequestContext(request))
            materia = MateriaUSB.objects.create(nombre=nombre,creditos=creditos,codigo=codigo)
            materia.cod_carrera.add(postulante.carrera)
            materia.save()

            materias = MateriaUSB.objects.all()
            return render_to_response('postulante/todasMaterias.html',{'materias':materias,'agregadaMateria':True},context_instance=RequestContext(request))
    else:
        formulario = nuevaMateriaForm()
    return render_to_response('postulante/agregarMateria.html', {'formulario':formulario},context_instance=RequestContext(request))

def todasMaterias(request):
    user = request.user
    postulante = Postulante.objects.get(usuario=user)
    materias = MateriaUSB.objects.all()
    return render_to_response('postulante/todasMaterias.html',{'materias':materias},context_instance=RequestContext(request))

def modificarMateria(request,id_mat):
    materia = MateriaUSB.objects.get(id=int(id_mat))
    if request.method == 'POST':
        formulario = nuevaMateriaForm(request.POST)
        if formulario.is_valid():
            nombre = formulario.cleaned_data['nombre']
            creditos = formulario.cleaned_data['creditos']
            codigo = formulario.cleaned_data['codigo']

            if materia.codigo != codigo:
                materias = MateriaUSB.objects.filter(codigo = codigo)
                if len(materias) != 0:
                    return render_to_response('postulante/agregarMateria.html',{'formulario':formulario,'repetidoCod':True},context_instance=RequestContext(request))

            materia.nombre=nombre
            materia.creditos=creditos
            materia.codigo=codigo
            materia.save()

            materias = MateriaUSB.objects.all()
            return render_to_response('postulante/todasMaterias.html',{'materias':materias,'modificadaMateria':True},context_instance=RequestContext(request))
    else:
        formulario = nuevaMateriaForm(initial={'nombre':materia.nombre,'creditos':materia.creditos,'codigo':materia.codigo})
    return render_to_response('postulante/agregarMateria.html', {'formulario':formulario},context_instance=RequestContext(request))

def eliminarMateria(request,id_mat):
    materia = MateriaUSB.objects.get(id=int(id_mat))
    materia.delete()
    materias = MateriaUSB.objects.all()
    return render_to_response('postulante/todasMaterias.html',{'materias':materias,'eliminadaMateria':True},context_instance=RequestContext(request))

def listar_casosExc_coord(request):
    user = request.user
    postulante = Postulante.objects.get(usuario=user)

    estudiantes_casos = Estudiante.objects.filter(tieneCasosExc = True,vistoCasoCoord=False)
    estudiantes = []
    for est in estudiantes_casos:
        if est.carrera_usb == postulante.carrera:
            estudiantes.append(est)

    return render_to_response('postulante/listar_casosExc_coord.html',{'estudiantes':estudiantes},context_instance=RequestContext(request))