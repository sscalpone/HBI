from django.contrib.auth.models import User

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader

from tracker.models import Profile, ProfileForm
from tracker.models import ProfilePermissions, ProfilePermissionsForm
from tracker.models import GlobalPermission

def permissions_check(user):
	if user.is_superuser:
		return True
	elif 'add_users' in user.user_permissions:
		return True
	return False


@login_required
@user_passes_test
def index(request):
    user_list = User.objects.all()
    context = {'user_list': user_list }
    return render(request, 'tracker/main.html', context)


@login_required
@user_passes_test(permissions_check)
def new(request):
    if request.POST:
        profile_form = ProfileForm(request.POST, request.FILES, request=request)
        permissions_form = ProfilePermissionsForm(request.POST, request.FILES, request=request)
        if 'discard' in request.POST:
            return HttpResponseRedirect(reverse('tracker:users'))
        else:
            if profile_form.is_valid() and permissions_form.is_valid:
                saved_permissions = permissions_form.save()
                if saved_permissions:
                    saved_user = profile_form.save(commit=False)
                    saved_user.permission = saved_permissions
                    user = User.objects.create_user(saved_user.username, saved_user.email, saved_user.password)
                    if saved_user.permission.add_users is True:
                        permission = GlobalPermission.objects.create(codename='add_users', name='Add Users')
                        user.user_permissions.add(permission)
                    if saved_user.permission.delete_info is True:
                        permission = GlobalPermission.objects.create(codename='delete_info', name='Delete Info')
                        user.user_permissions.add(permission)
                    if saved_user.permission.add_edit_forms is True:
                        permission = GlobalPermission.objects.create(codename='add_edit_forms', name='Add and Edit Forms')
                        user.user_permissions.add(permission)
                    if saved_user.permission.view is True:
                        permission = GlobalPermission.objects.create(codename='view', name='View')
                        user.user_permissions.add(permission)
                    user.save()
                    saved_permissions.delete()
                    context = {
                        'user_list': User.objects.all(),
                    }
                    return render(request, 'tracker/users.html', context)
    else:
        profile_form = ProfileForm()
        permissions_form = ProfilePermissionsForm()
    context = {
        'profile_form': profile_form.as_ul(),
        'permissions_form': permissions_form.as_ul(),
        'page': 'user',
    }
    return render(request, 'tracker/add_user.html', context)


def view(request):
    pass

def edit(request):
    pass



