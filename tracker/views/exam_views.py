#coding=utf-8

"""

exam_views.py pulls the most recent exams completed for a child that
affect priority, and, based on the priorities of those exams, set
priority, and render the child_information template.

"""

from django.contrib.auth.decorators import login_required

from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from tracker.models import Child
from tracker.models import DentalExam
from tracker.models import MedicalExamPart1
from tracker.models import MedicalExamPart2
from tracker.models import PsychologicalExam
from tracker.models import SocialExam


"""The index.py function gets the most recently filled-out exams for
the exams that affect priority. It then checks the priority of each of
those exams, and based on the highest-rated priority of any of those
exams, sets the child's priority. It then renders the child-
information template.
"""

@login_required
def index(request, child_id):
    child = get_object_or_404(Child, pk=child_id)
    residence_id = child.residence_id
    if (request.POST):
        if ('discard' in request.POST):
            child.delete()
            return HttpResponseRedirect(reverse('tracker:add_child',
                                        kwargs={'residence_id': residence_id})
                                        )

    # Get last Dental Exam if one exists
    try:
        latest_dental_exam = DentalExam.objects.filter(
            child_id=child_id).latest('id')
    except:
        latest_dental_exam = None
    # Get last MedicalExamPart1 if one exists
    try:
        latest_medical_exam_part1 = MedicalExamPart1.objects.filter(
            child_id=child_id).latest('id')
    except:
        latest_medical_exam_part1 = None
    # Get last MedicalExamPart2 if one exists
    try:
        latest_medical_exam_part2 = MedicalExamPart2.objects.filter(
            child_id=child_id).latest('id')
    except:
        latest_medical_exam_part2 = None
    # Get last PsychologicalExam if one exists
    try:
        latest_psychological_exam = PsychologicalExam.objects.filter(
            child_id=child_id).latest('id')
    except:
        latest_psychological_exam = None
    # Get last SocialExam if one exists
    try:
        latest_social_exam = SocialExam.objects.filter(
            child_id=child_id).latest('id')
    except:
        latest_social_exam = None

    priority = 3  # Sets priority to low unless otherwise stated
    if (latest_dental_exam):
        if (latest_dental_exam.priority < priority):
            priority = latest_dental_exam.priority
    if (latest_social_exam):
        if (latest_social_exam.priority < priority):
            priority = latest_social_exam.priority
    if (latest_psychological_exam):
        if (latest_psychological_exam.priority < priority):
            priority = latest_psychological_exam.priority
    if (latest_medical_exam_part1):
        if (latest_medical_exam_part1.priority < priority):
            priority = latest_medical_exam_part1.priority
    if (latest_medical_exam_part2):
        if (latest_medical_exam_part2.priority < priority):
            priority = latest_medical_exam_part2.priority

    # Set child priority
    if (child.priority != priority):
        child.priority = priority
        child.save()

    # Render the child_information template
    context = {
        'child': child,
        'child_id': child_id,
        'residence_id': residence_id,
        'dental_exam': latest_dental_exam,
        'medical_exam_part1': latest_medical_exam_part1,
        'medical_exam_part2': latest_medical_exam_part2,
        'psychological_exam': latest_psychological_exam,
        'social_exam': latest_social_exam,
        'page': 'child',
    }
    return render(request, 'tracker/child_information.html', context)
