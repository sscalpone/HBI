from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.shortcuts import render, get_object_or_404
from django.template import loader

from tracker.models import Child
from tracker.models import ChildForm

def index(request):
    list_of_children = Child.objects.all()
    context = {'children': list_of_children }
    return render(request, 'tracker/children.html', context)

def new(request):
    if request.method == 'POST':
        form = ChildForm(request.POST, request.FILES)
        if form.is_valid():
            saved_child = form.save()
            if saved_child:
                return HttpResponseRedirect(reverse('tracker:children'))
    else:
        form = ChildForm()
    context = {
        'form': form.as_ul,
    }
    return render(request, 'tracker/add_child.html', context)

def view(request, child_id):
    p = get_object_or_404(Child, pk=child_id)
    context = {
        'child': p,
        'child_id': p.id
    }
    return render(request, 'tracker/child_information.html', context)