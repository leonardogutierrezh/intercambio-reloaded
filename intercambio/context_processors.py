
def autentificar(request):
    print "entre"
    autenticado = 0
    usuario = 'ninguno'
    user = ""
    if request.user.is_authenticated():
        print "autenticado"
        user = request.user
        usuario = user.first_name
    print usuario
    return { 'usuario': usuario, 'autenticado' : autenticado , 'user': user}