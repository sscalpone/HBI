import datetime

from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.shortcuts import render, get_object_or_404
from django.template import loader

from tracker.models import SocialExam
from tracker.models import SocialExamForm
from tracker.models import Signature
from tracker.models import SignatureForm
from tracker.models import Child

def index(request, child_id):
    list = SocialExam.objects.filter(child_id=child_id)
    child = get_object_or_404(Child, pk=child_id)
    context = {
        'SocialExams': list,
        'child_id': child_id,
        'child': child
    }
    return render(request, 'tracker/social_exam_history.html', context)

def new(request, child_id):
    child = get_object_or_404(Child, pk=child_id)
    if request.method == 'POST':
        signature_form = SignatureForm(request.POST, request.FILES, request=request)
        social_exam_form = SocialExamForm(request.POST, request.FILES, request=request)
        if 'discard' in request.POST:
            return HttpResponseRedirect(reverse('tracker:child', kwargs={'child_id': child_id}))
        else:
            if signature_form.is_valid() and social_exam_form.is_valid():
                signature = signature_form.save()
                if signature:
                    social_exam = social_exam_form.save(commit=False)
                    social_exam.signature = signature
                    social_exam.child = child
                    social_exam.save()
                    social_exam_form.save_m2m()
                    return HttpResponseRedirect(reverse('tracker:child', kwargs={'child_id': child_id}))
    else:
        social_exam_form = SocialExamForm(initial={
                'child': child,
                'child_id': child_id,
                'date': datetime.date.today(),
            }
        )
        signature_form = SignatureForm()
    social_exam_list = SocialExam.objects.filter(child_id=child_id)
    context = {
        'child': child,
        'child_id': child_id,
        'residence_id': child.residence_id,
        'social_exam_form': social_exam_form.as_ul,
        'signature_form': signature_form.as_ul,
        'SocialExams': social_exam_list,
    }
    return render(request, 'tracker/add_child_social_history.html', context)

def view(request, child_id, exam_id):
    p = get_object_or_404(SocialExam, pk=exam_id)
    child = get_object_or_404(Child, pk=child_id)
    context = {
        'exam': p,
        'child': child,
        'child_id': child.id,
        'residence_id': child.residence_id,
    }
    return render(request, 'tracker/social_exam.html', context)
