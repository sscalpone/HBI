 #coding=utf-8

"""

residence.py contains the functions for the Residence objects:
index(), new(), view(), and edit(). index() pulls a list of all
Residence objects, new() populates a new Residence object for the
Residence_Form modelform, view() pulls individual Residence objects
for review, and edit() changes a Residence object using the
Residence_Form modelform.

"""

import datetime

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader

from tracker.models import Residence, ResidenceForm
from tracker.models import Child


"""The index() function renders the main template with the list of
residences in the app. Requires logging in to view.
"""
@login_required()
def index(request):
    list_of_residences = Residence.objects.all()
    context = {'residences': list_of_residences}
    return render(request, 'tracker/main.html', context)


"""The new() function creates and processes a new Residence form. It
then creates a new Residence object from the Residence model,
populates it with the form info, and saves it to the database. It is
protected with the login_required decorator, so that no one who isn't
logged in can add a form. The new() function renders the add_residence
template.
"""
@login_required()
def new(request):
    # If POST request, get posted Residence form.
    if (request.POST):
        form = ResidenceForm(request.POST, request.FILES, request=request)

        # If user clicked discard button, discard posted form and
        # render the main template.
        if ('discard' in request.POST):
            return HttpResponseRedirect(reverse('tracker:residences'))

        # If user clicked 'save' or 'submit', process and save form
        # (form will validate no matter what in 'save', will be
        # validated in custom clean() in 'submit'), create and save
        # new Residence object.
        else:
            if (form.is_valid()):
                saved_residence = form.save(commit=False)
                saved_residence.last_saved = datetime.datetime.utcnow()
                saved_residence.save()
                form.save_m2m()

                if (saved_residence):

                    # If user clicked 'save', render edit_residence 
                    # template
                    if 'save' in request.POST:
                        return HttpResponseRedirect(
                            reverse('tracker:edit_residence',
                                kwargs={'residence_id': saved_residence.id}))

                    # If user clicked 'submit', render main template
                    else:
                        return HttpResponseRedirect(
                            reverse('tracker:residence',
                                kwargs={'residence_id': saved_residence.id}))

                # if validation passed but residence still didn't
                # save, return to add_residence template with "Sorry,
                # please try again" error message
                else:
                    return render(request, 'tracker/add_residence.html',
                        {
                         'error_message': 'Lo sentimos, el formulario no se '
                         'puede guardar en este momento. Por favor, vuelva a '
                         'intentarlo.',
                        })

    # If not POST request, create new Residence form.
    else:
        form = ResidenceForm()

    # Render add_residence template
    context = {
        'form': form.as_ul,
        'page': 'residence',
    }
    return render(request, 'tracker/add_residence.html', context)


"""The view() function renders the residence template, populated with
information from the Residence model and a list of Child objects in
that residence. It is protected with the login_required decorator, so
that no one who isn't logged in can add a form.
"""
@login_required()
def view(request, residence_id):
    residence = get_object_or_404(Residence, pk=residence_id)
    # All the children in chosen residence
    children = Child.objects.filter(residence_id=residence_id)
    # All the children in that residence that are active
    active = Child.objects.filter(residence_id=residence_id).filter(
        is_active=True)
    # All the inactive children in that residence
    inactive = Child.objects.filter(residence_id=residence_id).filter(
        is_active=False)
    # Number of active boys in the residence
    boys = len(Child.objects.filter(residence_id=residence_id).filter(
        is_active=True).filter(gender='m'))
    # Number of inactive girls in the residence
    girls = len(Child.objects.filter(residence_id=residence_id).filter(
        is_active=True).filter(gender='f'))
    # Number of at-risk children in the residence
    at_risk = len(Child.objects.filter(residence_id=residence_id).filter(
        priority='1'))

    if (request.POST):
        # After confirmation, delete photo and render the
        # add_photograph template
        if ('discard' in request.POST):
            residence.delete()
            return HttpResponseRedirect(reverse('tracker:new_residence'))

    context = {
        'residence': residence,
        'children': children,
        'active': active,
        'inactive': inactive,
        'residence_id': residence.id,
        'boys': boys,
        'girls': girls,
        'at_risk': at_risk,
        'page': 'residence',
    }
    return render(request, 'tracker/residence.html', context)


"""The edit() function creates and processes a Residence form
populated with an existing Residence object information. It then adds
the edits to the Residence object and saves it to the database. It is
protected with the login_required decorator, so that no one who isn't
logged in can add a form. The edit() function renders the
edit_residence template.
"""
@login_required()
def edit(request, residence_id):
    residence = get_object_or_404(Residence, pk=(residence_id))

    # If POST request, get posted Residence form.
    if (request.POST):
        form = ResidenceForm(request.POST, request.FILES, instance=residence,
            request=request)

        # If user clicked discard button, discard posted form and
        # render the residence template.
        if ('discard' in request.POST):
            return HttpResponseRedirect(reverse('tracker:residences'))

        # If user clicked 'save' or 'submit', process and save form
        # (form will validate no matter what in 'save', will be
        # validated in custom clean() in 'submit'), and edit and save
        # Residence object.
        else:
            if (form.is_valid()):
                saved_residence = form.save()

                # Make sure residence object saved
                if (saved_residence):

                    # If user clicked 'save', render edit_residence
                    # template.
                    if ('save' in request.POST):
                        return HttpResponseRedirect(
                            reverse('tracker:edit_residence',
                                kwargs={'residence_id': saved_residence.id}))

                    # If user clicked 'submit', render residence
                    # template.
                    else:
                        return HttpResponseRedirect(
                            reverse('tracker:residence',
                                kwargs={'residence_id': saved_residence.id}))

                # if validation passed but residence still didn't
                # save, return to edit_residence template with "Sorry,
                # please try again" error message
                else:
                    return render(request, 'tracker/edit_residence.html',
                        {
                        'error_message': 'Lo sentimos, el formulario no se '
                        'puede guardar en este momento. Por favor, vuelva a '
                        'intentarlo.',
                        })

    # If not POST request, create new Residence form, populated with
    # Residence object info.
    else:
        form = ResidenceForm(instance=residence)
    context = {
        'form': form.as_ul,
        'residence_id': residence.id,
        'page': 'residence',
    }
    return render(request, 'tracker/edit_residence.html', context)

"""The delete() function confirms with the user that a photograph
should be deleted, and then deletes the objects from the database.
This function is unused as long as javascript is enabled, as the
deletion process is done in the view() function, and the form is
rendered in a jQueryUI dialog box. This function is kept merely as a
precaution/so that it can be rebuilt for other objects without needing
to parse the view() object too carefully.
"""
def delete(request, residence_id):
    # If POST request, get Photograph object, confirm deletion with
    # user, and delete object
    if (request.POST):
        residence = get_object_or_404(Residence, pk=residence_id)

        # On confirmation, delete object and load the add_photograph
        # template
        if ('discard' in request.POST):
            residence.delete()
            return HttpResponseRedirect(
                reverse('tracker:new_residence'))

        # If no confirmation, return to photograph template
        elif ('no' in request.POST):
            context = {
                'residence': residence,
                'residence_id': residence.id,
                'page': 'residence',
            }
            return render(request, 'tracker/residence.html', context)
