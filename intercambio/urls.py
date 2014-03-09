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
    url(r'^$', 'administrador.views.inicio'),
    url(r'^administrador_crear_cuenta$', 'administrador.views.crear_cuenta'),
    url(r'^administrador_listar_usuarios/(?P<creado>\d+)/$', 'administrador.views.listar_usuarios'),
)
