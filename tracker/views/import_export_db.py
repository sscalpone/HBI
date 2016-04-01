# coding=utf-8

import datetime
# from zipfile import ZipFile
# import csv
import gzip
import shutil

from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail

from import_export import resources

from tracker.models import Child
from tracker.models import DentalExam
from tracker.models import Documents
from tracker.models import Growth
from tracker.models import MedicalExamPart1
from tracker.models import MedicalExamPart2
from tracker.models import OperationHistory
from tracker.models import Photograph
from tracker.models import UserUUID
from tracker.models import PsychologicalExam
from tracker.models import Residence
from tracker.models import Signature
from tracker.models import SocialExam

@login_required
def import_export_db(request):
	if (request.POST):

		# If request was to export the database
		if ('submit_export' in request.POST):
			
			child = ChildResource().export()
			with open('csvs/child.csv', 'w') as child_csv:
				child_csv.write(child.csv)

			with open('csvs/child.csv', 'rb') as f_in, gzip.open('child.csv.gz', 'wb') as f_out:
				shutil.copyfileobj(f_in, f_out) 

			# gzipped = gzip.GzipFile(mode='wb', fileobj=child_csv)

			# with ZipFile('hbi_db.zip', 'w') as myzip:
			# 	myzip.write(child_csv)
			
			dental_exam = DentalExamResource().export()
			documents = DocumentsResource().export()
			growth = GrowthResource().export()
			medical_exam_part1 = MedicalExamPart1Resource().export()
			medical_exam_part2 = MedicalExamPart2Resource().export()
			operation_history = OperationHistoryResource().export()
			photograph = PhotographResource().export()
			user_uuid = UserUUIDResource().export()
			psychological_exam = PsychologicalExamResource().export()
			residence = ResidenceResource().export()
			signature = SignatureResource().export()
			social_exam = SocialExamResource().export()

			messages.add_message(request, messages.SUCCESS, 
				'The database was printed!')
			return HttpResponseRedirect(reverse('tracker:import_export'))
		
		# If request is to import the database - algorithm still being built
		elif ('submit_import' in request.POST):
			pass

	# Render the help.html template
	context = {
		'page': 'import_export',
	}
	return render(request, 'tracker/import_export.html', context)


class ChildResource(resources.ModelResource):

    class Meta:
        model = Child


class DentalExamResource(resources.ModelResource):

    class Meta:
        model = DentalExam


class DocumentsResource(resources.ModelResource):

    class Meta:
        model = Documents

class GrowthResource(resources.ModelResource):

    class Meta:
        model = Growth


class MedicalExamPart1Resource(resources.ModelResource):

    class Meta:
        model = MedicalExamPart1


class MedicalExamPart2Resource(resources.ModelResource):

    class Meta:
        model = MedicalExamPart2


class OperationHistoryResource(resources.ModelResource):

    class Meta:
        model = OperationHistory


class PhotographResource(resources.ModelResource):

    class Meta:
        model = Photograph


class UserUUIDResource(resources.ModelResource):

    class Meta:
        model = UserUUID


class PsychologicalExamResource(resources.ModelResource):

    class Meta:
        model = PsychologicalExam


class ResidenceResource(resources.ModelResource):

    class Meta:
        model = Residence


class SignatureResource(resources.ModelResource):

    class Meta:
        model = Signature


class SocialExamResource(resources.ModelResource):

    class Meta:
        model = SocialExam
