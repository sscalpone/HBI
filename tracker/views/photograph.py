import datetime

from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse


from django.shortcuts import render, get_object_or_404
from django.template import loader
import django.template.loader

from tracker.models import Photograph, PhotographForm
from tracker.models import Child

@login_required
def index(request, child_id):
    list = Photograph.objects.filter(child_id=child_id)
    child = get_object_or_404(Child, pk=child_id)
    context = {
        'Photographs': list,
        'child': child,
        'child_id': child_id,
        'residence_id': child.residence_id,
    }
    return render(request, 'tracker/add_photograph.html', context)

@login_required
def new(request, child_id):
    child = get_object_or_404(Child, pk=child_id)
    if request.method == 'POST':
        exam_form = PhotographForm(request.POST, request.FILES, request=request)
        if 'discard' in request.POST:
            return HttpResponseRedirect(reverse('tracker:child', kwargs={'child_id': child_id}))

        else:
            if exam_form.is_valid():
                    saved_exam = exam_form.save(commit=False)
                    saved_exam.child = child
                    saved_exam.save()
                    exam_form.save_m2m()
                    if 'save' in request.POST:
                        return HttpResponseRedirect(reverse('tracker:edit_photo', kwargs={'child_id': child_id, 'exam_id': saved_exam.id}))
                    else:
                        return HttpResponseRedirect(reverse('tracker:child', kwargs={'child_id': child_id}))     
    else:
        exam_form = PhotographForm(initial={
                'child': child,
                'child_id': child_id,
                'date': datetime.date.today(),
            }
        )
    exam_list = Photograph.objects.filter(child_id=child_id)
    context = {
        'child': child,
        'child_id': child_id,
        'residence_id': child.residence_id,
        'photograph_form': exam_form.as_ul,
        'Photographs': exam_list,
    }
    return render(request, 'tracker/add_photograph.html', context)

@login_required
def view(request, child_id, exam_id):
    if request.method=="POST":
        exam = get_object_or_404(Photograph, pk=exam_id)
        child = get_object_or_404(Child, pk=child_id)
        if 'yes' in request.POST:
            exam.delete()
            return HttpResponseRedirect(reverse('tracker:child', kwargs={'child_id': child_id}))  
        elif 'no' in request.POST:
            context = {
                'exam': exam,
                'child': child,
                'child_id': child.id,
                'residence_id': child.residence_id,
            }
            return render(request, 'tracker/photograph.html', context)
    p = get_object_or_404(Photograph, pk=exam_id)
    child = get_object_or_404(Child, pk=child_id)
    context = {
        'exam': p,
        'child': child,
        'child_id': child.id,
        'residence_id': child.residence_id,
    }
    return render(request, 'tracker/photograph.html', context)

@login_required
def edit(request, child_id, exam_id):
    child = get_object_or_404(Child, pk=child_id)
    exam = get_object_or_404(Photograph, pk=exam_id)
    if request.method == 'POST':
        exam_form = PhotographForm(request.POST, request.FILES, instance=exam, request=request)
        
        if 'discard' in request.POST:
            return HttpResponseRedirect(reverse('tracker:child', kwargs={'child_id': child_id}))

        else:
            if exam_form.is_valid():
                    saved_exam = exam_form.save(commit=False)
                    saved_exam.child = child
                    saved_exam.save()
                    exam_form.save_m2m()
                    if 'save' in request.POST:
                        return HttpResponseRedirect(reverse('tracker:edit_photo', kwargs={'child_id': child_id, 'exam_id': saved_exam.id}))
                    else:
                        return HttpResponseRedirect(reverse('tracker:child', kwargs={'child_id': child_id}))  
        
    else:
        exam_form = PhotographForm(initial={
                'child': child,
                'child_id': child_id,
                'date': datetime.date.today(),
            }, instance=exam
        )

    exam_list = Photograph.objects.filter(child_id=child_id)
    context = {
        'child': child,
        'child_id': child_id,
        'exam_id': exam.id,
        'residence_id': child.residence_id,
        'photograph_form': exam_form.as_ul,
        'Photographs': exam_list,
    }
    return render(request, 'tracker/edit_photograph.html', context)

def delete(request, child_id, exam_id):
    if request.method=="POST":
        exam = get_object_or_404(Photograph, pk=exam_id)
        child = get_object_or_404(Child, pk=child_id)
        if 'yes' in request.POST:
            exam.delete()
            return HttpResponseRedirect(reverse('tracker:child', kwargs={'child_id': child_id}))  
        elif 'no' in request.POST:
            context = {
                'exam': exam,
                'child': child,
                'child_id': child.id,
                'residence_id': child.residence_id,
            }
            return render(request, 'tracker/photograph.html', context)
    return render(request, 'tracker/delete_photograph.html')            



    



