# coding=utf-8

import datetime

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from tracker.models import Child, ChildForm


"""The new() function creates and processes a new Child form. It then
creates a new Child object from the Child model, populates it with the
form info, and saves it to the database. It is protected with the
login_required decorator, so that no one who isn't logged in can add a
form. The new() function renders the add_child template.
"""

@login_required()
def new(request, residence_id):
    # If POST request, get posted Child form.
    if (request.POST):
        form = ChildForm(request.POST, request.FILES, request=request)

        # If user clicked discard button, discard posted form and
        # render the residence template.
        if ('discard' in request.POST):
            return HttpResponseRedirect(
                reverse('tracker:residence',
                        kwargs={'residence_id': residence_id}))

        # If user clicked 'save' or 'submit', process and save form
        # (form will validate no matter what in 'save', will be
        # validated in custom clean() in 'submit'), create and save
        # new Child object.
        else:
            if (form.is_valid()):
                saved_child = form.save(commit=False)
                saved_child.last_saved = datetime.datetime.utcnow()
                saved_child.save()
                form.save_m2m()

                # make sure child saved
                if (saved_child):

                    # If user clicked 'save', render edit_child
                    # template.
                    if ('save' in request.POST):
                        return HttpResponseRedirect(
                            reverse('tracker:edit_child',
                                    kwargs={'child_id': saved_child.id}))

                    # If user clicked 'submit', render child template.
                    else:
                        return HttpResponseRedirect(
                            reverse('tracker:child',
                                    kwargs={'child_id': saved_child.id}))

               # if validation passed but child still didn't save,
               # return to add_child template with "Sorry, please try
               # again" error message
                else:
                    return render(request, 'tracker/add_child.html',
                                  {'error_message': 'Lo sentimos, el '
                                   'formulario no se puede guardar en este '
                                   'momento. Por favor, vuelva a intentarlo.',
                                   })

    # If not POST request, create new Child form.
    else:
        form = ChildForm()

    # Render add_child template
    context = {
        'form': form.as_ul,
        'residence_id': residence_id,
        'page': 'child',
    }
    return render(request, 'tracker/add_child.html', context)


"""The view() function renders the child_information template,
populated with information from the Child model. It is protected with
the login_required decorator, so that no one who isn't logged in can
add a form.
"""

@login_required
def view(request, child_id):
    child = get_object_or_404(Child, pk=child_id)
    residence_id = child.residence_id
    print "hello?"
    if (request.POST):
        print "post"
        # After confirmation, delete photo and render the
        # add_photograph template
        if ('discard' in request.POST):
            print "discard"
            child.delete()
            return HttpResponseRedirect(reverse('tracker:new_child',
                                        kwargs={'residence_id': residence_id})
                                        )

    context = {
        'child': child,
        'child_id': child.id,
        'residence_id': child.residence_id,
        'page': 'child',
    }
    return render(request, 'tracker/child_information.html', context)


"""The edit() function creates and processes a Child form populated
with an existing Child object. It then adds the edits to the Child
object and saves it to the database. It is protected with the
login_required decorator, so that no one who isn't logged in can add a
form. The new() function renders the edit_child template.
"""

@login_required
def edit(request, child_id):
    child = get_object_or_404(Child, pk=child_id)
    residence_id = child.residence_id

    # If POST request, get posted Child form.
    if (request.POST):
        form = ChildForm(request.POST, request.FILES, instance=child,
                         request=request)

        # If user clicked discard button, discard posted form and
        # render the residence template.
        if ('discard' in request.POST):
            return HttpResponseRedirect(
                reverse('tracker:residence',
                        kwargs={'residence_id': residence_id}))

        # If user clicked 'save' or 'submit', process and save form
        # (form will validate no matter what in 'save', will be
        # validated in custom clean() in 'submit'), and edit and save
        # Child object.
        else:
            if (form.is_valid()):
                saved_child = form.save(commit=False)
                saved_child.last_saved = datetime.datetime.utcnow()
                saved_child.save()
                form.save_m2m()

                # Check that the child object saved
                if (saved_child):

                    # If user clicked 'save', render edit_child
                    # template.
                    if ('save' in request.POST):
                        return HttpResponseRedirect(reverse(
                            'tracker:edit_child',
                            kwargs={'child_id': saved_child.id}
                        ))

                    # If user clicked 'submit', render child template.
                    else:
                        return HttpResponseRedirect(
                            reverse('tracker:child',
                                    kwargs={'child_id': saved_child.id}))

                # if validation passed but child still didn't save,
                # return to add_child template with "Sorry, please try
                # again" error message
                else:
                    return render(request, 'tracker/edit_child.html',
                                  {'error_message': 'Lo sentimos, el '
                                   'formulario no se puede guardar en este '
                                   'momento. Por favor, vuelva a intentarlo.',
                                   })

    # If not POST request, create new Child form, populated with Child
    # object.
    else:
        form = ChildForm(instance=child)

    # Render edit_child template
    context = {
        'form': form.as_ul,
        'residence_id': residence_id,
        'child_id': child_id,
        'page': 'child',
    }
    return render(request, 'tracker/edit_child.html', context)


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
        child = get_object_or_404(Child, pk=child_id)
        residence_id = child.residence_id

        # On confirmation, delete object and load the add_photograph
        # template
        if ('discard' in request.POST):
            child.delete()
            return HttpResponseRedirect(reverse('tracker:new_child',
                                        kwargs={'residence_id': residence_id})
                                        )

        # If no confirmation, return to photograph template
        elif ('no' in request.POST):
            context = {
                'child': child,
                'child_id': child.id,
                'residence_id': child.residence_id,
                'page': 'residence',
            }
            return render(request, 'tracker/child.html', context)
