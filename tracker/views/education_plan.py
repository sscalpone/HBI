# coding=utf-8

import datetime

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from tracker.models import EducationPlan, EducationPlanForm
from tracker.models import SignatureForm
from tracker.models import Child


"""The new() function creates and processes a new EducationPlan form. It
then creates a new EducationPlan object from the EducationPlan model,
populates it with the form info, and saves it to the database. It does
the same with a Signature form, which is indexed in the EducationPlan
object, along with the Child object. It also generates a list of past
dental exam forms filled out for this child, which can be viewed from
this template. It is protected with the login_required decorator, so
that no one who isn't logged in can add a form. The new() function
renders the add_education_plan template.
"""

@login_required
def new(request, child_id):
    child = get_object_or_404(Child, pk=child_id)

    # If POST request, get posted exam and signature form.
    if (request.POST):
        signature_form = SignatureForm(request.POST, request.FILES,
                                       request=request)
        exam_form = EducationPlanForm(request.POST, request.FILES,
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
        # EducationPlan and Signature objects, populate them with said
        # forms, and save them.
        else:
            if (signature_form.is_valid() and exam_form.is_valid()):
                saved_signature = signature_form.cleaned_data

                # Check that signature object is saved
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
                    saved_exam.save()
                    exam_form.save_m2m()

                    # Check that exam object saved
                    if (saved_exam):

                        # If user clicked 'save', render
                        # edit_education_plan template.
                        if ('save' in request.POST):
                            return HttpResponseRedirect(
                                reverse('tracker:edit_education_plan',
                                        kwargs={
                                            'child_id': child_id,
                                            'exam_id': saved_exam.id
                                        }))

                        # If user clicked 'submit', render
                        # add_education_plan template.
                        else:
                            return HttpResponseRedirect(
                                reverse('tracker:new_education_plan',
                                        kwargs={'child_id': child_id}))

                    # If validation passed but exam still didn't save,
                    # return to add_education_plan template with "Sorry,
                    # please try again" error message
                    else:
                        return render(request,
                                      'tracker/add_exam.html',
                                      {'error_message': 'Lo sentimos, el '
                                       'formulario no se puede guardar en '
                                       'este momento. Por favor, vuelva a '
                                       'intentarlo.', })

                # If validation passed but signature still didn't
                # save,return to add_education_plan template with "Sorry,
                # please try again" error message
                else:
                    return render(request, 'tracker/add_exam.html',
                                  {'error_message': 'Lo sentimos, el '
                                   'formulario no se puede guardar en este '
                                   'momento. Por favor, vuelva a '
                                   'intentarlo.', })

    # If not POST request, create new EducationPlan form and Signature
    # form.
    else:
        exam_form = EducationPlanForm(
            initial={
                'child': child,
                'child_id': child_id,
                'date': datetime.date.today(),
            })
        signature_form = SignatureForm()

    # Render add_education_plan template
    education_plan_list = EducationPlan.objects.filter(child_id=child_id)
    context = {
        'child': child,
        'child_id': child_id,
        'residence_id': child.residence_id,
        'exam_form': exam_form.as_ul,
        'signature_form': signature_form.as_ul,
        'ExamList': education_plan_list,
        'page': 'education_plan',
        'name': 'Area Pedagógica',
        # 'exam': True,
    }
    return render(request, 'tracker/add_exam.html', context)


"""The view() function renders the education_plan template, populated
with information from the EducationPlan model. It is protected with the
login_required decorator, so that no one who isn't logged in can add a
form.
"""

@login_required
def view(request, child_id, exam_id):
    exam = get_object_or_404(EducationPlan, pk=exam_id)
    child = get_object_or_404(Child, pk=child_id)
    if (request.POST):
        # After confirmation, delete photo and render the
        # add_photograph template
        if ('discard' in request.POST):
            exam.delete()
            return HttpResponseRedirect(reverse('tracker:new_education_plan',
                                        kwargs={'child_id': child_id}))

    context = {
        'exam': exam,
        'child': child,
        'child_id': child.id,
        'residence_id': child.residence_id,
        'page': 'education_plan',
        # 'exam': True,
    }
    return render(request, 'tracker/education_plan.html', context)


"""The edit() function creates and processes a EducationPlan form
populated with an existing EducationPlan object information. It then adds
the edits to the EducationPlan object and saves it to the database. It
does the same with a Signature form, which is indexed in the
EducationPlan object, along with the Child object. It is protected with
the login_required decorator, so that no one who isn't logged in can
add a form. The edit() function renders the edit_education_plan template.
"""

@login_required
def edit(request, child_id, exam_id):
    child = get_object_or_404(Child, pk=child_id)
    exam = get_object_or_404(EducationPlan, pk=exam_id)

    # If POST request, get posted exam and signature form.
    if (request.POST):
        signature_form = SignatureForm(request.POST, request.FILES,
                                       request=request)
        exam_form = EducationPlanForm(request.POST, request.FILES,
                                      instance=exam, request=request)

        # If user clicked discard button, discard posted form and
        # render the child_information template.
        if ('discard' in request.POST):
            return HttpResponseRedirect(
                reverse('tracker:child', kwargs={'child_id': child_id}))

        # If user clicked 'save' or 'submit', process and save forms
        # (form will validate no matter what in 'save', will be
        # validated in custom clean() in 'submit'), and edit and save
        # EducationPlan and Signature object.
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
                    saved_exam.save()
                    exam_form.save_m2m()

                    # Check that exam object saved
                    if (saved_exam):

                        # If user clicked 'save', render
                        # edit_education_plan template.
                        if ('save' in request.POST):
                            return HttpResponseRedirect(
                                reverse('tracker:edit_education_plan',
                                        kwargs={
                                            'child_id': child_id,
                                            'exam_id': saved_exam.id
                                        }))

                        # If user clicked 'submit', render
                        # add_education_plan template.
                        else:
                            return HttpResponseRedirect(
                                reverse('tracker:new_education_plan',
                                        kwargs={'child_id': child_id}))

                    # if validation passed but exam still didn't save,
                    # return to edit_education_plan template with "Sorry,
                    # please try again" error message
                    else:
                        return render(request,
                                      'tracker/edit_exam.html',
                                      {'error_message': 'Lo sentimos, el '
                                       'formulario no se puede guardar en '
                                       'este momento. Por favor, vuelva a '
                                       'intentarlo.', })

                # if validation passed but signature still didn't
                # save, return to edit_education_plan template with
                # "Sorry, please try again" error message
                else:
                    return render(request, 'tracker/edit_exam.html',
                                  {'error_message': 'Lo sentimos, el '
                                   'formulario no se puede guardar en este '
                                   'momento. Por favor, vuelva a '
                                   'intentarlo.', })

    # If not POST request, create new EducationPlan form and Signature
    # form, populated with the EducationPlan and Signature objects.
    else:
        exam_form = EducationPlanForm(instance=exam)
        signature_form = SignatureForm(initial={
            'signature_name': exam.signature_name,
            'signature_surname': exam.signature_surname,
            'signature_emp': exam.signature_emp,
            'signature_direction': exam.signature_direction,
            'signature_cell': exam.signature_cell,
        })

    # Render edit_education_plan template
    exam_list = EducationPlan.objects.filter(child_id=child_id)
    context = {
        'child': child,
        'child_id': child_id,
        'exam_id': exam.id,
        'residence_id': child.residence_id,
        'exam_form': exam_form.as_ul,
        'signature_form': signature_form.as_ul,
        'ExamList': exam_list,
        'page': 'education_plan',
        'name': 'Area Pedagógica',
        # 'exam': True,
    }
    return render(request, 'tracker/edit_exam.html', context)


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
        exam = get_object_or_404(EducationPlan, pk=exam_id)
        child = get_object_or_404(Child, pk=child_id)

        # On confirmation, delete object and load the add_photograph
        # template
        if ('discard' in request.POST):
            exam.delete()
            return HttpResponseRedirect(reverse('tracker:new_education_plan',
                                        kwargs={'child_id': child_id}))

        # If no confirmation, return to photograph template
        elif ('no' in request.POST):
            context = {
                'exam': exam,
                'child': child,
                'child_id': child.id,
                'residence_id': child.residence_id,
                'page': 'education_plan',
            }
            return render(request, 'tracker/education_plan.html', context)
