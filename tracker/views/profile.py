import datetime

from django.contrib.auth import authenticate

from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader

from tracker.models import Profile, ProfileForm, UserUUID

def permissions_check(user):
    if user.has_perm('tracker.add_users'):
        return True
    else:
        return False


@login_required
def index(request):
    user_list = User.objects.all()
    context = {
        'profile_list': user_list,
        'request': request,
        'page': 'user',
    }
    return render(request, 'tracker/profiles.html', context)


@login_required
@user_passes_test(permissions_check, login_url='tracker/residences/', )
def new(request):
    if request.POST:
        profile_form = ProfileForm(request.POST, request.FILES, request=request)
        if 'discard' in request.POST:
            return HttpResponseRedirect(reverse('tracker:profiles'))
        else:
            if profile_form.is_valid():
                    saved_user = profile_form.save(commit=False)
                    user = User.objects.create_user(saved_user.username, saved_user.email, saved_user.password)
                    user.first_name = saved_user.first_name
                    user.last_name = saved_user.last_name
                    user.is_staff = saved_user.is_staff
                    content_type = ContentType.objects.get_for_model(Profile)
                    if saved_user.add_users is True:
                        permission = Permission.objects.get(codename='add_users', content_type=content_type)
                        user.user_permissions.add(permission)
                    if saved_user.delete_info is True:
                        permission = Permission.objects.get(codename='delete_info', content_type=content_type)
                        user.user_permissions.add(permission)
                    if saved_user.add_edit_forms is True:
                        permission = Permission.objects.get(codename='add_edit_forms', content_type=content_type)
                        user.user_permissions.add(permission)
                    if saved_user.view is True:
                        permission = Permission.objects.get(codename='view', content_type=content_type)
                        user.user_permissions.add(permission)
                    user.save()
                    uuid = UserUUID(user=user)
                    uuid.save()
                    context = {
                        'profile_list': User.objects.all(),
                    }
                    return render(request, 'tracker/profiles.html', context)
    else:
        profile_form = ProfileForm()
    context = {
        'profile_form': profile_form.as_ul(),
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
        
        permissions = p.get_all_permissions()
        if request.method=="POST":
            content_type = ContentType.objects.get_for_model(Profile)
            
            if 'name_form' in request.POST:
                p.first_name = request.POST['first_name']
                p.last_name = request.POST['last_name']
                p.save()
                return HttpResponseRedirect(reverse('tracker:profile', kwargs={'profile_id': profile_id}))
            
            elif 'password_form' in request.POST:
                if authenticate(username=p.username, password=request.POST['old_password']):
                    if request.POST['new_password'] == request.POST['confirm_password']:
                        p.set_password(request.POST['new_password'])
                        p.save()
                        return HttpResponseRedirect(reverse('tracker:profile', kwargs={'profile_id': profile_id}))
                    else:
                        context = {
                            'profile': p,
                            'profile_id': p.id,
                            'page': 'profile',
                            'permissions': permissions,
                            'request': request,
                            'error_message_password': 'New passwords do not match.'
                        }
                        return render(request, 'tracker/profile.html', context)
                else:
                    context = {
                        'profile': p,
                        'profile_id': p.id,
                        'page': 'profile',
                        'permissions': permissions,
                        'request': request,
                        'error_message_password': 'Password is incorrect.'
                    }
                    return render(request, 'tracker/profile.html', context)
            
            elif 'add_users_form' in request.POST:
                permission = Permission.objects.get(codename='add_users', content_type=content_type)
                if request.POST['add_users'] == 'True':
                    p.user_permissions.add(permission)
                    p.save()
                    return HttpResponseRedirect(reverse('tracker:profile', kwargs={'profile_id': profile_id}))
                elif request.POST['add_users'] =='False':  
                    p.user_permissions.remove(permission)
                    p.save()
                    return HttpResponseRedirect(reverse('tracker:profile', kwargs={'profile_id': profile_id}))

            elif 'delete_info_form' in request.POST:
                permission = Permission.objects.get(codename='delete_info', content_type=content_type)
                if request.POST['delete_info'] == 'True':
                    p.user_permissions.add(permission)
                    p.save()
                    return HttpResponseRedirect(reverse('tracker:profile', kwargs={'profile_id': profile_id}))
                elif request.POST['delete_info'] == 'False':  
                    p.user_permissions.remove(permission)
                    p.save()
                    return HttpResponseRedirect(reverse('tracker:profile', kwargs={'profile_id': profile_id}))

            elif 'add_edit_forms_form' in request.POST:
                permission = Permission.objects.get(codename='add_edit_forms', content_type=content_type)
                if request.POST['add_edit_forms'] == 'True':
                    p.user_permissions.add(permission)
                    p.save()
                    return HttpResponseRedirect(reverse('tracker:profile', kwargs={'profile_id': profile_id}))
                elif request.POST['add_edit_forms'] == 'False':  
                    p.user_permissions.remove(permission)
                    p.save()
                    return HttpResponseRedirect(reverse('tracker:profile', kwargs={'profile_id': profile_id}))

            elif 'is_staff_form' in request.POST:
                if request.POST['is_staff'] == 'True':
                    p.is_staff = True
                    p.save()
                    return HttpResponseRedirect(reverse('tracker:profile', kwargs={'profile_id': profile_id}))
                elif request.POST['if_staff'] == 'False':  
                    p.is_staff = False
                    p.save()
                    return HttpResponseRedirect(reverse('tracker:profile', kwargs={'profile_id': profile_id}))

            elif 'is_active_form' in request.POST:
                if request.POST['is_active'] == 'True':
                    p.is_active = True
                    p.save()
                    return HttpResponseRedirect(reverse('tracker:profile', kwargs={'profile_id': profile_id}))
                elif request.POST['is_active'] == 'False':  
                    p.is_active = False
                    p.save()
                    return HttpResponseRedirect(reverse('tracker:profile', kwargs={'profile_id': profile_id}))

        context = {
            'profile': p,
            'profile_id': p.id,
            'page': 'profile',
            'permissions': permissions,
            'request': request,
            'page': 'user',
        }
        return render(request, 'tracker/profile.html', context)




