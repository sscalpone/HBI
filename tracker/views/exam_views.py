#coding=utf-8

from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404

from tracker.models import Child
from tracker.models import DentalExam
from tracker.models import MedicalExamPart1
from tracker.models import MedicalExamPart2
from tracker.models import PsychologicalExam
from tracker.models import SocialExam


@login_required
def index(request, child_id):
	child = get_object_or_404(Child, pk=child_id)
	residence_id = child.residence_id
	try:
		latest_dental_exam = DentalExam.objects.filter(child_id=child_id).latest('id')
	except:
		latest_dental_exam = None
	try:
		latest_medical_exam_part2 = MedicalExamPart2.objects.filter(child_id=child_id).latest('id')
	except:
		latest_medical_exam_part2 = None
	try:
		latest_psychological_exam = PsychologicalExam.objects.filter(child_id=child_id).latest('id')
	except:
		latest_psychological_exam = None
	try:
		latest_social_exam = SocialExam.objects.filter(child_id=child_id).latest('id')
	except:
		latest_social_exam = None

	priority = 3
	if latest_dental_exam:
		if latest_dental_exam.priority < priority:
			priority = latest_dental_exam.priority
	if latest_social_exam:
		if latest_social_exam.priority < priority:
			priority = latest_social_exam.priority
	if latest_psychological_exam:
		if latest_psychological_exam.priority < priority:
			priority = latest_psychological_exam.priority
	if latest_medical_exam_part2:
		if latest_medical_exam_part2.priority < priority:
			priority = latest_medical_exam_part2.priority

	if child.priority != priority:
		child.priority = priority
		child.save()

	context = {
		'child': child,
		'child_id': child_id,
		'residence_id': residence_id,
		'dental_exam': latest_dental_exam,
		'medical_exam_part2': latest_medical_exam_part2,
		'psychological_exam': latest_psychological_exam,
		'social_exam': latest_social_exam,
		'page': 'child',	
	}
	return render(request, 'tracker/child_information.html', context)
