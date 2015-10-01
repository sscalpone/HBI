# coding=utf-8

import datetime

from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from django.shortcuts import render, get_object_or_404
from django.template import loader
import django.template.loader

import matplotlib.pyplot as plt
import matplotlib.pylab
import matplotlib.dates as mdates

from tracker.models import MedicalExamPart1, MedicalExamPart1Form
from tracker.models import Signature, SignatureForm
from tracker.models import Child

@login_required
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

@login_required
def new(request, child_id):
    child = get_object_or_404(Child, pk=child_id)
    
    if request.method == 'POST':
        signature_form = SignatureForm(request.POST, request.FILES, request=request)
        exam_form = MedicalExamPart1Form(request.POST, request.FILES, request=request)
        
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
                        return HttpResponseRedirect(reverse('tracker:edit_medical_exam_part1', kwargs={'child_id': child_id, 'exam_id': saved_exam.id}))
                    else:
                        return HttpResponseRedirect(reverse('tracker:new_medical_exam_part1', kwargs={'child_id': child_id}))
    
    else:
        exam_form = MedicalExamPart1Form(initial={
                'child': child,
                'child_id': child_id,
                'date': datetime.date.today(),
            }
        )
        signature_form = SignatureForm()
    exam_list = MedicalExamPart1.objects.filter(child_id=child_id)
    context = {
        'child': child,
        'child_id': child_id,
        'residence_id': child.residence_id,
        'medical_exam_part1_form': exam_form.as_ul,
        'signature_form': signature_form.as_ul,
        'MedicalExamPart1s': exam_list,
    }
    return render(request, 'tracker/add_medical_exam_part1.html', context)

@login_required
def view(request, child_id, exam_id):
    p = get_object_or_404(MedicalExamPart1, pk=exam_id)
    child = get_object_or_404(Child, pk=child_id)
    signature = get_object_or_404(Signature, pk=p.signature_id)
    context = {
        'exam': p,
        'child': child,
        'child_id': child.id,
        'residence_id': child.residence_id,
        'signature': signature,
    }
    return render(request, 'tracker/medical_exam_part1.html', context)

@login_required
def edit(request, child_id, exam_id):
    child = get_object_or_404(Child, pk=child_id)
    exam = get_object_or_404(MedicalExamPart1, pk=exam_id)
    signature = get_object_or_404(Signature, pk=exam.signature_id)
    if request.method == 'POST':
        signature_form = SignatureForm(request.POST, request.FILES, instance=signature, request=request)
        exam_form = MedicalExamPart1Form(request.POST, request.FILES, instance=exam, request=request)
        
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
                        return HttpResponseRedirect(reverse('tracker:edit_medical_exam_part1', kwargs={'child_id': child_id, 'exam_id': saved_exam.id}))
                    else:
                        return HttpResponseRedirect(reverse('tracker:new_medical_exam_part1', kwargs={'child_id': child_id}))
    
    else:
        exam_form = MedicalExamPart1Form(initial={
                'child': child,
                'child_id': child_id,
                'date': datetime.date.today(),
            }, instance=exam
        )
        signature_form = SignatureForm(instance=signature)
    exam_list = MedicalExamPart1.objects.filter(child_id=child_id)
    context = {
        'child': child,
        'child_id': child_id,
        'exam_id': exam.id,
        'residence_id': child.residence_id,
        'medical_exam_part1_form': exam_form.as_ul,
        'signature_form': signature_form.as_ul,
        'MedicalExamPart1s': exam_list,
    }
    return render(request, 'tracker/edit_medical_exam_part1.html', context)

def graph_height(request, child_id):
    exams = MedicalExamPart1.objects.filter(child_id=child_id)
    if exams:
        heights = list()
        dates = list()
        for exam in exams:
            heights.append(exam.height)
            dates.append(exam.date)
        years = mdates.YearLocator()
        months = mdates.MonthLocator()
        yearsFmt = mdates.DateFormatter('%Y')

        plt.gca().xaxis.set_major_formatter(yearsFmt)
        plt.gca().xaxis.set_major_locator(years)
        plt.plot(dates, heights)
        plt.gcf().autofmt_xdate()

        xlabel('Fecha (años)')
        ylabel('Altura (cm)')
        grid=true

        buffer = StringIO.StringIO()
        canvas = pylab.get_current_fig_manager().canvas
        canvas.draw()
        graphIMG = Image.fromstring("RGB", canvas.get_width_height(), canvas.tostring_rgb())
        graphIMG.save(buffer, "PNG")
        pylab.close()

        return render(request, 'tracker/height_chart.html', 'graphIMG')




def graph_weight(request, child_id):
    exams = MedicalExamPart1.objects.filter(child_id=child_id)
    weights = list()
    dates = list()
    for exam in exams:
        weights.append(exam.weight)
        dates.append(exam.date)

