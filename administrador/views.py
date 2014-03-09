from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context, Template
from django.contrib.auth.decorators import login_required
from django.core import serializers
from administrador.models import *
from administrador.forms import *
import datetime
# Create your views here.

def inicio(request):
    return render_to_response('inicio.html', {}, context_instance=RequestContext(request))

def crear_cuenta(request):
    if request.method == 'POST':
        formulario = NuevoUsuarioForm(request.POST)
        if formulario.is_valid():
            nombreUsu = formulario.cleaned_data['nombre_usuario']
            email = formulario.cleaned_data['email']
            nombre = formulario.cleaned_data['nombre']
            user = User.objects.create_user(nombre, email, 'johnpassword')
    else:
        formulario = NuevoUsuarioForm()
    return render_to_response('administrador/crear_cuenta.html', {'formulario': formulario}, context_instance=RequestContext(request))