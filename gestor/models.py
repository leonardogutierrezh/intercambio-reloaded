#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from administrador.models import *

class Gestor(models.Model):
    username = models.CharField(max_length=100)
    contrasena = models.CharField(max_length=100)

class Noticas(models.Model):
    gestor = models.ForeignKey(Gestor)
    informacion = models.CharField(max_length=500)
    fecha = models.DateField(auto_now=True)

