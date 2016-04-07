# coding=utf-8

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader


"""index() checks the authentication of each user. If they check out, 
they're taken to the home page. If they aren't, they get set back to 
the login template.
"""
def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('tracker:residences'))
    else:
        return render(request, 'tracker/index.html')


"""login() authenticates the user's username and password. If the 
username and password match, and the user is active, then the index 
template is loaded.
"""
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            return HttpResponseRedirect(reverse('tracker:residences'))
        else:
            # Return a 'disabled account' error message
            return render(request, 'tracker/index.html', {
                'error_message': 'Usted no es un usuario activo.',
            })
    else:
        # Return an 'invalid login' error message
        return render(request, 'tracker/index.html', {
            'error_message': 
                'Su nombre de usuario y la contraseña no coinciden.',
        })


"""logout() logs the user out and renders the index template with a 
"Your session has been terminated" message.
"""
def logout(request):
    auth_logout(request)
    return render(request, 'tracker/index.html', 
        {
            'message': 'Has terminado tu sesion satisfactoriamente.',
        })
