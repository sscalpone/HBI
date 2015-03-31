import datetime

from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader

from tracker.models import MedicalExamPart1
from tracker.models import MedicalExamPart1Form
from tracker.models import Signature
from tracker.models import SignatureForm
from tracker.models import Child

def index(request, child_id):
    list = MedicalExamPart1.objects.filter(child_id=child_id)
    context = RequestContext(request, {
        'Medical Exams': list,
        'child_id': child_id
    })
    return render(request, 'tracker/child_medical_exam_part1_histories.html', context)

def new(request, child_id):
    child = get_object_or_404(Child, pk=child_id)
    if request.method == 'POST':
        signature_form = SignatureForm(request.POST, request.FILES)
        medical_exam_part1_form = MedicalExamPart1Form(request.POST, request.FILES)
        if signature_form.is_valid() and medical_exam_part1_form.is_valid():
            signature = signature_form.save()
            if signature:
                medical_exam_part1 = medical_exam_part1_form.save(commit=False)
                medical_exam_part1.signature = signature
                medical_exam_part1.child = child
                if medical_exam_part1.save():
                    return HttpResponseRedirect(reverse('tracker:medical_exam_part1s'))
    else:
        medical_exam_part1_form = MedicalExamPart1Form(initial={
                'child': child,
                'child_id': child_id,
                'date': datetime.date.today(),
            }
        )
        signature_form = SignatureForm()
    context = {
        'child': child,
        'child_id': child_id,
        'medical_exam_part1_form': medical_exam_part1_form,
        'signature_form': signature_form,
    }
    return render(request, 'tracker/add_child_medical_exam_part1_history.html', context)

def view(request, exam_id):
    p = get_object_or_404(MedicalExamPart1, pk=exam_id)
    context = {
        'exam': p,
    }
    return render(request, 'tracker/child_medical_exam_part1_history.html', context)
