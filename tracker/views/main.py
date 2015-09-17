from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader

def index(request):
    return render(request, 'tracker/index.html')

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
                'error_message': "You are not an active user.",
            })
    else:
        # Return an 'invalid login' error message
        return render(request, 'tracker/index.html', {
            'error_message': "Your username and password do not match.",
        })

def logout(request):
    auth_logout(request)
    return render(request, 'tracker/index.html', {
        'message': "You have successfully logged out.",
        })
