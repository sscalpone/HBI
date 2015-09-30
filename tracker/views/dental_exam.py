# coding=utf-8

import datetime

from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from django.shortcuts import render, get_object_or_404
from django.template import loader
import django.template.loader

from tracker.models import DentalExam, DentalExamForm
from tracker.models import Signature, SignatureForm
from tracker.models import Child

@login_required
def index(request, child_id):
    list = DentalExam.objects.filter(child_id=child_id)
    child = get_object_or_404(Child, pk=child_id)
    context = {
        'DentalExams': list,
        'child': child,
        'child_id': child_id,
        'residence_id': child.residence_id,
    }
    return render(request, 'tracker/add_dental_exam.html', context)

@login_required
def new(request, child_id):
    child = get_object_or_404(Child, pk=child_id)
    if request.method == 'POST':
        signature_form = SignatureForm(request.POST, request.FILES, request=request)
        exam_form = DentalExamForm(request.POST, request.FILES, request=request)
        if 'discard' in request.POST:
            messages.add_message(request, messages.SUCCESS, 'Con éxito desechada información.')
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
                        messages.add_message(request, messages.SUCCESS, 'Guardado correctamente la información.')
                        return HttpResponseRedirect(reverse('tracker:edit_dental_exam', kwargs={'child_id': child_id, 'exam_id': saved_exam.id}))
                    else:
                        messages.add_message(request, messages.SUCCESS, 'Enviado correctamente la información.')
                        return HttpResponseRedirect(reverse('tracker:new9_dental_exam', kwargs={'child_id': child_id}))     
    else:
        exam_form = DentalExamForm(initial={
                'child': child,
                'child_id': child_id,
                'date': datetime.date.today(),
            }
        )
        signature_form = SignatureForm()
    dental_exam_list = DentalExam.objects.filter(child_id=child_id)
    context = {
        'child': child,
        'child_id': child_id,
        'residence_id': child.residence_id,
        'dental_exam_form': exam_form.as_ul,
        'signature_form': signature_form.as_ul,
        'DentalExams': dental_exam_list,
    }
    return render(request, 'tracker/add_dental_exam.html', context)

@login_required
def view(request, child_id, exam_id):
    p = get_object_or_404(DentalExam, pk=exam_id)
    child = get_object_or_404(Child, pk=child_id)
    signature = get_object_or_404(Signature, pk=p.signature_id)
    context = {
        'exam': p,
        'child': child,
        'child_id': child.id,
        'residence_id': child.residence_id,
        'signature': signature
    }
    return render(request, 'tracker/dental_exam.html', context)

@login_required
def edit(request, child_id, exam_id):
    child = get_object_or_404(Child, pk=child_id)
    exam = get_object_or_404(DentalExam, pk=exam_id)
    signature = get_object_or_404(Signature, pk=exam.signature_id)
    if request.method == 'POST':
        signature_form = SignatureForm(request.POST, request.FILES, instance=signature, request=request)
        exam_form = DentalExamForm(request.POST, request.FILES, instance=exam, request=request)
        
        if 'discard' in request.POST:
            messages.add_message(request, messages.SUCCESS, 'Con éxito desechada información.')
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
                        messages.add_message(request, messages.SUCCESS, 'Guardado correctamente la información.')
                        return HttpResponseRedirect(reverse('tracker:edit_dental_exam', kwargs={'child_id': child_id, 'exam_id': saved_exam.id}))
                    else:
                        messages.add_message(request, messages.SUCCESS, 'Enviado correctamente la información.')
                        return HttpResponseRedirect(reverse('tracker:new_dental_exam', kwargs={'child_id': child_id}))  
        
    else:
        exam_form = DentalExamForm(initial={
                'child': child,
                'child_id': child_id,
                'date': datetime.date.today(),
            }, instance=exam
        )
        signature_form = SignatureForm(instance=signature)
    exam_list = DentalExam.objects.filter(child_id=child_id)
    context = {
        'child': child,
        'child_id': child_id,
        'exam_id': exam.id,
        'residence_id': child.residence_id,
        'dental_exam_form': exam_form.as_ul,
        'signature_form': signature_form.as_ul,
        'DentalExams': exam_list,
    }
    return render(request, 'tracker/edit_dental_exam.html', context)

