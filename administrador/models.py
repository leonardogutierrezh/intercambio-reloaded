#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class Pais(models.Model):
    nombre = models.CharField(max_length=100)

class Universidad(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.ForeignKey(Pais)

class Usuario(models.Model):
    usuario = models.ForeignKey(User)
    tipo = models.CharField(max_length=100)

class Administrador(models.Model):
    username = models.CharField(max_length=100)
    contrasena = models.CharField(max_length=100)

