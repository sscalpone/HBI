# coding=utf-8

import datetime

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader

from tracker.models import Child
from tracker.models import MedicalExamPart2, MedicalExamPart2Form
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
    if request.POST:
        signature_form = SignatureForm(request.POST, request.FILES, 
            request=request)
        exam_form = MedicalExamPart2Form(request.POST, request.FILES, 
            request=request)

        # If user clicked discard button, discard posted form and 
        # render the child_information template.
        if 'discard' in request.POST:
            return HttpResponseRedirect(reverse('tracker:child', 
                kwargs={'child_id': child_id}))
        
        # If user clicked 'save' or 'submit', process and save form 
        # (form will validate no matter what in 'save', will be 
        # validated in custom clean() in 'submit'), and create 
        # MedicalExamPart2 and Signature objects, populate them with 
        # said forms, and save them.
        else:
            if signature_form.is_valid() and exam_form.is_valid():
                saved_signature = signature_form.save()
                
                # Check that signature object is saved
                if saved_signature:
                    saved_exam = exam_form.save(commit=False)
                    saved_exam.signature = saved_signature
                    saved_exam.child = child
                    saved_exam.last_saved = datetime.datetime.utcnow()
                    saved_exam.save()
                    exam_form.save_m2m()

                    # Check that exam object saved
                    if (saved_exam):

                        # If user clicked 'save', render 
                        # edit_medical_exam_part2 template.
                        if 'save' in request.POST:
                            return HttpResponseRedirect(
                                reverse('tracker:edit_medical_exam_part2', 
                                    kwargs={
                                        'child_id': child_id, 
                                        'exam_id': saved_exam.id,
                                    }))

                        # If user clicked 'submit', render 
                        # add_medical_exam_part2 template.
                        else:
                            return HttpResponseRedirect(reverse('tracker:new_medical_exam_part2', 
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
                    return render(request, 
                        'tracker/add_medical_exam_part2.html', 
                        {
                         'error_message': 'Lo sentimos, el formulario no se '
                         'puede guardar en este momento. Por favor, vuelva a '
                         'intentarlo.',
                        })
    
    # If not POST request, create new MedicalExamPart2 form and 
    # Signature form. 
    else:
        exam_form = MedicalExamPart2Form(
            initial={
                'child': child,
                'child_id': child_id,
                'date': datetime.date.today(),
            })
        signature_form = SignatureForm()

    # Render add_medical_exam_part2 template
    exam_list = MedicalExamPart2.objects.filter(child_id=child_id)
    context = {
        'child': child,
        'child_id': child_id,
        'residence_id': child.residence_id,
        'medical_exam_part2_form': exam_form.as_ul,
        'signature_form': signature_form.as_ul,
        'MedicalExamPart2s': exam_list,
        'page': 'medical_exam_part2',
    }
    return render(request, 'tracker/add_medical_exam_part2.html', context)


"""The view() function renders the medical_exam_part2 template, 
populated with information from the MedicalExamPart2 model. It is 
protected with the login_required decorator, so that no one who isn't 
logged in can add a form.
"""
@login_required
def view(request, child_id, exam_id):
    p = get_object_or_404(MedicalExamPart2, pk=exam_id)
    child = get_object_or_404(Child, pk=child_id)
    signature = get_object_or_404(Signature, pk=p.signature_id)
    context = {
        'exam': p,
        'child': child,
        'child_id': child.id,
        'residence_id': child.residence_id,
        'signature': signature,
        'page': 'medical_exam_part2',
    }
    return render(request, 'tracker/medical_exam_part2.html', context)


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
    exam = get_object_or_404(MedicalExamPart2, pk=exam_id)
    signature = get_object_or_404(Signature, pk=exam.signature_id)
    
    # If POST request, get posted exam and signature form.
    if (request.POST):
        signature_form = SignatureForm(request.POST, request.FILES, 
            instance=signature, request=request)
        exam_form = MedicalExamPart2Form(request.POST, request.FILES, 
            instance=exam, request=request)
        
        # If user clicked discard button, discard posted form and 
        # render the child_information template.
        if ('discard' in request.POST):
            return HttpResponseRedirect(reverse('tracker:child', 
                kwargs={'child_id': child_id}))
        
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
                    saved_exam.save()
                    exam_form.save_m2m()

                    # Check that exam object saved
                    if (saved_exam):

                        # If user clicked 'save', render 
                        # edit_medical_exam_part2 template.
                        if 'save' in request.POST:
                            return HttpResponseRedirect(
                                reverse('tracker:edit_medical_exam_part2', 
                                    kwargs={
                                        'child_id': child_id, 
                                        'exam_id': saved_exam.id
                                    }))
                        
                        # If user clicked 'submit', render 
                        # add_medical_exam_part2 template.
                        else:
                            return HttpResponseRedirect(
                                reverse('tracker:new_medical_exam_part2', 
                                    kwargs={'child_id': child_id}))

                    # if validation passed but exam still didn't save, 
                    # return to edit_medical_exam_part2 template with 
                    # "Sorry, please try again" error message
                    else:
                        return render(request, 
                            'tracker/edit_medical_exam_part2.html', 
                            {
                             'error_message': 'Lo sentimos, el formulario no '
                             'se puede guardar en este momento. Por favor, '
                             'vuelva a intentarlo.',
                            })

                # if validation passed but signature still didn't 
                # save, return to edit_medical_exam_part2 template 
                # with "Sorry, please try again" error message
                else:
                    return render(request, 
                        'tracker/edit_medical_exam_part2.html', 
                        {
                         'error_message': 'Lo sentimos, el formulario no se '
                         'puede guardar en este momento. Por favor, vuelva a '
                         'intentarlo.',
                        })
    
    # If not POST request, create new MedicalExamPart2 form and 
    # Signature form, populated with the MedicalExamPart2 and 
    # Signature objects. 
    else:
        exam_form = MedicalExamPart2Form(instance=exam)
        signature_form = SignatureForm(instance=signature)

    # Render edit_medical_exam_part2 template
    exam_list = MedicalExamPart2.objects.filter(child_id=child_id)
    context = {
        'child': child,
        'child_id': child_id,
        'residence_id': child.residence_id,
        'exam_id': exam.id,
        'medical_exam_part2_form': exam_form.as_ul,
        'signature_form': signature_form.as_ul,
        'MedicalExamPart2s': exam_list,
        'page': 'medical_exam_part2',
    }
    return render(request, 'tracker/edit_medical_exam_part2.html', context)




