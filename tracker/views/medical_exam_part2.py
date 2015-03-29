import datetime

from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader

from tracker.models import MedicalExamPart2
from tracker.models import MedicalExamPart2Form
from tracker.models import Signature
from tracker.models import SignatureForm
from tracker.models import Child

def index(request, child_id):
    list = MedicalExamPart2.objects.filter(child_id=child_id)
    context = RequestContext(request, {
        'Medical Exams': list,
        'child_id': child_id
    })
    return render(request, 'tracker/child_medical_exam_part2_histories.html', context)

def new(request, child_id):
    if request.method == 'POST':
        signature_form = SignatureForm(request.POST, request.FILES)
        medical_exam_part2_form = MedicalExamPart2Form(request.POST, request.FILES)
        if signature_form.is_valid() and medical_exam_part2_form.is_valid():
            signature = signature_form.save()
            if signature:
                child = get_object_or_404(Child, pk=child_id)
                medical_exam_part2 = medical_exam_part2_form.save(commit=False)
                medical_exam_part2.signature = signature
                medical_exam_part2.child = child
                if medical_exam_part2.save():
                    return HttpResponseRedirect(reverse('tracker:medical_exam_part2s'))
    else:
        child = get_object_or_404(Child, pk=child_id)
        medical_exam_part2_form = MedicalExamPart2Form(initial={
                'child': child_id,
                'date': datetime.date.today(),
            }
        )
        signature_form = SignatureForm()
    context = {
        'child_id': child_id,
        'medical_exam_part2_form': medical_exam_part2_form,
        'signature_form': signature_form,
    }
    return render(request, 'tracker/add_child_medical_exam_part2_history.html', context)

def view(request, exam_id):
    p = get_object_or_404(MedicalExamPart2, pk=exam_id)
    context = {
        'exam': p,
    }
    return render(request, 'tracker/child_medical_exam_part2_history.html', context)
