#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from administrador.models import *

class MateriaUSB(models.Model):
    cod_carrera = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=100)
    creditos = models.IntegerField()

class PlanDeEstudio(models.Model):
    materiaUsb = models.ForeignKey(MateriaUSB)
    codigoUniv = models.CharField(max_length=100)
    nombreMateriaUniv = models.CharField(max_length=100)
    creditosUniv = models.IntegerField()

class Carrera(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=100)
    decanato = models.CharField(max_length=100, null=True)
    areaDeEstudio = models.CharField(max_length=100, null=True)
    universidad = models.ForeignKey(Universidad)
    def __unicode__(self):
        return self.nombre

class CarreraUsb(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=100)
    decanato = models.CharField(max_length=100, null=True)
    areaDeEstudio = models.CharField(max_length=100, null=True)
    def __unicode__(self):
        return self.nombre

from estudiante.models import Estudiante

class Postulante(models.Model):
    usuario = models.ForeignKey(User)
    tipo = models.CharField(max_length=100)
    universidad = models.ForeignKey(Universidad, null=True, blank=True)
    carrera = models.ForeignKey(Carrera, null=True, blank=True)

class Postulacion(models.Model):
    username = models.ForeignKey(Estudiante)
    estadoPostulacion = models.CharField(max_length=100)
    comentRecomendacion = models.CharField(max_length=100, null=True)
    date = models.DateField(auto_now=True)


