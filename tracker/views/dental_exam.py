import datetime
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader

from tracker.models import DentalExam
from tracker.models import DentalExamForm

def new(request, child_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed('Only POST here')
    form = DentalExamForm(request.POST, request.FILES)
    if form.is_valid():
        saved_form = form.save()
        form = DentalExamForm(initial={'child': child_id})
    p = DentalExam.objects.filter(child = child_id)
    context = {
        'form': form,
        'child_id': child_id,
        'dental_exam': p,
    }
    return render(request, 'tracker/dental_exam.html', context)

def view(request, child_id):
    p = DentalExam.objects.filter(child = child_id)
    form = DentalExamForm(initial={'child': child_id})
    context = {
        'form': form,
        'child_id': child_id,
        'dental_exam': p,
    }
    return render(request, 'tracker/dental_exam.html', context)
