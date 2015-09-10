import datetime

from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.shortcuts import render, get_object_or_404
from django.template import loader
import django.template.loader

from tracker.models import DentalExam, DentalExamForm
from tracker.models import Signature, SignatureForm
from tracker.models import Child

def index(request, child_id):
    list = DentalExam.objects.filter(child_id=child_id)
    child = get_object_or_404(Child, pk=child_id)
    context = {
        'DentalExams': list,
        'child': child,
        'child_id': child_id
    }
    return render(request, 'tracker/dental_exam_history.html', context)

def new(request, child_id):
    child = get_object_or_404(Child, pk=child_id)
    if request.method == 'POST':
        signature_form = SignatureForm(request.POST, request.FILES, request=request)
        dental_exam_form = DentalExamForm(request.POST, request.FILES, request=request)
        if 'discard' in request.POST:
            return HttpResponseRedirect(reverse('tracker:child', kwargs={'child_id': child_id}))

        else:
            if signature_form.is_valid() and dental_exam_form.is_valid():
                signature = signature_form.save()
                if signature:
                    dental_exam = dental_exam_form.save(commit=False)
                    dental_exam.signature = signature
                    dental_exam.child = child
                    dental_exam.save()
                    dental_exam_form.save_m2m()
                    return HttpResponseRedirect(reverse('tracker:child', kwargs={'child_id': child_id}))  
        
    else:
        dental_exam_form = DentalExamForm(initial={
                'child': child,
                'child_id': child_id,
                'date': datetime.date.today(),
            }
        )
        signature_form = SignatureForm()
    context = {
        'child': child,
        'child_id': child_id,
        'dental_exam_form': dental_exam_form.as_ul,
        'signature_form': signature_form.as_ul,
    }
    return render(request, 'tracker/add_child_dental_history.html', context)

def view(request, child_id, exam_id):
    p = get_object_or_404(DentalExam, pk=exam_id)
    child = get_object_or_404(Child, pk=child_id)
    context = {
        'exam': p,
        'child': child,
        'child_id': child.id
    }
    return render(request, 'tracker/dental_exam.html', context)
