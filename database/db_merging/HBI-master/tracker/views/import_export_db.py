# coding=utf-8

import datetime
import os
import zipfile
import StringIO
import os
import os.path
import csv

from django.core.servers.basehttp import FileWrapper

from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.http import response, StreamingHttpResponse, HttpResponse, HttpResponseRedirect
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
from tracker.models import ImportDBForm

def check_file_type(file):
	file_type = mimetypes.guess_type(file.name)
	return file_type[0]

def handle_uploaded_file(file):
	pass


def compare_csv(model_csv, model_instance):
	with open(model_csv, 'rb') as f:
		reader = csv.reader(f)
		csv_list = list(reader)
		# print csv_list[0][1]
		for item in model_instance:
			for sublist in csv_list:
				if item.uuid in sublist[1]:
					# model_field_names = item._meta.get_all_field_names()
					# print len(model_field_names)
					# for i in csv_list[0]:
					# 	if i == 
		

def import_export_db(request):
	if (request.POST):

		# If request was to export the database, 
		# make csv files of each table and gzip them
		if ('submit_export' in request.POST):
			
			# Making the csv files using django-import-export app
			# saving them to the csvs directory
			tables = []

			child = ChildResource().export()
			with open('csvs/child.csv', 'w') as child_csv:
				child_csv.write(child.csv)
			tables.append('csvs/child.csv')

			dental_exam = DentalExamResource().export()
			with open('csvs/dental_exam.csv', 'w') as dental_exam_csv:
				dental_exam_csv.write(dental_exam.csv)
			tables.append('csvs/dental_exam.csv')

			documents = DocumentsResource().export()
			with open('csvs/documents.csv', 'w') as documents_csv:
				documents_csv.write(documents.csv)
			tables.append('csvs/documents.csv')

			growth = GrowthResource().export()
			with open('csvs/growth.csv', 'w') as growth_csv:
				growth_csv.write(growth.csv)
			tables.append('csvs/growth.csv')

			medical_exam_part1 = MedicalExamPart1Resource().export()
			with open('csvs/medical_exam_part1.csv', 'w') as medical_exam_part1_csv:
				medical_exam_part1_csv.write(medical_exam_part1.csv)
			tables.append('csvs/medical_exam_part1.csv')

			medical_exam_part2 = MedicalExamPart2Resource().export()
			with open('csvs/medical_exam_part2.csv', 'w') as medical_exam_part2_csv:
				medical_exam_part2_csv.write(medical_exam_part2.csv)
			tables.append('csvs/medical_exam_part2.csv')

			operation_history = OperationHistoryResource().export()
			with open('csvs/operation_history.csv', 'w') as operation_history_csv:
				operation_history_csv.write(operation_history.csv)
			tables.append('csvs/operation_history.csv')

			photograph = PhotographResource().export()
			with open('csvs/photograph.csv', 'w') as photograph_csv:
				photograph_csv.write(photograph.csv)
			tables.append('csvs/photograph.csv')

			user_uuid = UserUUIDResource().export()
			with open('csvs/user_uuid.csv', 'w') as user_uuid_csv:
				user_uuid_csv.write(user_uuid.csv)
			tables.append('csvs/user_uuid.csv')

			psychological_exam = PsychologicalExamResource().export()
			with open('csvs/psychological_exam.csv', 'w') as psychological_exam_csv:
				psychological_exam_csv.write(psychological_exam.csv)
			tables.append('csvs/psychological_exam.csv')

			residence = ResidenceResource().export()
			with open('csvs/residence.csv', 'w') as residence_csv:
				residence_csv.write(residence.csv)
			tables.append('csvs/residence.csv')

			signature = SignatureResource().export()
			with open('csvs/signature.csv', 'w') as signature_csv:
				signature_csv.write(signature.csv)
			tables.append('csvs/signature.csv')

			social_exam = SocialExamResource().export()
			with open('csvs/social_exam.csv', 'w') as social_exam_csv:
				social_exam_csv.write(social_exam.csv)
			tables.append('csvs/social_exam.csv')

			if (os.path.isfile('media/hbi-db-export.zip')):
				os.remove('media/hbi-db-export.zip')

			zippy = zipfile.ZipFile('media/hbi-db-export.zip', 'a')
			for item in tables:
				zippy.write(item)

			# response = HttpResponse(zippy, content_type="application/zip")
			# response['Content-Disposition'] = 'attachment; filename="hbi-db-export.zip"'

			# zippy.close()
			# return response
			form = ImportDBForm()

			context = {
				'zip_file': True,
				'page': 'import_export',
				'form': form.as_ul,
			}
			return render(request, 'tracker/import_export.html', context)

		# If request is to import the database - algorithm still being built 
		elif ('submit_import' in request.POST):
			form = ImportDBForm(request.POST, request.FILES)
			if form.is_valid():
				# handle_uploaded_file(request.FILES['upload'])
				with zipfile.ZipFile(request.FILES['upload']) as zf:
					zf.extractall('database/db_merging')

				compare_csv('database/db_merging/csvs/child.csv', Child.objects.all())

				messages.add_message(request, messages.SUCCESS, 
				'Yes!')
				return HttpResponseRedirect(reverse('tracker:import_export'))
			else:
				messages.add_message(request, messages.SUCCESS, 
				'No!')
				return HttpResponseRedirect(reverse('tracker:import_export'))
	
	else:
		form = ImportDBForm()			

		# Render the help.html template
		context = {
			'page': 'import_export',
			'form': form.as_ul,
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
