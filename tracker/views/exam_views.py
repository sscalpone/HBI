from django.shortcuts import render, render_to_response, get_object_or_404

from tracker.models import Child
from tracker.models import DentalExam
from tracker.models import MedicalExamPart1
from tracker.models import MedicalExamPart2
from tracker.models import PsychologicalExam
from tracker.models import SocialExam


def index(request, child_id):
	child = get_object_or_404(Child, pk=child_id)
	dental_exam_list = DentalExam.objects.filter(child_id=child_id)
	medical_exam_part_1_list = MedicalExamPart1.objects.filter(child_id=child_id)
	medical_exam_part_2_list = MedicalExamPart2.objects.filter(child_id=child_id)
	psychological_exam_list = PsychologicalExam.objects.filter(child_id=child_id)
	social_exam_list = SocialExam.objects.filter(child_id=child_id)
	context = {
		'child': child,
		'child_id': child_id,
		'DentalExams': dental_exam_list,
		'MedicalExamPart1s': medical_exam_part_1_list,
		'MedicalExamsPart2s': medical_exam_part_2_list,
		'PsychologicalExams': psychological_exam_list,
		'SocialExams': social_exam_list,		
	}
	return render(request, 'tracker/child_information.html', context)
