#coding=utf-8

import datetime

from tracker.models import CustomUser as User
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from tracker.models import ProfileForm
from tracker.models import EditNameForm, EditPasswordForm
from tracker.models import EditIsStaffForm, EditIsActiveForm
from tracker.models import EditAddUsersForm, EditDeleteInfoForm
from tracker.models import EditAddEditFormsForm
from tracker.models import EditRestrictToHomeForm, EditEmailForm


def is_superuser_check(user):
    return user.is_superuser


"""add_users_check() checks if a user can add_users and returns a
boolean.
"""

def add_users_check(user):
    if (user.has_perm('tracker.add_users')):
        return True
    else:
        return False


"""add_edit_forms_check() checks if a user can add and edit forms for
children in homes, and returns a boolean.
"""

def add_edit_forms_check(user):
    if (user.has_perm('tracker.add_edit_forms')):
        return True
    else:
        return False


"""restrict_to_home_check() checks if a user is restricted to a home,
and returns the home if True, and returns a None if false.
"""

def restrict_to_home_check(user):
    if (not user.has_perm('tracker.not_restricted_to_home')):
        return user.residence
    else:
        return None


def current_user_profile_check(user_id, profile_id):
    if (user_id == int(profile_id)):
        return True
    else:
        return False


"""index() gets a list of users and renders the profiles.html template
with that list. If the user can add users (checks with add_user_check)
and is the superuser, the entire list of users is displayed. If the
user can add users but isn't the superuser, all users except the
superuser are displayed. Otherwise, only the current user's profile is
displayed. Protected by thr login_required decorator so users have to
be logged in to access information.
"""

@login_required
def index(request):
    # Check if user can add users
    if (add_users_check(request.user)):
        # If user can add users, check if user is superuser
        if (request.user.is_superuser):
            user_list = User.objects.all()

        # If not superuser, exclude superuser from list
        else:
            user_list = User.objects.filter(is_superuser=0)

    # If user can't add users, only display current user's profile
    else:
        user_list = User.objects.filter(pk=request.user.id)

    # Render the profile.html template
    context = {
        'profile_list': user_list,
        'request': request,
        'page': 'user',
    }
    return render(request, 'tracker/profiles.html', context)


"""new() creates a new User using the Profile model (which will be
removed in later versions as extraneous) and the ProfileForm modelform.
User objects are populated from the ProfileForm, with extra
information (which home they belong to and their UUID) in the UserUUID
model. Protected by the login_required and
user_passes_test(add_users_check) decorators so that only logged-in
users who can also add new users can visit this page.
"""

@login_required
@user_passes_test(add_users_check, login_url='tracker/residences/')
def new(request):
    # If POST request, get posted ProfileForm
    if (request.POST):
        profile_form = ProfileForm(request.POST, request.FILES,
                                   request=request)

        # If user clicked discard button, discard posted form and
        # render the profiles template.
        if ('discard' in request.POST):
            return HttpResponseRedirect(reverse('tracker:profiles'))

        # If user clicked 'save' or 'submit', process and save form
        # (form will validate no matter what in 'save', will be
        # validated in custom clean() in 'submit'). Create a User
        # object and populate it with the ProfileForm information.
        # The Profile object will not be saved.
        else:
            if (profile_form.is_valid()):
                    saved_user = profile_form.cleaned_data
                    # Check that profile_form saved
                    if (saved_user):
                        # Create and populate new User object
                        user = User.objects.create_user(
                            saved_user['username'],
                            saved_user['email'],
                            saved_user['password']
                        )
                        user.is_superuser = saved_user['is_superuser']
                        user.first_name = saved_user['first_name']
                        user.last_name = saved_user['last_name']
                        user.is_staff = saved_user['is_staff']
                        user.residence = saved_user['residence']
                        user.last_saved = datetime.datetime.utcnow()
                        content_type = ContentType.objects.get_for_model(
                            User)

                        # Add permissions
                        if (saved_user['add_users'] is True):
                            user.add_users = True
                            permission = Permission.objects.get(
                                codename='add_users',
                                content_type=content_type
                            )
                            user.user_permissions.add(permission)

                        if (saved_user['delete_info'] is True):
                            user.delete_info = True
                            permission = Permission.objects.get(
                                codename='delete_info',
                                content_type=content_type
                            )
                            user.user_permissions.add(permission)

                        if (saved_user['add_edit_forms'] is True):
                            user.add_edit_forms = True
                            permission = Permission.objects.get(
                                codename='add_edit_forms',
                                content_type=content_type
                            )
                            user.user_permissions.add(permission)

                        if (saved_user['view'] is True):
                            user.add_edit_forms = True
                            permission = Permission.objects.get(
                                codename='view',
                                content_type=content_type
                            )
                            user.user_permissions.add(permission)

                        if (saved_user['restrict_to_home'] is False):
                            user.not_restricted_to_home = True
                            permission = Permission.objects.get(
                                codename='not_restricted_to_home',
                                content_type=content_type
                            )
                            user.user_permissions.add(permission)

                        user.save()

                        # Check that user object saved
                        if (user):
                            context = {
                                'profile_list': User.objects.all(),
                            }
                            return render(request,
                                          'tracker/profiles.html',
                                          context)

                        # if validation passed but the user object
                        # still didn't save, return to
                        # add_profile template with "Sorry,
                        # please try again" error message
                        else:
                            return render(request,
                                          'tracker/add_profile.html',
                                          {'error_message': 'Lo sentimos, el '
                                           'formulario se puede guardar en '
                                           'este momento. Por favor, vuelva a'
                                           ' intentarlo.', })

                    # if validation passed but the profile still
                    # didn't save, return to add_disease_history
                    # template with "Sorry, please try again" error
                    # message
                    else:
                        return render(request,
                                      'tracker/add_profile.html',
                                      {'error_message': 'Lo sentimos, el '
                                       'formulario no se puede guardar en '
                                       'este momento. Por favor, vuelva a '
                                       'intentarlo.', })

    # If not POST request, load add_profile.html template
    else:
        profile_form = ProfileForm()
    context = {
        'profile_form': profile_form.as_ul(),
        'page': 'user',
    }
    return render(request, 'tracker/add_profile.html', context)


"""

"""
@login_required
def view(request, profile_id):
    user = request.user

    # Check if the user can add users or if profile is of the current
    # user. If neither are true, return to profiles. This is just a
    # precaution, as the profiles page shouldn't display any profiles
    # the current user isn't allowed to see.
    if (not current_user_profile_check(user.id, profile_id)):
        if (not add_users_check(user)):
            return HttpResponseRedirect(reverse('tracker:profiles'))

    p = get_object_or_404(User, pk=profile_id)

    # If the profile is of the superuser and the current user is
    # not a the superuser, turn to the profiles template again.
    # Also a precaution, as the superuser profile should only
    # display on profiles if the current user is the superuser.
    if (p.is_superuser and not user.is_superuser):
        context = {
            'error_message': 'Usted no tiene permiso para ver este usuario.',
            'profile_list': User.objects.all(),
        }
        return render(request, 'tracker/profiles.html', context)

    else:
        permissions = p.get_all_permissions()

        # If POST request, edit the User
        if (request.POST):
            content_type = ContentType.objects.get_for_model(User)

            # Each form has different name so that posted forms
            # can be differentiated and processed correctly

            # If the user is editing the name, process the form
            # and edit the user's name
            if ('name_form' in request.POST):
                form = EditNameForm(request.POST, request.FILES,
                                    request=request)
                if (form.is_valid()):
                    saved_form = form.cleaned_data
                    if (not request.user.check_password(
                            saved_form['password'])):
                        messages.add_message(request, messages.INFO,
                                             'Su contraseña es incorrecta.',
                                             extra_tags='name')
                        return HttpResponseRedirect(
                            reverse('tracker:profile',
                                    kwargs={'profile_id': profile_id}))
                    profile = get_object_or_404(User, pk=profile_id)
                    profile.first_name = saved_form['first_name']
                    profile.last_name = saved_form['last_name']
                    profile.last_saved = datetime.datetime.utcnow()
                    profile.save()

                # Render the profile.html template
                return HttpResponseRedirect(
                    reverse('tracker:profile',
                            kwargs={'profile_id': profile_id}))

            # If the user is editing the email, process the form
            # and edit the user's email
            elif ('email_form' in request.POST):
                form = EditEmailForm(request.POST, request.FILES,
                                     request=request)
                if (form.is_valid()):
                    saved_form = form.cleaned_data
                    if (not request.user.check_password(
                            saved_form['password'])):
                        messages.add_message(request,
                                             messages.INFO,
                                             'Su contraseña es incorrecta.',
                                             extra_tags='name')
                        return HttpResponseRedirect(
                            reverse('tracker:profile',
                                    kwargs={'profile_id': profile_id}))
                    profile = get_object_or_404(User, pk=profile_id)
                    profile.email = saved_form['email']
                    profile.last_saved = datetime.datetime.utcnow()
                    profile.save()

                # Render the profile.html template
                return HttpResponseRedirect(
                    reverse('tracker:profile',
                            kwargs={'profile_id': profile_id}))

            # If the user is editing the password, process the
            # form and edit the user's password
            elif ('password_form' in request.POST):
                form = EditPasswordForm(request.POST, request.FILES,
                                        request=request)
                if (form.is_valid()):
                    saved_form = form.cleaned_data
                    profile = get_object_or_404(User, pk=profile_id)
                    profile.password = make_password(saved_form['password'])
                    profile.last_saved = datetime.datetime.utcnow()
                    profile.save()

                # Render the profile template
                return HttpResponseRedirect(
                    reverse('tracker:profile',
                            kwargs={'profile_id': profile_id}))

            # If the user is editing the add_user permission,
            # process the form and edit the user's permission
            elif 'add_users_form' in request.POST:
                form = EditAddUsersForm(request.POST, request.FILES,
                                        request=request)
                if (form.is_valid()):
                    saved_form = form.cleaned_data
                    profile = get_object_or_404(User, pk=profile_id)
                    permission = Permission.objects.get(
                        codename='add_users',
                        content_type=content_type
                    )
                    if (saved_form['add_users'] is True):
                        profile.add_users = True
                        profile.user_permissions.add(permission)
                    else:
                        profile.add_users = False
                        profile.user_permissions.remove(permission)
                    profile.last_saved = datetime.datetime.utcnow()
                    profile.save()

                # Render the profile template
                return HttpResponseRedirect(
                    reverse('tracker:profile',
                            kwargs={'profile_id': profile_id}))

            # If the user is editing the delete_info permission,
            # process the form and edit the user's permission
            elif 'delete_info_form' in request.POST:
                form = EditDeleteInfoForm(request.POST, request.FILES,
                                          request=request)
                if (form.is_valid()):
                    saved_form = form.cleaned_data
                    profile = get_object_or_404(User, pk=profile_id)
                    permission = Permission.objects.get(
                        codename='delete_info',
                        content_type=content_type
                    )
                    if (saved_form['delete_info'] is True):
                        profile.delete_info = True
                        profile.user_permissions.add(permission)
                    else:
                        profile.delete_info = False
                        profile.user_permissions.remove(permission)
                    profile.last_saved = datetime.datetime.utcnow()
                    profile.save()
                return HttpResponseRedirect(reverse('tracker:profile', 
                    kwargs={'profile_id': profile_id}))

            # If the user is editing the add_edit_forms 
            # permission, process the form and edit the user's 
            # permission
            elif 'add_edit_forms_form' in request.POST:
                form = EditAddEditFormsForm(request.POST, request.FILES, 
                    request=request)
                if (form.is_valid()):
                    saved_form = form.cleaned_data
                    profile = get_object_or_404(User, pk=profile_id)
                    permission = Permission.objects.get(
                        codename='add_edit_forms', 
                        content_type=content_type
                    )
                    if (saved_form['add_edit_forms'] is True):
                        profile.add_edit_forms = True
                        profile.user_permissions.add(permission)
                    else:
                        profile.add_edit_forms = False
                        profile.user_permissions.remove(permission)
                    profile.last_saved = datetime.datetime.utcnow()
                    profile.save()
                return HttpResponseRedirect(reverse('tracker:profile', 
                    kwargs={'profile_id': profile_id}))

            # If the user is editing the add_edit_forms 
            # permission, process the form and edit the user's 
            # permission
            elif 'restrict_to_home_form' in request.POST:
                form = EditRestrictToHomeForm(request.POST, request.FILES, 
                    request=request)
                if (form.is_valid()):
                    saved_form = form.cleaned_data
                    profile = get_object_or_404(User, pk=profile_id)
                    permission = Permission.objects.get(
                        codename='not_restricted_to_home', 
                        content_type=content_type
                    )
                    if (saved_form['restrict_to_home'] is False):
                        profile.not_restricted_to_home = True
                        profile.residence = None
                        profile.user_permissions.add(permission)
                    else:
                        profile.add_edit_forms = True
                        profile.residence = saved_form['residence']
                        profile.user_permissions.remove(permission)
                    profile.last_saved = datetime.datetime.utcnow()
                    profile.save()
                return HttpResponseRedirect(reverse('tracker:profile', 
                    kwargs={'profile_id': profile_id}))


            # If the user is editing the staff status, 
            # process the form and edit the user's staff status
            elif 'is_staff_form' in request.POST:
                form = EditIsStaffForm(request.POST, request.FILES, 
                    request=request)
                if (form.is_valid()):
                    saved_form = form.cleaned_data
                    profile = get_object_or_404(User, pk=profile_id)
                    if (saved_form['is_staff'] is True):
                        profile.is_staff = True
                    else:
                        profile.is_staff = False
                    profile.last_saved = datetime.datetime.utcnow()
                    profile.save()
                return HttpResponseRedirect(reverse('tracker:profile', 
                    kwargs={'profile_id': profile_id}))

            # If the user is editing the user's active status, 
            # process the form and edit the user's active status
            elif 'is_active_form' in request.POST:
                form = EditIsActiveForm(request.POST, request.FILES, 
                    request=request)
                if (form.is_valid()):
                    saved_form = form.cleaned_data
                    profile = get_object_or_404(User, pk=profile_id)
                    if (saved_form['is_active'] is True):
                        profile.is_active = True
                    else:
                        profile.is_active = False
                    profile.last_saved = datetime.datetime.utcnow()
                    profile.save()
                return HttpResponseRedirect(reverse('tracker:profile', 
                    kwargs={'profile_id': profile_id}))
            

        profile = get_object_or_404(User, pk=profile_id)
        name_form = EditNameForm(initial={
                'first_name': profile.first_name,
                'last_name': profile.last_name,
            })
        
        email_form = EditEmailForm(initial={
                'email': profile.email,
            })
        
        password_form = EditPasswordForm()
        
        is_active_form = EditIsActiveForm(initial={
                'is_active': profile.is_active,
            })
        
        is_staff_form = EditIsStaffForm(initial={
                'is_staff': profile.is_staff,
            })
        
        add_users_form = EditAddUsersForm(initial={
                'add_users': profile.has_perm('tracker.add_users'),
            })
        
        delete_info_form = EditDeleteInfoForm(initial={
                'delete_info': profile.has_perm('tracker.delete_info'),
            })
        
        add_edit_forms_form = EditAddEditFormsForm(
            initial={
                'add_edit_forms': profile.has_perm(
                    'tracker.add_edit_forms'
                ),
            })
        
        restrict_to_home_form = EditRestrictToHomeForm(
            initial={
               'restrict_to_home': not profile.has_perm(
                    'tracker.not_restricted_to_home'
                ),
               'residence': profile.residence,
            })

        # Render the profile template
        context = {
            'profile': p,
            'profile_id': p.id,
            'page': 'profile',
            'permissions': permissions,
            'request': request,
            'page': 'user',
            'name_form': name_form.as_ul,
            'password_form': password_form.as_ul,
            'is_active_form': is_active_form.as_ul,
            'is_staff_form': is_staff_form.as_ul,
            'add_users_form': add_users_form.as_ul,
            'delete_info_form': delete_info_form.as_ul,
            'add_edit_forms_form': add_edit_forms_form.as_ul,
            'restrict_to_home_form': restrict_to_home_form.as_ul,
            'email_form': email_form.as_ul,
        }
        return render(request, 'tracker/profile.html', context)
