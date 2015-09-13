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
    if request.POST:
        form = ChildForm(request.POST, request.FILES, request=request)
        if 'discard' in request.POST:
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
        'residence_id': residence_id,
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

def edit(request, child_id):
    child = get_object_or_404(Child, pk=child_id)
    residence_id = child.residence_id
    if request.POST:
        print 'edit post'
        form = ChildForm(request.POST, request.FILES, instance=child, request=request)
        if 'discard' in request.POST:
            print 'edit discard'
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
                'residence_id': p.id,
                'active': active,
                'inactive': inactive,
                'boys': boys,
                'girls': girls,
                'at_risk': at_risk
            }
        else:
            print 'edit form.is_valid()'
            if form.is_valid():
                form.id = child.id
                saved_child = form.save()
                child_id = saved_child.id
                print 'edit validated'
                return HttpResponseRedirect(reverse('tracker:child', kwargs={'child_id': child_id}))
    else:
        print 'edit method is not post'
        form = ChildForm(instance=child)
    print 'edit context'
    context = {
        'form': form.as_ul,
        'residence_id': residence_id,
        'child_id': child_id
    }
    return render(request, 'tracker/edit_child.html', context)

