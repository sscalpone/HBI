import datetime

from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader

from tracker.models import DentalExam
from tracker.models import DentalExamForm
from tracker.models import Signature
from tracker.models import SignatureForm
from tracker.models import Child

def index(request, child_id):
    list = DentalExam.objects.filter(child_id=child_id)
    context = RequestContext(request, {
        'DentalExams': list,
        'child_id': child_id
    })
    return render(request, 'tracker/child_dental_histories.html', context)

def new(request, child_id):
    child = get_object_or_404(Child, pk=child_id)
    if request.method == 'POST':
        signature_form = SignatureForm(request.POST, request.FILES)
        dental_exam_form = DentalExamForm(request.POST, request.FILES)
        if signature_form.is_valid() and dental_exam_form.is_valid():
            signature = signature_form.save()
            if signature:
                dental_exam = dental_exam_form.save(commit=False)
                dental_exam.signature = signature
                dental_exam.child = child
                if dental_exam.save():
                    return HttpResponseRedirect(reverse('tracker:dental_exams'))
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
        'dental_exam_form': dental_exam_form,
        'signature_form': signature_form,
    }
    return render(request, 'tracker/add_child_dental_history.html', context)

def view(request, exam_id):
    p = get_object_or_404(DentalExam, pk=exam_id)
    context = {
        'exam': p,
    }
    return render(request, 'tracker/child_dental_history.html', context)
