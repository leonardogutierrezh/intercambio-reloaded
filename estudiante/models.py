#encoding:utf-8
#from celery.worker.strategy import default
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from postulante.models import *

class AntecedenteAcad(models.Model):
    indice = models.FloatField()
    creditosAprobados = models.IntegerField()
    anoIngreso = models.IntegerField()
    ###########3
    anosAprob = models.IntegerField()
    coordMovilidad = models.CharField(max_length=100, null=True)
    coordAcademico = models.CharField(max_length=100, null=True)

class Representante(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefCel = models.IntegerField()
    telefCasa = models.IntegerField()
    email = models.CharField(max_length=100)
    tipoRelacion = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)

class Financiamiento(models.Model):
    fuente = models.CharField(max_length=100)
    descripcionFuente = models.CharField(max_length=100)
    ayuda = models.BooleanField()
    descripcionAyuda = models.CharField(max_length=100)

class Idiomas(models.Model):
    idioma = models.CharField(max_length=100)
    verbal = models.CharField(max_length=100)
    escrito = models.CharField(max_length=100)
    auditivo = models.CharField(max_length=100)

class Estudiante(models.Model):
    user = models.ForeignKey(User)
    nombre1 = models.CharField(max_length=100)
    nombre2 = models.CharField(max_length=100)
    apellido1 = models.CharField(max_length=100)
    apellido2 = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    carnet = models.CharField(max_length=100, null=True)
    estudUsb = models.BooleanField()

    fechaCreacion = models.DateField(auto_now=True)
    origen = models.CharField(max_length=100, null=True)
    carrera = models.ForeignKey(Carrera, null=True)
    sexo = models.CharField(max_length=100, null=True)
    urbanizacion = models.CharField(max_length=100, null=True)
    calle = models.CharField(max_length=100, null=True)
    edificio = models.CharField(max_length=100, null=True)
    apartamento = models.CharField(max_length=100, null=True)
    codigopostal = models.CharField(max_length=100, null=True)
    ciudad = models.CharField(max_length=100, null=True)
    estado = models.CharField(max_length=100, null=True)
    telfCel = models.IntegerField(null=True)
    telfCasa = models.IntegerField(null=True)
    fax = models.IntegerField(null=True)
    fechaNacimiento = models.CharField(max_length=100, null=True)
    nacionalidad = models.CharField(max_length=100, null=True)
    comentario = models.CharField(max_length=100, null=True)
    cedula = models.IntegerField(max_length=50, null=True)
    pasaporte = models.CharField(max_length=100, null=True)
    lenguaMaterna = models.CharField(max_length=100, null=True)
    paisOrigen = models.ForeignKey(Pais, null=True)
    univOrigen = models.ForeignKey(Universidad, null=True)
    cursoEspanol = models.CharField(max_length=100, null=True)
    antecedente = models.ForeignKey(AntecedenteAcad, null=True)
    planDeEstudio = models.ForeignKey(PlanDeEstudio, null=True)
    estadoPostulacion = models.CharField(max_length=100, default ='Sin postular')
    representante = models.ForeignKey(Representante, null=True)
    idiomas = models.ManyToManyField(Idiomas, null=True)
    def __unicode__(self):
        return self.user.username

class UniversidadExtranjera(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.ForeignKey(Pais)
    cupo = models.IntegerField()
    def __unicode__(self):
        return self.nombre

class UniversidadAsignada(models.Model):
    nombreEstud = models.ForeignKey(Estudiante)
    nombreUniv = models.CharField(max_length=100)           ## VER

