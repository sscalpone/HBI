# coding=utf-8

import datetime

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader

from tracker.models import Child
from tracker.models import Photograph, PhotographForm


"""The new() function creates and processes a new Photograph form.
It then creates a new Photograph object from the Photograph
model, populates it with the form info, and saves it to the database. 
A Child object is indexed in the Photograph object. It also generates 
a list of past photograph forms filled out for this child, which 
can be viewed from this template. Itis protected with the 
login_required decorator, so that no one who isn't logged in can add a
form. The new() function renders the add_photograph template.
"""
@login_required
def new(request, child_id):
    child = get_object_or_404(Child, pk=child_id)

    # If POST request, get posted photograph
    if (request.POST):
        exam_form = PhotographForm(request.POST, request.FILES, 
            request=request)

        # If user clicked discard button, discard posted form and 
        # render the child_information template.
        if ('discard' in request.POST):
            return HttpResponseRedirect(reverse('tracker:child', 
                kwargs={'child_id': child_id}))

        # If user clicked 'save' or 'submit', process and save form 
        # (form will validate no matter what in 'save', will be 
        # validated in custom clean() in 'submit'), and create 
        # Photograph and Signature objects, populate them with said 
        # forms, and save them.
        else:
            if (exam_form.is_valid()):
                saved_exam = exam_form.save(commit=False)
                saved_exam.child = child
                saved_exam.last_saved = datetime.datetime.utcnow()
                saved_exam.save()
                exam_form.save_m2m()

                # Check that photograph object saved
                if (saved_exam):

                    # If user clicked 'save', render edit_photograph
                    # template.
                    if ('save' in request.POST):
                        return HttpResponseRedirect(
                            reverse('tracker:edit_photo', 
                                kwargs={
                                    'child_id': child_id, 
                                    'exam_id': saved_exam.id
                                }))

                    # If user clicked 'submit', render add_photograph
                    # template.
                    else:
                        return HttpResponseRedirect(reverse('tracker:new_photo', kwargs={'child_id': child_id}))     

                # if validation passed but photograph still didn't 
                # save, return to add_photograph template with 
                # "Sorry, please try again" error message
                else:
                    return render(request, 
                        'tracker/add_photograph.html', 
                        {
                         'error_message': 'Lo sentimos, el formulario no '
                         'se puede guardar en este momento. Por favor, '
                         'vuelva a intentarlo.',
                        })
    
    # If not POST request, create new Photograph form.
    else:
        exam_form = PhotographForm(
            initial={
                'child': child,
                'child_id': child_id,
                'date': datetime.date.today(),
            })

     # Render add_photograph template
    exam_list = Photograph.objects.filter(child_id=child_id)
    context = {
        'child': child,
        'child_id': child_id,
        'residence_id': child.residence_id,
        'photograph_form': exam_form.as_ul,
        'Photographs': exam_list,
        'page': 'photo',
    }
    return render(request, 'tracker/add_photograph.html', context)


"""The view() function renders the photograph template, populated with 
information from the Photograph model. It is protected with the 
login_required decorator, so that no one who isn't logged in can view 
the photograph. The view() function also processes a discard form to delete photos.
"""
@login_required
def view(request, child_id, exam_id):
    exam = get_object_or_404(Photograph, pk=exam_id)
    child = get_object_or_404(Child, pk=child_id)
    # If POST request, confirm delete and then delete photograph from 
    # database
    if (request.POST):
        # After confirmation, delete photo and render the 
        # add_photograph template
        if ('discard' in request.POST):
            exam.delete()
            return HttpResponseRedirect(reverse('tracker:new_photo', 
                kwargs={'child_id': child_id}))  

    # If not POST request, get Photograph object and load the 
    # photograph template
    p = get_object_or_404(Photograph, pk=exam_id)
    child = get_object_or_404(Child, pk=child_id)
    context = {
        'exam': p,
        'child': child,
        'child_id': child.id,
        'residence_id': child.residence_id,
        'page': 'photo',
    }
    return render(request, 'tracker/photograph.html', context)


"""The edit() function creates and processes a Photograph form 
populated with an existing Photograph object information. It then adds 
the edits to the Photograph object and saves it to the database.It is 
protected with the login_required decorator, so that no one who isn't 
logged in can edit a photograph. The edit() function renders the 
edit_photograph template.
"""
@login_required
def edit(request, child_id, exam_id):
    child = get_object_or_404(Child, pk=child_id)
    exam = get_object_or_404(Photograph, pk=exam_id)
    
    # If POST request, get posted photograph form.
    if (request.POST):
        exam_form = PhotographForm(request.POST, request.FILES, instance=exam,
            request=request)
        
        # If user clicked discard button, discard posted form and 
        # render the child_information template.
        if ('discard' in request.POST):
            return HttpResponseRedirect(reverse('tracker:child', 
                kwargs={'child_id': child_id}))

        # If user clicked 'save' or 'submit', process and save forms 
        # (form will validate no matter what in 'save', will be 
        # validated in custom clean() in 'submit'), and edit and save 
        # Photograph object.
        else:
            if (exam_form.is_valid()):
                saved_exam = exam_form.save(commit=False)
                saved_exam.child = child
                saved_exam.save()
                exam_form.save_m2m()

                # Check that photograph object saved
                if (saved_exam):

                    # If user clicked 'save', render edit_photograph
                    # template.
                    if ('save' in request.POST):
                        return HttpResponseRedirect(
                            reverse('tracker:edit_photo', 
                                kwargs={
                                    'child_id': child_id, 
                                    'exam_id': saved_exam.id
                                }))

                    # If user clicked 'submit', render  add_photograph 
                    # template.
                    else:
                        return HttpResponseRedirect(
                            reverse('tracker:new_photo', 
                                kwargs={'child_id': child_id}))  

                # if validation passed but photograph still didn't 
                # save, return to add_photograph template with 
                # "Sorry, please try again" error message
                else:
                    return render(request, 
                        'tracker/edit_photograph.html', 
                        {
                         'error_message': 'Lo sentimos, el formulario no '
                         'se puede guardar en este momento. Por favor, '
                         'vuelva a intentarlo.',
                        })
    
    # If not POST request, create new Photograph form and Signature 
    # form, populated with the Photograph and Signature objects.    
    else:
        exam_form = PhotographForm(instance=exam)

    # Render edit_photograph template
    exam_list = Photograph.objects.filter(child_id=child_id)
    context = {
        'child': child,
        'child_id': child_id,
        'exam_id': exam.id,
        'residence_id': child.residence_id,
        'photograph_form': exam_form.as_ul,
        'Photographs': exam_list,
        'page': 'photo',
    }
    return render(request, 'tracker/edit_photograph.html', context)


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
        exam = get_object_or_404(Photograph, pk=exam_id)
        child = get_object_or_404(Child, pk=child_id)
        
        # On confirmation, delete object and load the add_photograph 
        # template
        if ('discard' in request.POST):
            exam.delete()
            return HttpResponseRedirect(reverse('tracker:new_photo', 
                kwargs={'child_id': child_id}))  
        
        # If no confirmation, return to photograph template
        elif ('no' in request.POST):
            context = {
                'exam': exam,
                'child': child,
                'child_id': child.id,
                'residence_id': child.residence_id,
                'page': 'photo',
            }
            return render(request, 'tracker/photograph.html', context)