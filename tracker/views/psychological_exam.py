import datetime

from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader

from tracker.models import PsychologicalExam
from tracker.models import PsychologicalExamForm
from tracker.models import Signature
from tracker.models import SignatureForm
from tracker.models import Child

def index(request, child_id):
    list = PsychologicalExam.objects.filter(child_id=child_id)
    context = RequestContext(request, {
        'PsychologicalExams': list,
        'child_id': child_id
    })
    return render(request, 'tracker/child_psychological_histories.html', context)

def new(request, child_id):
    if request.method == 'POST':
        signature_form = SignatureForm(request.POST, request.FILES)
        psychological_exam_form = PsychologicalExamForm(request.POST, request.FILES)
        if signature_form.is_valid() and psychological_exam_form.is_valid():
            signature = signature_form.save()
            if signature:
                child = get_object_or_404(Child, pk=child_id)
                psychological_exam = psychological_exam_form.save(commit=False)
                psychological_exam.signature = signature
                psychological_exam.child = child
                if psychological_exam.save():
                    return HttpResponseRedirect(reverse('tracker:psychological_exams'))
    else:
        child = get_object_or_404(Child, pk=child_id)
        psychological_exam_form = PsychologicalExamForm(initial={
                'child': child_id,
                'date': datetime.date.today(),
            }
        )
        signature_form = SignatureForm()
    context = {
        'child_id': child_id,
        'psychological_exam_form': psychological_exam_form,
        'signature_form': signature_form,
    }
    return render(request, 'tracker/add_child_psychological_history.html', context)

def view(request, exam_id):
    p = get_object_or_404(PsychologicalExam, pk=exam_id)
    context = {
        'exam': p,
    }
    return render(request, 'tracker/child_psychological_history.html', context)
