from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context, Template
from django.contrib.auth.decorators import login_required
from django.core import serializers
from administrador.models import *
import datetime
# Create your views here.

def inicio(request):
    return render_to_response('inicio.html', {}, context_instance=RequestContext(request))

def crear_cuenta(request):
    formulario = UserCreationForm()
    return render_to_response('administrador/crear_cuenta.html', {'formulario': formulario}, context_instance=RequestContext(request))