import datetime

from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.shortcuts import render, get_object_or_404
from django.template import loader

from tracker.models import PsychologicalExam
from tracker.models import PsychologicalExamForm
from tracker.models import Signature
from tracker.models import SignatureForm
from tracker.models import Child

def index(request, child_id):
    list = PsychologicalExam.objects.filter(child_id=child_id)
    child = get_object_or_404(Child, pk=child_id)
    context = {
        'PsychologicalExams': list,
        'child_id': child_id,
        'child': child
    }
    return render(request, 'tracker/add_psychological_exam.html', context)

def new(request, child_id):
    child = get_object_or_404(Child, pk=child_id)
    if request.method == 'POST':
        signature_form = SignatureForm(request.POST, request.FILES, request=request)
        psychological_exam_form = PsychologicalExamForm(request.POST, request.FILES, request=request)
        if 'discard' in request.POST:
            return HttpResponseRedirect(reverse('tracker:child', kwargs={'child_id': child_id}))
        else:
            if signature_form.is_valid() and psychological_exam_form.is_valid():
                signature = signature_form.save()
                if signature:
                    psychological_exam = psychological_exam_form.save(commit=False)
                    psychological_exam.signature = signature
                    psychological_exam.child = child
                    psychological_exam.save()
                    psychological_exam_form.save_m2m()
                    return HttpResponseRedirect(reverse('tracker:child', kwargs={'child_id': child_id}))
    else:
        psychological_exam_form = PsychologicalExamForm(initial={
                'child': child,
                'child_id': child_id,
                'date': datetime.date.today(),
            }
        )
        signature_form = SignatureForm()
    psychological_exam_list = PsychologicalExam.objects.filter(child_id=child_id)
    context = {
        'child': child,
        'child_id': child_id,
        'residence_id': child.residence_id,
        'psychological_exam_form': psychological_exam_form.as_ul,
        'signature_form': signature_form.as_ul,
        'PsychologicalExams': psychological_exam_list,
    }
    return render(request, 'tracker/add_psychological_exam.html', context)

def view(request, child_id, exam_id):
    p = get_object_or_404(PsychologicalExam, pk=exam_id)
    child = get_object_or_404(Child, pk=child_id)
    signature = get_object_or_404(Signature, pk=p.signature_id)
    context = {
        'exam': p,
        'child': child,
        'child_id': child.id,
        'residence_id': child.residence_id,
        'signature': signature,

    }
    return render(request, 'tracker/psychological_exam.html', context)

def edit(request, child_id, exam_id):
    child = get_object_or_404(Child, pk=child_id)
    exam = get_object_or_404(PsychologicalExam, pk=exam_id)
    signature = get_object_or_404(Signature, id=exam.signature_id)
    if request.method == 'POST':
        signature_form = SignatureForm(request.POST, request.FILES, instance=signature, request=request)
        exam_form = PsychologicalExamForm(request.POST, request.FILES, instance=exam, request=request)
        if 'discard' in request.POST:
            return HttpResponseRedirect(reverse('tracker:child', kwargs={'child_id': child_id}))
        else:
            if signature_form.is_valid() and exam_form.is_valid():
                saved_signature = signature_form.save()
                if saved_signature:
                    saved_exam = exam_form.save(commit=False)
                    saved_exam.signature = saved_signature
                    saved_exam.child = child
                    saved_exam.save()
                    exam_form.save_m2m()
                    return HttpResponseRedirect(reverse('tracker:child', kwargs={'child_id': child_id}))
    else:
        exam_form = PsychologicalExamForm(initial={
                'child': child,
                'child_id': child_id,
                'date': datetime.date.today(),
            }, instance=exam
        )
        signature_form = SignatureForm(instance=signature)
    exam_list = PsychologicalExam.objects.filter(child_id=child_id)
    context = {
        'child': child,
        'child_id': child_id,
        'exam_id': exam.id,
        'residence_id': child.residence_id,
        'psychological_exam_form': exam_form.as_ul,
        'signature_form': signature_form.as_ul,
        'PsychologicalExams': exam_list,
    }
    return render(request, 'tracker/edit_psychological_exam.html', context)





