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
        form = ResidenceForm(request.POST, request.FILES)
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
    context = {
        'residence': p,
        'children': children,
        'residence_id': p.id,
    }
    return render(request, 'tracker/residence.html', context)





