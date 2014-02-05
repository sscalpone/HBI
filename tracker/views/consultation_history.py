import datetime
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader

from tracker.models import ConsultationHistory
from tracker.models import ConsultationHistoryForm

# def index(request):
#     return render(request, 'tracker/consultation_history.html', context)

def new(request, child_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed('Only POST here')
    form = ConsultationHistoryForm(request.POST, request.FILES)
    if form.is_valid():
        saved_form = form.save()
        form = ConsultationHistoryForm(initial={'child': child_id})
    p = ConsultationHistory.objects.filter(child = child_id)
    context = {
        'form': form,
        'child_id': child_id,
        'consultation_history': p,
    }
    return render(request, 'tracker/consultation_history.html', context)

def view(request, child_id):
    p = ConsultationHistory.objects.filter(child = child_id)
    form = ConsultationHistoryForm(initial={'child': child_id})
    context = {
        'form': form,
        'child_id': child_id,
        'consultation_history': p,
    }
    return render(request, 'tracker/consultation_history.html', context)
