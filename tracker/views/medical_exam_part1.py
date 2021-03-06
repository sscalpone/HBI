# coding=utf-8

import datetime
import numpy as np
from dateutil.relativedelta import relativedelta

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

from tracker.models import Child
from tracker.models import MedicalExamPart1, MedicalExamPart1Form
from tracker.models import SignatureForm

import who_stats


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
            return HttpResponseRedirect(
                reverse('tracker:child',
                        kwargs={'child_id': child_id}
                        ))

        # If user clicked 'save' or 'submit', process and save form
        # (form will validate no matter what in 'save', will be
        # validated in custom clean() in 'submit'), and create
        # MedicalExamPart2 and Signature objects, populate them with
        # said forms, and save them.
        else:
            if (signature_form.is_valid() and exam_form.is_valid()):
                saved_signature = signature_form.cleaned_data

                # Check that exam object saved
                if (saved_signature):
                    saved_exam = exam_form.save(commit=False)
                    saved_exam.signature_name = saved_signature[
                        'signature_name']
                    saved_exam.signature_surname = saved_signature[
                        'signature_surname']
                    saved_exam.signature_emp = saved_signature[
                        'signature_emp']
                    saved_exam.signature_direction = saved_signature[
                        'signature_direction']
                    saved_exam.signature_cell = saved_signature[
                        'signature_cell']
                    saved_exam.child = child
                    saved_exam.last_saved = datetime.datetime.utcnow()
                    if (saved_exam.weight and saved_exam.height):
                        saved_exam.bmi = round(saved_exam.weight
                                               / (saved_exam.height/100
                                                  * saved_exam.height/100), 2)
                    saved_exam.save()
                    exam_form.save_m2m()

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
                        return render(
                            request,
                            'tracker/add_exam.html',
                            {'error_message': 'Lo sentimos, el formulario no '
                             'se puede guardar en este momento. Por favor, '
                             'vuelva a intentarlo.', })

                # If validation passed but signature still didn't
                # save,return to add_medical_exam_part2 template with
                # "Sorry, please try again" error message
                else:
                    return render(request,
                                  'tracker/add_exam.html',
                                  {'error_message': 'Lo sentimos, el '
                                   'formulario no se puede guardar en este '
                                   'momento. Por favor, vuelva a '
                                   'intentarlo.', })

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
        'exam_form': exam_form.as_ul,
        'signature_form': signature_form.as_ul,
        'ExamList': exam_list,
        'page': 'medical_exam_part1',
        'name': 'Nuevo Informe Médico / Parte 1',
        # 'exam': True,
    }
    return render(request, 'tracker/add_exam.html', context)


"""The view() function renders the medical_exam_part2 template,
populated with information from the MedicalExamPart2 model. It is
protected with the login_required decorator, so that no one who isn't
logged in can add a form.
"""

@login_required
def view(request, child_id, exam_id):
    exam = get_object_or_404(MedicalExamPart1, pk=exam_id)
    child = get_object_or_404(Child, pk=child_id)
    if (request.POST):
        # After confirmation, delete photo and render the
        # add_photograph template
        if ('discard' in request.POST):
            exam.delete()
            return HttpResponseRedirect(
                reverse('tracker:new_medical_exam_part1',
                        kwargs={'child_id': child_id}))

    context = {
        'exam': exam,
        'child': child,
        'child_id': child.id,
        'residence_id': child.residence_id,
        'page': 'medical_exam_part1',
        # 'exam': True,
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

    # If POST request, get posted exam and signature form.
    if (request.POST):
        signature_form = SignatureForm(request.POST, request.FILES,
                                       request=request)
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
                saved_signature = signature_form.cleaned_data

                # Check that signature object saved
                if (saved_signature):
                    saved_exam = exam_form.save(commit=False)
                    saved_exam.signature_name = saved_signature[
                        'signature_name']
                    saved_exam.signature_surname = saved_signature[
                        'signature_surname']
                    saved_exam.signature_emp = saved_signature[
                        'signature_emp']
                    saved_exam.signature_direction = saved_signature[
                        'signature_direction']
                    saved_exam.signature_cell = saved_signature[
                        'signature_cell']
                    saved_exam.child = child
                    saved_exam.last_saved = datetime.datetime.utcnow()
                    if (saved_exam.weight and saved_exam.height):
                        saved_exam.bmi = round(saved_exam.weight
                                               / (saved_exam.height/100
                                                  * saved_exam.height/100), 2)
                    saved_exam.save()
                    exam_form.save_m2m()

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
                        return render(request,
                                      'tracker/edit_exam.html',
                                      {'error_message': 'Lo sentimos, el '
                                       'formulario no se puede guardar en '
                                       'este momento. Por favor, vuelva a '
                                       'intentarlo.', })

                # if validation passed but signature still didn't
                # save, return to edit_medical_exam_part2 template
                # with "Sorry, please try again" error message
                else:
                    return render(request,
                                  'tracker/edit_exam.html',
                                  {'error_message': 'Lo sentimos, el '
                                   'formulario no se puede guardar en este '
                                   'momento. Por favor, vuelva a '
                                   'intentarlo.', })

    # If not POST request, create new MedicalExamPart2 form and
    # Signature form, populated with the MedicalExamPart2 and
    # Signature objects.
    else:
        exam_form = MedicalExamPart1Form(instance=exam)
        signature_form = SignatureForm(initial={
            'signature_name': exam.signature_name,
            'signature_surname': exam.signature_surname,
            'signature_emp': exam.signature_emp,
            'signature_direction': exam.signature_direction,
            'signature_cell': exam.signature_cell,
            })

    # Render edit_medical_exam_part2 template
    exam_list = MedicalExamPart1.objects.filter(child_id=child_id)
    context = {
        'child': child,
        'child_id': child_id,
        'exam_id': exam.id,
        'residence_id': child.residence_id,
        'exam_form': exam_form.as_ul,
        'signature_form': signature_form.as_ul,
        'ExamList': exam_list,
        'page': 'medical_exam_part1',
        'name': 'Nuevo Informe Médico / Parte 1',
        # 'exam': True,
    }
    return render(request, 'tracker/edit_exam.html', context)


def age_in_months(f_date, t_date):
    r = relativedelta(t_date, f_date)
    months = r.years * 12 + r.months + r.days/30.
    return int(months)


"""growth_png() creates a graph of the children's height and weight
and compares it to the average heights and weights of children around
the world. It uses the matplotlib library to create a png image.
"""

def growth_png(request, child_id):
    child = get_object_or_404(Child, pk=child_id)
    exams = MedicalExamPart1.objects.filter(child_id=child_id)
    age = []
    weight = []
    height = []
    bmi = []

    avg_weight_age = []
    avg_weight = []
    avg_height_age = []
    avg_height = []
    avg_bmi_age = []
    avg_bmi = []

    if (child.gender == 'm'):
        avg_bmi_list = who_stats.boys_bmi
        avg_height_list = who_stats.boys_height
        avg_weight_list = who_stats.boys_weight

    if (child.gender == 'f'):
        avg_bmi_list = who_stats.girls_bmi
        avg_height_list = who_stats.girls_height
        avg_weight_list = who_stats.girls_weight

    for exam in exams:
        age.append(age_in_months(child.birthdate, exam.date))
        height.append(exam.height)
        weight.append(exam.weight)
        bmi.append(exam.bmi)

    np_age = np.array(age)
    np_height = np.array(height)
    np_weight = np.array(weight)
    np_bmi = np.array(bmi)

    age_length = len(age)

    if exams:
        for item in avg_height_list:
            if item[0] > age[0] and item[0] < age[age_length-1]:
                avg_height_age.append(item[0])
                avg_height.append(item[1])
        for item in avg_weight_list:
            if item[0] > age[0] and item[0] < age[age_length-1]:
                avg_weight_age.append(item[0])
                avg_weight.append(item[1])
        for item in avg_bmi_list:
            if item[0] > age[0] and item[0] < age[age_length-1]:
                avg_bmi_age.append(item[0])
                avg_bmi.append(item[1])

    np_avg_height_age = np.array(avg_height_age)
    np_avg_height = np.array(avg_height)
    np_avg_weight_age = np.array(avg_weight_age)
    np_avg_weight = np.array(avg_weight)
    np_avg_bmi_age = np.array(avg_bmi_age)
    np_avg_bmi = np.array(avg_bmi)

    child_arc = mpatches.Patch(color='#95bcf2', label='Arco Nino')
    expected_arc = mpatches.Patch(color='#666666', label='Arco Esperado')

    plt.figure(figsize=(7, 10))

    plt.subplot(311)
    plt.plot(np_age, np_height, color='#95bcf2', marker='.')
    plt.plot(np_avg_height_age, np_avg_height, color='#666666', marker='')
    plt.xlabel('Edad en Meses')
    plt.ylabel('Estatura (cm)')
    plt.legend(handles=[child_arc, expected_arc], loc=4)

    plt.subplot(312)
    plt.plot(np_age, np_weight, color='#95bcf2', marker='.')
    plt.plot(np_avg_weight_age, np_avg_weight, color='#666666', marker='')
    plt.xlabel('Edad en Meses')
    plt.ylabel('Peso (kg)')
    plt.legend(handles=[child_arc, expected_arc], loc=4)

    plt.subplot(313)
    plt.plot(np_age, np_bmi, color='#95bcf2', marker='.')
    plt.plot(np_avg_bmi_age, np_avg_bmi, color='#666666', marker='')
    plt.xlabel('Edad en Meses')
    plt.ylabel('IMC')
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


"""The delete() function confirms with the user that a photograph
should be deleted, and then deletes the objects from the database.
This function is unused as long as javascript is enabled, as the
deletion process is done in the view() function, and the form is
rendered in a jQueryUI dialog box. This function is kept merely as a
precaution/so that it can be rebuilt for other objects without needing
to parse the view() object too carefully.
"""

def delete(request, child_id, exam_id):
    # If POST request, get Photograph object, confirm deletion with
    # user, and delete object
    if (request.POST):
        exam = get_object_or_404(MedicalExamPart1, pk=exam_id)
        child = get_object_or_404(Child, pk=child_id)

        # On confirmation, delete object and load the add_photograph
        # template
        if ('discard' in request.POST):
            exam.delete()
            return HttpResponseRedirect(
                reverse('tracker:new_medical_exam_part1',
                        kwargs={'child_id': child_id}))

        # If no confirmation, return to photograph template
        elif ('no' in request.POST):
            context = {
                'exam': exam,
                'child': child,
                'child_id': child.id,
                'residence_id': child.residence_id,
                'page': 'medical_exam_part1',
            }
            return render(request, 'tracker/medical_exam_part1.html', context)
