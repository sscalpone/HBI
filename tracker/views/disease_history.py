import datetime

from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.shortcuts import render, get_object_or_404
from django.template import loader
import django.template.loader

from tracker.models import DiseaseHistory, DiseaseHistoryForm
from tracker.models import Signature, SignatureForm
from tracker.models import Child

def index(request, child_id):
    list = DiseaseHistory.objects.filter(child_id=child_id)
    child = get_object_or_404(Child, pk=child_id)
    context = {
        'DiseaseHistories': list,
        'child': child,
        'child_id': child_id,
        'residence_id': child.residence_id,
    }
    return render(request, 'tracker/add_disease_history.html', context)

def new(request, child_id):
    child = get_object_or_404(Child, pk=child_id)
    if request.method == 'POST':
        signature_form = SignatureForm(request.POST, request.FILES, request=request)
        exam_form = DiseaseHistoryForm(request.POST, request.FILES, request=request)
        if 'discard' in request.POST:
            return HttpResponseRedirect(reverse('tracker:child', kwargs={'child_id': child_id}))

        else:
            if signature_form.is_valid() and exam_form.is_valid():
                saved_signature = signature_form.save()
                
                if saved_signature:
                    saved_exam = exam_form.save(commit=False)
                    saved_exam.signature = saved_signature
                    saved_exam.child = child
                    saved_exam.save()
                    exam_form.save_m2m()
                    if 'save' in request.POST:
                        return HttpResponseRedirect(reverse('tracker:edit_disease_history', kwargs={'child_id': child_id, 'exam_id': saved_exam.id}))
                    else:
                        return HttpResponseRedirect(reverse('tracker:child', kwargs={'child_id': child_id}))     
    else:
        exam_form = DiseaseHistoryForm(initial={
                'child': child,
                'child_id': child_id,
                'date': datetime.date.today(),
            }
        )
        signature_form = SignatureForm()
    exam_list = DiseaseHistory.objects.filter(child_id=child_id)
    context = {
        'child': child,
        'child_id': child_id,
        'residence_id': child.residence_id,
        'disease_history_form': exam_form.as_ul,
        'signature_form': signature_form.as_ul,
        'DiseaseHistories': exam_list,
    }
    return render(request, 'tracker/add_disease_history.html', context)

def view(request, child_id, exam_id):
    p = get_object_or_404(DiseaseHistory, pk=exam_id)
    child = get_object_or_404(Child, pk=child_id)
    signature = get_object_or_404(Signature, pk=p.signature_id)
    context = {
        'exam': p,
        'child': child,
        'child_id': child.id,
        'residence_id': child.residence_id,
        'signature': signature
    }
    return render(request, 'tracker/disease_history.html', context)

def edit(request, child_id, exam_id):
    child = get_object_or_404(Child, pk=child_id)
    exam = get_object_or_404(DiseaseHistory, pk=exam_id)
    signature = get_object_or_404(Signature, pk=exam.signature_id)
    if request.method == 'POST':
        signature_form = SignatureForm(request.POST, request.FILES, instance=signature, request=request)
        exam_form = DiseaseHistoryForm(request.POST, request.FILES, instance=exam, request=request)
        
        if 'discard' in request.POST:
            return HttpResponseRedirect(reverse('tracker:child', kwargs={'child_id': child_id}))

        else:
            if signature_form.is_valid() and exam_form.is_valid():
                saved_signature = signature_form.save()
                
                if saved_signature:
                    saved_exam = exam_form.save(commit=False)
                    saved_exam.signature = saved_signature
                    saved_exam.child = child
                    saved_exam.save()
                    exam_form.save_m2m()
                    if 'save' in request.POST:
                        return HttpResponseRedirect(reverse('tracker:edit_disease_history', kwargs={'child_id': child_id, 'exam_id': saved_exam.id}))
                    else:
                        return HttpResponseRedirect(reverse('tracker:child', kwargs={'child_id': child_id}))  
        
    else:
        exam_form = DiseaseHistoryForm(initial={
                'child': child,
                'child_id': child_id,
                'date': datetime.date.today(),
            }, instance=exam
        )
        signature_form = SignatureForm(instance=signature)
    exam_list = DiseaseHistory.objects.filter(child_id=child_id)
    context = {
        'child': child,
        'child_id': child_id,
        'exam_id': exam.id,
        'residence_id': child.residence_id,
        'disease_history_form': exam_form.as_ul,
        'signature_form': signature_form.as_ul,
        'DiseaseHistories': exam_list,
    }
    return render(request, 'tracker/edit_disease_history.html', context)

