from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader

def index(request):
    return render(request, 'tracker/index.html')

def login(request):
    return HttpResponseRedirect(reverse('tracker:main'))