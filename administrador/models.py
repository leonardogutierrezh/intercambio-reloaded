#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from countries.models import *

class Pais(models.Model):
    nombre = models.CharField(max_length=100)
    def __unicode__(self):
        return self.nombre

class ProgramaIntercambio(models.Model):
    nombre = models.CharField(max_length=100)
    def __unicode__(self):
        return self.nombre

class Universidad(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.ForeignKey(Country)
    programa = models.ForeignKey(ProgramaIntercambio)
    cupo = models.IntegerField()
    def __unicode__(self):
        return self.nombre

class Usuario(models.Model):
    usuario = models.ForeignKey(User)
    tipo = models.CharField(max_length=100)

class Administrador(models.Model):
    username = models.CharField(max_length=100)
    usuario = models.ForeignKey(User)
    email = models.EmailField()
    nombre = models.CharField(max_length=200)

class Log(models.Model):
    suceso = models.CharField(max_length=200)
    usuario = models.ForeignKey(User)
    fecha = models.DateField(auto_now=True)

class Idioma(models.Model):
    nombre = models.CharField(max_length=100)

#class ProgramaIntercambio(models.Model):
#    nombre = models.CharField(max_length=100)
#    universidad = models.ManyToManyField(Universidad)
#    def __unicode__(self):
#        return self.nombre
