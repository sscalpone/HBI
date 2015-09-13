from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.shortcuts import render, get_object_or_404
from django.template import loader

from tracker.models import Residence
from tracker.models import ResidenceForm
from tracker.models import Child

def index(request):
    list_of_residences = Residence.objects.all()
    context = {'residences': list_of_residences }
    return render(request, 'tracker/main.html', context)

def new(request):
    if request.method == 'POST':
        form = ResidenceForm(request.POST, request.FILES, request=request)
        if 'discard' in request.POST:
            return HttpResponseRedirect(reverse('tracker:residences'))
        else:
            if form.is_valid():
                saved_residence = form.save()
                if saved_residence:
                    return HttpResponseRedirect(reverse('tracker:residences'))
    else:
        form = ResidenceForm()
    context = {
        'form': form.as_ul,
    }
    return render(request, 'tracker/add_residence.html', context)

def view(request, residence_id):
    p = get_object_or_404(Residence, pk=residence_id)
    children = Child.objects.filter(residence_id=residence_id)
    active = Child.objects.filter(residence_id=residence_id).filter(active=True)
    inactive = Child.objects.filter(residence_id=residence_id).filter(active=False)
    boys = Child.objects.filter(residence_id=residence_id).filter(gender='m')
    girls = Child.objects.filter(residence_id=residence_id).filter(gender='f')
    at_risk = Child.objects.filter(residence_id=residence_id).filter(priority='1')
    context = {
        'residence': p,
        'children': children,
        'active': active,
        'inactive': inactive,
        'residence_id': p.id,
        'boys': boys,
        'girls': girls,
        'at_risk': at_risk
    }
    return render(request, 'tracker/residence.html', context)

def edit(request, residence_id):
    residence = get_object_or_404(Residence, pk=(residence_id))
    if request.method == 'POST':
        form = ResidenceForm(request.POST, request.FILES, instance=residence, request=request)
        if 'discard' in request.POST:
            return HttpResponseRedirect(reverse('tracker:residences'))
        else:
            if form.is_valid():
                saved_residence = form.save()
                if saved_residence:
                    return HttpResponseRedirect(reverse('tracker:residences'))
    else:
        form = ResidenceForm(instance=residence)
    context = {
        'form': form.as_ul,
        'residence_id': residence.id
    }
    return render(request, 'tracker/edit_residence.html', context)





