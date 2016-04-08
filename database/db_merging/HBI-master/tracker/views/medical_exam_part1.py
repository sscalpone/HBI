# coding=utf-8

import datetime

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import loader

from matplotlib import pylab
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

from tracker.models import Child
from tracker.models import Growth
from tracker.models import MedicalExamPart1, MedicalExamPart1Form
from tracker.models import Signature, SignatureForm


"""The new() function creates and processes a new MedicalExamPart2 
form. It then creates a new MedicalExamPart2 object from the 
MedicalExamPart2 model, populates it with the form info, and saves it 
to the database. It does the same with a Signature form, which is 
indexed in the MedicalExamPart2 object, along with the Child object. 
It also generates a list of past MedicalExamPart2 forms filled out for 
this child, which can be viewed from this template. It is protected 
with the login_required decorator, so that no one who isn't logged in 
can add a form. The new() function renders the add_medical_exam_part2 
template.
"""
@login_required
def new(request, child_id):
    child = get_object_or_404(Child, pk=child_id)
    
    # If POST request, get posted exam and signature form.
    if (request.POST):
        signature_form = SignatureForm(request.POST, request.FILES, 
            request=request)
        exam_form = MedicalExamPart1Form(request.POST, request.FILES, 
            request=request)
        
        # If user clicked discard button, discard posted form and 
        # render the child_information template.
        if ('discard' in request.POST):
            return HttpResponseRedirect(reverse('tracker:child', 
                kwargs={'child_id': child_id}))
        
        # If user clicked 'save' or 'submit', process and save form 
        # (form will validate no matter what in 'save', will be 
        # validated in custom clean() in 'submit'), and create 
        # MedicalExamPart2 and Signature objects, populate them with 
        # said forms, and save them.
        else:
            if (signature_form.is_valid() and exam_form.is_valid()):
                saved_signature = signature_form.save()
                
                # Check that exam object saved
                if (saved_signature):
                    saved_exam = exam_form.save(commit=False)
                    saved_exam.signature = saved_signature
                    saved_exam.child = child
                    saved_exam.last_saved = datetime.datetime.utcnow()
                    saved_exam.save()
                    exam_form.save_m2m()

                    # Create and populate Growth object
                    growth = Growth.objects.create(
                        child=child, 
                        exam=saved_exam, 
                        date=saved_exam.date, 
                        height=saved_exam.height, 
                        weight=saved_exam.weight, 
                        age=child.age_in_years(
                            from_date=child.birthdate, 
                            to_date=saved_exam.date), 
                        gender=child.gender
                        )

                    # Check that exam object saved
                    if (saved_exam):

                        # If user clicked 'save', render 
                        # edit_medical_exam_part2 template.
                        if ('save' in request.POST):
                            return HttpResponseRedirect(
                                reverse('tracker:edit_medical_exam_part1', 
                                    kwargs={
                                        'child_id': child_id, 
                                        'exam_id': saved_exam.id
                                    }))

                        # If user clicked 'submit', render 
                        # add_medical_exam_part2 template.
                        else:
                            return HttpResponseRedirect(
                                reverse('tracker:new_medical_exam_part1', 
                                    kwargs={'child_id': child_id}))

                    # If validation passed but exam still didn't save, 
                    # return to add_medical_exam_part2 template with 
                    # "Sorry, please try again" error message
                    else:
                        return render(request, 
                            'tracker/add_medical_exam_part2.html', 
                            {
                             'error_message': 'Lo sentimos, el formulario no '
                             'se puede guardar en este momento. Por favor, '
                             'vuelva a intentarlo.',
                            })

                # If validation passed but signature still didn't 
                # save,return to add_medical_exam_part2 template with 
                # "Sorry, please try again" error message
                else:
                    return render(request, 'tracker/add_medical_exam_part2.html', 
                        {
                         'error_message': 'Lo sentimos, el formulario no se '
                         'puede guardar en este momento. Por favor, vuelva a '
                         'intentarlo.',
                        })

    # If not POST request, create new MedicalExamPart2 form and 
    # Signature form. 
    else:
        exam_form = MedicalExamPart1Form(initial={
                'child': child,
                'child_id': child_id,
                'date': datetime.date.today(),
            })
        signature_form = SignatureForm()

    # Render add_medical_exam_part2 template
    exam_list = MedicalExamPart1.objects.filter(child_id=child_id)
    context = {
        'child': child,
        'child_id': child_id,
        'residence_id': child.residence_id,
        'medical_exam_part1_form': exam_form.as_ul,
        'signature_form': signature_form.as_ul,
        'MedicalExamPart1s': exam_list,
        'page': 'medical_exam_part1',
        'exam': True,
    }
    return render(request, 'tracker/add_medical_exam_part1.html', context)


"""The view() function renders the medical_exam_part2 template, 
populated with information from the MedicalExamPart2 model. It is 
protected with the login_required decorator, so that no one who isn't 
logged in can add a form.
"""
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
        'page': 'medical_exam_part1',
        'exam': True,
    }
    return render(request, 'tracker/medical_exam_part1.html', context)


"""The edit() function creates and processes a MedicalExamPart2 form 
populated with an existing MedicalExamPart2 object information. It 
then adds the edits to the MedicalExamPart2 object and saves it to the 
database. It does the same with a Signature form, which is indexed in 
the MedicalExamPart2 object, along with the Child object. It is 
protected with the login_required decorator, so that no one who isn't 
logged in can add a form. The edit() function renders the 
edit_medical_exam_part2 template.
"""
@login_required
def edit(request, child_id, exam_id):
    child = get_object_or_404(Child, pk=child_id)
    exam = get_object_or_404(MedicalExamPart1, pk=exam_id)
    growth = get_object_or_404(Growth, exam_id=exam_id)
    signature = get_object_or_404(Signature, pk=exam.signature_id)

    # If POST request, get posted exam and signature form.
    if (request.POST):
        signature_form = SignatureForm(request.POST, request.FILES, 
            instance=signature, request=request)
        exam_form = MedicalExamPart1Form(request.POST, request.FILES, 
            instance=exam, request=request)
        
        # If user clicked discard button, discard posted form and 
        # render the child_information template.
        if ('discard' in request.POST):
            return HttpResponseRedirect(
                reverse('tracker:child', kwargs={'child_id': child_id}))
        
        # If user clicked 'save' or 'submit', process and save forms 
        # (form will validate no matter what in 'save', will be 
        # validated in custom clean() in 'submit'), and edit and save 
        # MedicalExamPart2 and Signature object.
        else:
            if (signature_form.is_valid() and exam_form.is_valid()):
                saved_signature = signature_form.save()
                
                # Check that signature object saved
                if (saved_signature):
                    saved_exam = exam_form.save(commit=False)
                    saved_exam.signature = saved_signature
                    saved_exam.child = child
                    saved_exam.last_saved = datetime.datetime.utcnow()
                    saved_exam.save()
                    exam_form.save_m2m()
                    
                    # Edit growth object
                    growth.child = child
                    growth.exam = saved_exam
                    growth.date = saved_exam.date
                    height=saved_exam.height
                    weight = saved_exam.weight
                    growth.age=child.age_in_years(from_date=child.birthdate, 
                        to_date=saved_exam.date)
                    growth.gender = child.gender
                    growth.save()

                    # Check that exam object saved
                    if (saved_exam):

                        # If user clicked 'save', render 
                        # edit_medical_exam_part2 template.
                        if ('save' in request.POST):
                            return HttpResponseRedirect(
                                reverse('tracker:edit_medical_exam_part1', 
                                    kwargs={
                                        'child_id': child_id, 
                                        'exam_id': saved_exam.id
                                    }))

                        # If user clicked 'submit', render 
                        # add_medical_exam_part2 template.
                        else:
                            return HttpResponseRedirect(
                                reverse('tracker:new_medical_exam_part1', 
                                    kwargs={'child_id': child_id}))

                    # if validation passed but exam still didn't save, 
                    # return to edit_medical_exam_part2 template with 
                    # "Sorry, please try again" error message
                    else:
                        return render(request, 'tracker/edit_medical_exam_part2.html', 
                            {
                             'error_message': 'Lo sentimos, el formulario no '
                             'se puede guardar en este momento. Por favor, '
                             'vuelva a intentarlo.',
                            })

                # if validation passed but signature still didn't 
                # save, return to edit_medical_exam_part2 template 
                # with "Sorry, please try again" error message
                else:
                    return render(request, 'tracker/edit_medical_exam_part2.html', 
                        {
                         'error_message': 'Lo sentimos, el formulario no se '
                         'puede guardar en este momento. Por favor, vuelva a '
                         'intentarlo.',
                        })
    
    # If not POST request, create new MedicalExamPart2 form and 
    # Signature form, populated with the MedicalExamPart2 and 
    # Signature objects. 
    else:
        exam_form = MedicalExamPart1Form(instance=exam)
        signature_form = SignatureForm(instance=signature)

    # Render edit_medical_exam_part2 template
    exam_list = MedicalExamPart1.objects.filter(child_id=child_id)
    context = {
        'child': child,
        'child_id': child_id,
        'exam_id': exam.id,
        'residence_id': child.residence_id,
        'medical_exam_part1_form': exam_form.as_ul,
        'signature_form': signature_form.as_ul,
        'MedicalExamPart1s': exam_list,
        'page': 'medical_exam_part1',
        'exam': True,
    }
    return render(request, 'tracker/edit_medical_exam_part1.html', context)

"""growth_png() creates a graph of the children's height and weight 
and compares it to the average heights and weights of children around 
the world. It uses the matplotlib library to create a png image.
"""
def growth_png(request, child_id):
    child = get_object_or_404(Child, pk=child_id)
    growth = Growth.objects.filter(child_id=child_id)
    child_age = child.age()
    age=list()
    weight=list()
    height=list()
    
    avg_age=list()
    avg_weight=list()
    avg_height=list()
    if (child.gender == 'm'):
        avg_height_list = ([0, 50.0],[1, 76.1],[2, 86.5],[3, 95.3],[4, 102.5],[5, 109.7],[6, 115.7],[7, 122.0],[8, 128.1],[9, 133.7],[10, 138.8],[11, 143.7],[12, 149.3],[13, 156.4],[14, 164.1],[15, 170.1],[16, 173.6],[17, 175.3],[18, 176.2],[19, 176.6],[20, 176.8])
        avg_weight_list = ([0, 3.5],[1, 10.5],[2, 12.7],[3, 14.4],[4, 16.3],[5, 18.5],[6, 20.8],[7, 23.2],[8, 25.8],[9, 28.7],[10, 32.1],[11, 36.1],[12, 40.7],[13, 45.6],[14, 51.2],[15, 56.5],[16, 61.1],[17, 64.7],[18, 67.3],[19, 69.2],[20, 70.6])
    if (child.gender == 'f'):
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
    expected_arc = mpatches.Patch(color='#666666', label='Arco Esperado')
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


"""graph_growth() renders the growth_graph template, which displays 
the graph image created in graph_png().
"""
def graph_growth(request, child_id):
    child = get_object_or_404(Child, pk=child_id)
    context = {
        'child': child,
        'child_id': child.id,
        'residence_id': child.residence_id,
        'page': 'growth_graph',
    }
    return render(request, 'tracker/growth_graph.html', context)

