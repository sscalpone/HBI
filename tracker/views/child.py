from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.shortcuts import render, get_object_or_404
from django.template import loader

from tracker.models import Child
from tracker.models import ChildForm
from tracker.models import Residence

def index(request):
    list_of_children = Child.objects.all()
    context = {'children': list_of_children }
    return render(request, 'tracker/residence.html', context)

def new(request, residence_id):
    if request.method == 'POST':
        form = ChildForm(request.POST, request.FILES)
        if form.is_valid():
            saved_child = form.save()
            if saved_child:
                context = {
                    'child': saved_child,
                    'child_id': saved_child.id,
                    'residence_id': saved_child.residence_id
                }
                return render(request, 'tracker/child_information.html', context)
                # return HttpResponseRedirect(reverse('tracker:child', kwargs={'child_id': child.id, 'residence_id': child.residence_id}))
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
    # return HttpResponseRedirect(reverse('tracker:child', kwargs={'child_id': child.id, 'residence_id': residence.id}))





