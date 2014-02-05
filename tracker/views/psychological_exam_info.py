import datetime
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader

from tracker.models import Child
from tracker.models import PsychologicalExamInfo
from tracker.models import PsychologicalExamInfoForm

def new(request, child_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed('Only POST here')
    form = PsychologicalExamInfoForm(request.POST, request.FILES)
    if form.is_valid():
        saved_form = form.save()
        form = PsychologicalExamInfoForm(initial={'child': child_id})
    p = PsychologicalExamInfo.objects.filter(child = child_id)
    c = get_object_or_404(Child, pk=child_id)
    context = {
        'form': form,
        'child': c,
        'psychological_exams': p,
    }
    return render(request, 'tracker/psychological_exam_info.html', context)

def view(request, child_id):
    c = get_object_or_404(Child, pk=child_id)
    p = PsychologicalExamInfo.objects.filter(child = child_id)
    form = PsychologicalExamInfoForm(initial={'child': child_id})
    context = {
        'form': form,
        'child': c,
        'psychological_exams': p,
    }
    return render(request, 'tracker/psychological_exam_info.html', context)

