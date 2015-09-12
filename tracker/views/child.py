from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.shortcuts import render, get_object_or_404
from django.template import loader

from tracker.models import Child
from tracker.models import ChildForm
from tracker.models import Residence

def new(request, residence_id):
    if request.method == 'POST':
        form = ChildForm(request.POST, request.FILES, request=request)
        if 'discard' in request.POST:
            p = get_object_or_404(Residence, pk=residence_id)
            children = Child.objects.filter(residence_id=residence_id)
            boys = Child.objects.filter(residence_id=residence_id).filter(gender='m')
            girls = Child.objects.filter(residence_id=residence_id).filter(gender='f')
            context = {
                'residence': p,
                'children': children,
                'residence_id': p.id,
                'boys': boys,
                'girls': girls
            }
            return render(request, 'tracker/residence.html', context)
        else: 
            if form.is_valid():
                saved_child = form.save()
                if saved_child:
                    child_id = saved_child.id
                    return HttpResponseRedirect(reverse('tracker:child', kwargs={'child_id': child_id}))
    else:
        form = ChildForm()
    context = {
        'form': form.as_ul,
        'residence_id': residence_id
    }
    return render(request, 'tracker/add_child.html', context)

def view(request, child_id):
    p = get_object_or_404(Child, pk=child_id)
    context = {
        'child': p,
        'child_id': p.id,
        'residence_id': p.residence_id
    }
    return render(request, 'tracker/child_information.html', context)
    





