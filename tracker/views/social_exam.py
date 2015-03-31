import datetime

from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader

from tracker.models import SocialExam
from tracker.models import SocialExamForm
from tracker.models import Signature
from tracker.models import SignatureForm
from tracker.models import Child

def index(request, child_id):
    list = SocialExam.objects.filter(child_id=child_id)
    context = RequestContext(request, {
        'SocialExams': list,
        'child_id': child_id
    })
    return render(request, 'tracker/child_social_histories.html', context)

def new(request, child_id):
    child = get_object_or_404(Child, pk=child_id)
    if request.method == 'POST':
        signature_form = SignatureForm(request.POST, request.FILES)
        social_exam_form = SocialExamForm(request.POST, request.FILES)
        if signature_form.is_valid() and social_exam_form.is_valid():
            signature = signature_form.save()
            if signature:
                social_exam = social_exam_form.save(commit=False)
                social_exam.signature = signature
                social_exam.child = child
                if social_exam.save():
                    return HttpResponseRedirect(reverse('tracker:social_exams'))
    else:
        social_exam_form = SocialExamForm(initial={
                'child': child,
                'child_id': child_id,
                'date': datetime.date.today(),
            }
        )
        signature_form = SignatureForm()
    context = {
        'child': child,
        'child_id': child_id,
        'social_exam_form': social_exam_form,
        'signature_form': signature_form,
    }
    return render(request, 'tracker/add_child_social_history.html', context)

def view(request, exam_id):
    p = get_object_or_404(SocialExam, pk=exam_id)
    context = {
        'exam': p,
    }
    return render(request, 'tracker/child_social_history.html', context)
