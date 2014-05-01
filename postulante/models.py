#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from administrador.models import *

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
    indiceCarrera = models.CharField(max_length=10,default=1)
    def __unicode__(self):
        return self.nombre

class MateriaUSB(models.Model):
    cod_carrera = models.ManyToManyField(CarreraUsb)
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=100)
    creditos = models.IntegerField()
    def __unicode__(self):
        return self.codigo

class PlanDeEstudio(models.Model):
    materiaUsb = models.ForeignKey(MateriaUSB)
    codigoUniv = models.CharField(max_length=100)
    nombreMateriaUniv = models.CharField(max_length=100)
    creditosUniv = models.IntegerField()
    auxiliar = models.CharField(max_length=10)

from estudiante.models import Estudiante

class Postulante(models.Model):
    usuario = models.ForeignKey(User)
    tipo = models.CharField(max_length=100)
    universidad = models.ForeignKey(Universidad, null=True, blank=True)
    carrera = models.ForeignKey(CarreraUsb, null=True, blank=True)

class Postulacion(models.Model):
    username = models.ForeignKey(Estudiante)
    estadoPostulacion = models.CharField(max_length=100)
    recomendadoCoordinacion = models.BooleanField()
    comentRecomendacionCoord = models.CharField(max_length=100, null=True)
    date = models.DateField(auto_now=True)



