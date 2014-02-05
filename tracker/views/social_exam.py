from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader

from tracker.models import SocialExamInfo
from tracker.models import SocialExamInfoForm

def index(request, child_id):
    list = SocialExamInfo.objects.filter(child_id=child_id)
    context = RequestContext(request, {
        'SocialExams': list,
        'child_id': child_id
    })
    return render(request, 'tracker/child_social_histories.html', context)

def new(request, child_id):
    if request.method == 'POST':
        form = SocialExamInfoForm(request.POST, request.FILES)
        if form.is_valid():
            saved = form.save()
            if saved:
                return HttpResponseRedirect(reverse('tracker:social_exams'))
    else:
        form = SocialExamInfoForm(initial={'child': child_id})
    context = {
        'child_id': child_id,
        'form': form,
    }
    return render(request, 'tracker/add_child_social_history.html', context)

def view(request, exam_id):
    p = get_object_or_404(SocialExamInfo, pk=exam_id)
    context = {
        'exam': p,
    }
    return render(request, 'tracker/child_social_history.html', context)
