# coding=utf-8

import datetime

from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import loader
import django.template.loader

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import pylab
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from tracker.models import MedicalExamPart1, MedicalExamPart1Form
from tracker.models import Growth
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
                    growth = Growth.objects.create(child=child, exam=saved_exam, date=saved_exam.date, height=saved_exam.height, weight=saved_exam.weight, age=child.age_in_years(from_date=child.birthdate, to_date=saved_exam.date), gender=child.gender)

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
    growth = get_object_or_404(Growth, exam_id=exam_id)
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
                    
                    growth.child = child
                    growth.exam = saved_exam
                    growth.date = saved_exam.date
                    height=saved_exam.height
                    weight = saved_exam.weight
                    growth.age=child.age_in_years(from_date=child.birthdate, to_date=saved_exam.date)
                    growth.gender = child.gender
                    growth.save() 
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

def growth_png(request, child_id):
    child = get_object_or_404(Child, pk=child_id)
    growth = Growth.objects.filter(child_id=child_id)
    child_age = child.age()
    print child_age
    age=list()
    weight=list()
    height=list()
    
    avg_age=list()
    avg_weight=list()
    avg_height=list()
    if child.gender == 'm':
        avg_height_list = ([0, 50.0],[1, 76.1],[2, 86.5],[3, 95.3],[4, 102.5],[5, 109.7],[6, 115.7],[7, 122.0],[8, 128.1],[9, 133.7],[10, 138.8],[11, 143.7],[12, 149.3],[13, 156.4],[14, 164.1],[15, 170.1],[16, 173.6],[17, 175.3],[18, 176.2],[19, 176.6],[20, 176.8])
        avg_weight_list = ([0, 3.5],[1, 10.5],[2, 12.7],[3, 14.4],[4, 16.3],[5, 18.5],[6, 20.8],[7, 23.2],[8, 25.8],[9, 28.7],[10, 32.1],[11, 36.1],[12, 40.7],[13, 45.6],[14, 51.2],[15, 56.5],[16, 61.1],[17, 64.7],[18, 67.3],[19, 69.2],[20, 70.6])
    if child.gender == 'f':
        avg_weight_list = ([0, 3.4],[1, 9.7],[2, 12.1],[3, 13.9],[4, 15.9],[5, 18.0],[6, 20.3],[7, 22.9],[8, 25.8],[9, 29.1],[10, 33.1],[11, 37.8],[12, 41.8],[13, 46.0],[14, 49.5],[15, 52.1],[16, 53.9],[17, 55.2],[18, 56.2],[19, 57.4],[20, 58.2])
        avg_height_list = ([0, 49.2],[1, 74.4],[2, 85.0],[3, 94.2],[4, 101.0],[5, 108.0],[6, 115.0],[7, 121.8],[8, 127.8],[9, 133.1],[10, 138.2],[11, 144.3],[12, 151.3],[13, 157.3],[14, 160.5],[15, 161.9],[16, 162.6],[17, 162.9],[18, 163.1],[19, 163.2],[20, 163.3])
    
    for instance in growth:
        age.append(instance.age)
        height.append(instance.height)
        weight.append(instance.weight)

    for item in avg_height_list:
        if item[0] in age:
            avg_height.append(item[1])
    for item in avg_weight_list:
        if item[0] in age:
            avg_weight.append(item[1])

    child_arc = mpatches.Patch(color='#95bcf2', label='Arco Nino')
    expected_arc = mpatches.Patch(color='#666666', label='Esperado Nino')
    plt.subplot(211)
    plt.plot(age, height, color='#95bcf2', marker='.')
    plt.plot(age, avg_height, color='#666666', marker='.')
    plt.xlabel('Anos')
    plt.ylabel('Estatura (cm)')
    plt.legend(handles=[child_arc, expected_arc], loc=4)
    
    plt.subplot(212)
    plt.plot(age, weight, color='#95bcf2', marker='.')
    plt.plot(age, avg_weight, color='#666666', marker='.')
    plt.xlabel('Anos')
    plt.ylabel('Peso (kg)')
    plt.legend(handles=[child_arc, expected_arc], loc=4)


    canvas = FigureCanvas(plt.figure(1))
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response

def graph_growth(request, child_id):
    child = get_object_or_404(Child, pk=child_id)
    context = {
        'child': child,
        'child_id': child.id,
        'residence_id': child.residence_id,
    }
    return render(request, 'tracker/growth_graph.html', context)

