from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'intercambio.views.home', name='home'),
    # url(r'^intercambio/', include('intercambio.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^$', 'administrador.views.inicio'),
    url(r'^$', 'estudiante.views.iniciarSesion'),
    url(r'^administrador_crear_cuenta$', 'administrador.views.crear_cuenta'),
    url(r'^cerrar_sesion$', 'administrador.views.cerrar_sesion'),
    url(r'^administrador_listar_usuarios/(?P<creado>\d+)/$', 'administrador.views.listar_usuarios'),

    url(r'^registrarEstudianteUSB', 'estudiante.views.registrarEstudianteUSB'),
    url(r'^registrarEstudianteExt', 'estudiante.views.registrarEstudianteExt'),
    url(r'^iniciarSesion', 'estudiante.views.iniciarSesion'),
    url(r'^recaudosExt', 'administrador.views.recaudosExt'),
    url(r'^recaudosNac', 'administrador.views.recaudosNac'),
    url(r'^recaudosAdic', 'administrador.views.recaudosAdic'),
    url(r'^estadoPostulacion', 'estudiante.views.estadoPostulacion'),
    url(r'^perfilEstudianteUSB', 'estudiante.views.perfilEstudianteUSB'),
    url(r'^perfilEstudianteExt', 'estudiante.views.perfilEstudianteExt'),
    url(r'^ver_usuario/(?P<id_usuario>\d+)/$','administrador.views.ver_usuario' ),
    url(r'^postularse', 'estudiante.views.postularse'),
    url(r'^formularioUNO', 'estudiante.views.formularioUNO'),
)
