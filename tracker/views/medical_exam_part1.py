import datetime

from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.shortcuts import render, get_object_or_404
from django.template import loader
import django.template.loader

from tracker.models import MedicalExamPart1, MedicalExamPart1Form
from tracker.models import Signature, SignatureForm
from tracker.models import Child

def index(request, child_id):
    list = MedicalExamPart1.objects.filter(child_id=child_id)
    child = get_object_or_404(Child, pk=child_id)
    context = {
        'MedicalExamPart1s': list,
        'child_id': child_id,
        'child': child,
        'residence_id': child.residence_id,
    }
    return render(request, 'tracker/add_medical_exam_part1.html', context)

def new(request, child_id):
    child = get_object_or_404(Child, pk=child_id)
    
    if request.method == 'POST':
        signature_form = SignatureForm(request.POST, request.FILES, request=request)
        medical_exam_part1_form = MedicalExamPart1Form(request.POST, request.FILES, request=request)
        
        if 'discard' in request.POST:
            return HttpResponseRedirect(reverse('tracker:child', kwargs={'child_id': child_id}))
        
        else:
            if signature_form.is_valid() and medical_exam_part1_form.is_valid():
                signature = signature_form.save()
                
                if signature:
                    medical_exam_part1 = medical_exam_part1_form.save(commit=False)
                    medical_exam_part1.signature = signature
                    medical_exam_part1.child = child
                    medical_exam_part1.save()
                    medical_exam_part1_form.save_m2m()
                    return HttpResponseRedirect(reverse('tracker:child', kwargs={'child_id': child_id}))
    
    else:
        medical_exam_part1_form = MedicalExamPart1Form(initial={
                'child': child,
                'child_id': child_id,
                'date': datetime.date.today(),
            }
        )
        signature_form = SignatureForm()
    medical_exam_part_1_list = MedicalExamPart1.objects.filter(child_id=child_id)
    context = {
        'child': child,
        'child_id': child_id,
        'residence_id': child.residence_id,
        'medical_exam_part1_form': medical_exam_part1_form.as_ul,
        'signature_form': signature_form.as_ul,
        'MedicalExamPart1s': medical_exam_part_1_list,
    }
    return render(request, 'tracker/add_medical_exam_part1.html', context)

def view(request, child_id, exam_id):
    p = get_object_or_404(MedicalExamPart1, pk=exam_id)
    child = get_object_or_404(Child, pk=exam_id)
    signature = get_object_or_404(Signature, pk=p.signature_id)
    context = {
        'exam': p,
        'child': child,
        'child_id': child.id,
        'residence_id': child.residence_id,
        'signature': signature,
    }
    return render(request, 'tracker/medical_exam_part1.html', context)

def edit(request, child_id, exam_id):
    child = get_object_or_404(Child, pk=child_id)
    exam = get_object_or_404(MedicalExamPart1, pk=exam_id)
    signature = get_object_or_404(Signature, pk=exam.signature_id)
    if request.method == 'POST':
        signature_form = SignatureForm(request.POST, request.FILES, instance=signature, request=request)
        medical_exam_part1_form = MedicalExamPart1Form(request.POST, request.FILES, instance=exam, request=request)
        
        if 'discard' in request.POST:
            return HttpResponseRedirect(reverse('tracker:child', kwargs={'child_id': child_id}))
        
        else:
            if signature_form.is_valid() and medical_exam_part1_form.is_valid():
                saved_signature = signature_form.save()
                
                if saved_signature:
                    medical_exam_part1 = medical_exam_part1_form.save(commit=False)
                    medical_exam_part1.signature = saved_signature
                    medical_exam_part1.child = child
                    medical_exam_part1.save()
                    medical_exam_part1_form.save_m2m()
                    return HttpResponseRedirect(reverse('tracker:child', kwargs={'child_id': child_id}))
    
    else:
        medical_exam_part1_form = MedicalExamPart1Form(initial={
                'child': child,
                'child_id': child_id,
                'date': datetime.date.today(),
            }, instance=exam
        )
        signature_form = SignatureForm(instance=signature)
    medical_exam_part_1_list = MedicalExamPart1.objects.filter(child_id=child_id)
    context = {
        'child': child,
        'child_id': child_id,
        'exam_id': exam.id,
        'residence_id': child.residence_id,
        'medical_exam_part1_form': medical_exam_part1_form.as_ul,
        'signature_form': signature_form.as_ul,
        'MedicalExamPart1s': medical_exam_part_1_list,
    }
    return render(request, 'tracker/edit_medical_exam_part1.html', context)




