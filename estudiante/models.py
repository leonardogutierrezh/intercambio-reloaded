#encoding:utf-8
#from celery.worker.strategy import default
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from postulante.models import *
from countries.models import *
from administrador.models import Idioma,Universidad

class AntecedenteAcad(models.Model):
    indice = models.FloatField()
    creditosAprobados = models.IntegerField()
    anoIngreso = models.IntegerField()
    ###########3
    anosAprob = models.IntegerField()
    coordMovilidad = models.CharField(max_length=100, null=True)
    coordAcademico = models.CharField(max_length=100, null=True)

class DocumentosRequeridos(models.Model):
    foto = models.ImageField(upload_to='cargas')
    informe = models.ImageField(upload_to='cargas')
    carta = models.ImageField(upload_to='cargas')
    planilla = models.ImageField(upload_to='cargas')
    certificado = models.ImageField(upload_to='cargas', null=True, blank=True)
    curriculum = models.ImageField(upload_to='cargas', null=True, blank=True)

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

class ManejoIdiomas(models.Model):
    idioma = models.ForeignKey(Idioma)
    verbal = models.CharField(max_length=30)
    escrito = models.CharField(max_length=30)
    auditivo = models.CharField(max_length=30)
    auxiliar = models.CharField(max_length=10)

class OpcionUNO(models.Model):
    programa = models.ForeignKey(ProgramaIntercambio)
    univ = models.ForeignKey(Universidad)
    tipoPrograma = models.CharField(max_length=50)
    fechaInicio = models.CharField(max_length=50)
    anoInicio = models.CharField(max_length=50)
    fechaFin = models.CharField(max_length=50)
    anoFin = models.CharField(max_length=50)
    duracion = models.CharField(max_length=50)

class OpcionDOS(models.Model):
    programa = models.ForeignKey(ProgramaIntercambio)
    univ = models.ForeignKey(Universidad)
    tipoPrograma = models.CharField(max_length=50)
    fechaInicio = models.CharField(max_length=50)
    anoInicio = models.CharField(max_length=50)
    fechaFin = models.CharField(max_length=50)
    anoFin = models.CharField(max_length=50)
    duracion = models.CharField(max_length=50)

class Estudiante(models.Model):
    user = models.ForeignKey(User)
    nombre1 = models.CharField(max_length=100)
    nombre2 = models.CharField(max_length=100)
    apellido1 = models.CharField(max_length=100)
    apellido2 = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    carnet = models.CharField(max_length=100, null=True,  blank=True)
    estudUsb = models.BooleanField()

    fechaCreacion = models.DateField(auto_now=True, blank=True)
    origen = models.CharField(max_length=100, null=True, blank=True)
    carrera_usb = models.ForeignKey(CarreraUsb, null=True, blank=True)
    carrera_ext = models.ForeignKey(Carrera, null=True, blank=True)
    sexo = models.CharField(max_length=100, null=True, blank=True)
    urbanizacion = models.CharField(max_length=100, null=True, blank=True)
    calle = models.CharField(max_length=100, null=True, blank=True)
    edificio = models.CharField(max_length=100, null=True, blank=True)
    apartamento = models.CharField(max_length=100, null=True, blank=True)
    codigopostal = models.CharField(max_length=100, null=True, blank=True)
    ciudad = models.CharField(max_length=100, null=True, blank=True)
    estado = models.CharField(max_length=100, null=True, blank=True)
    telfCel = models.IntegerField(null=True, blank=True)
    telfCasa = models.IntegerField(null=True, blank=True)
    fax = models.IntegerField(null=True, blank=True)
    fechaNacimiento = models.CharField(max_length=100, null=True, blank=True)
    nacionalidad = models.ForeignKey(Country, null=True, blank=True)
    comentario = models.CharField(max_length=100, null=True, blank=True)
    cedula = models.IntegerField(max_length=50, null=True, blank=True)
    pasaporte = models.CharField(max_length=100, null=True, blank=True)
    lenguaMaterna = models.CharField(max_length=100, null=True, blank=True)
    paisOrigen = models.ForeignKey(Pais, null=True, blank=True)
    univOrigen = models.ForeignKey(Universidad, null=True, blank=True)
    cursoEspanol = models.CharField(max_length=100, null=True, blank=True)
    antecedente = models.ForeignKey(AntecedenteAcad, null=True, blank=True)
    planDeEstudio = models.ManyToManyField(PlanDeEstudio, null=True, blank=True)
    estadoPostulacion = models.CharField(max_length=100, default ='Sin postular')
    representante = models.ForeignKey(Representante, null=True, blank=True)
    idiomas = models.ManyToManyField(ManejoIdiomas, null=True, blank=True)
    financiamiento = models.ForeignKey(Financiamiento, null=True, blank=True)
    documentos = models.ForeignKey(DocumentosRequeridos, null=True, blank=True)
    primerPaso = models.BooleanField(default=False)
    segundoPaso = models.BooleanField(default=False)
    tercerPaso = models.BooleanField(default=False)
    cuartoPaso = models.BooleanField(default=False)
    primeraOpcion = models.ForeignKey(OpcionUNO,null=True,blank=True)
    segundaOpcion = models.ForeignKey(OpcionDOS,null=True,blank=True)

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


