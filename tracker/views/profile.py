from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader

from tracker.models import Profile, ProfileForm
from tracker.models import ProfilePermissions, ProfilePermissionsForm

def permissions_check(user):
    if user.has_perm('tracker.add_users'):
        return True
    else:
        return False


# def permission_or_own_page(request, user_id):
#     profile = request.user
#     if permissions_check(profile):
#         return True
#     elif profile.id == user_id:
#         return True
#     else:
#         return False

@login_required
# @user_passes_test(permissions_check)
def index(request):
    user_list = User.objects.all()
    context = {
        'profile_list': user_list,
        'request': request,
    }
    return render(request, 'tracker/profiles.html', context)


@login_required
@user_passes_test(permissions_check, login_url='tracker/residences/', )
def new(request):
    if request.POST:
        profile_form = ProfileForm(request.POST, request.FILES, request=request)
        permissions_form = ProfilePermissionsForm(request.POST, request.FILES, request=request)
        if 'discard' in request.POST:
            return HttpResponseRedirect(reverse('tracker:profiles'))
        else:
            if profile_form.is_valid() and permissions_form.is_valid:
                    saved_user = profile_form.save(commit=False)
                    saved_permission = permissions_form.save(commit=False)
                    user = User.objects.create_user(saved_user.username, saved_user.email, saved_user.password)
                    user.first_name = saved_user.first_name
                    user.last_name = saved_user.last_name
                    content_type = ContentType.objects.get_for_model(Profile)
                    if saved_permission.add_users is True:
                        permission = Permission.objects.get(codename='add_users', content_type=content_type)
                        user.user_permissions.add(permission)
                    if saved_permission.delete_info is True:
                        permission = Permission.objects.get(codename='delete_info', content_type=content_type)
                        user.user_permissions.add(permission)
                    if saved_permission.add_edit_forms is True:
                        permission = Permission.objects.get(codename='add_edit_forms', content_type=content_type)
                        user.user_permissions.add(permission)
                    if saved_permission.view is True:
                        permission = Permission.objects.get(codename='view', content_type=content_type)
                        user.user_permissions.add(permission)
                    user.save()
                    context = {
                        'profile_list': User.objects.all(),
                    }
                    return render(request, 'tracker/profiles.html', context)
    else:
        profile_form = ProfileForm()
        permissions_form = ProfilePermissionsForm()
    context = {
        'profile_form': profile_form.as_ul(),
        'permissions_form': permissions_form.as_ul(),
        'page': 'user',
    }
    return render(request, 'tracker/add_profile.html', context)

@login_required
def view(request, profile_id):
    user = request.user
    
    if permissions_check(user):
        allowed=True
    
    elif user.id == int(profile_id):
        allowed=True
    
    else:
        allowed=False
    
    if allowed==False:
        return HttpResponseRedirect(reverse('tracker:residences'))
    
    else:
        p = get_object_or_404(User, pk=profile_id)
        if p.is_superuser and not user.is_superuser:
            context = {
            'error_message': 'Usted no tiene permiso para ver este usuario.',
            'profile_list': User.objects.all(),
            }
            return render(request, 'tracker/profiles.html', context)
        else:
            permissions = p.get_all_permissions()
            print permissions
            context = {
                'profile': p,
                'profile_id': p.id,
                'page': 'profile',
                'permissions': permissions,
                'request': request,
            }
            return render(request, 'tracker/profile.html', context)

def edit(request):
    pass



