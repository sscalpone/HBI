# coding=utf-8

import datetime
import pytz
import zipfile
import os
import os.path
import csv

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

def compare_csv(file, model_instance, dependant_file_1=None, 
	dependant_file_2=None, dependant_file_3=None):

	csvfile = open(file, 'rb')
	not_reader = csv.reader(csvfile)
	headers = not_reader.next()
	csvfile.close()

	if (model_instance == 'residence'):
		field_names = [f.name for f in Residence._meta.fields]
	# elif (model_instance == 'child'):
	# 	field_names = [f.name for f in Child._meta.fields]
	for name in field_names:
		if name not in headers:
			return False

	csvfile = open(file, 'rb')
	reader = csv.DictReader(csvfile)

	# Iterate through the csv file, matching the UUIDs in the file to 
	# the children in the master database. If they exist, compare the
	# entire csv row to the Child and update appropriately. If they 
	# don't exist, create new children in the master.
	for row in reader:
		uuid_csv = row['uuid']
		try:
			if (model_instance == 'residence'):
				obj = Residence.objects.get(uuid=uuid_csv)
			# elif if (model_instance == 'child'):
			# 	obj = Child.objects.get(uuid=uuid_csv)
		
		except:
			# Create new instance of model who has never been in the 
			# database before
			if (not row['uuid']):
				pass
			
			# Create new instance of model who has been in the 
			# database, but not the master
			else:
				pass

		if obj:
			# if (pytz.utc.localize(datetime.datetime.strptime(
			# 	row['last_saved'], "%Y-%m-%d %H:%M:%S")) > getattr(obj, 'last_saved')):
			# 	csv_new = True
			# else:
			# 	csv_new = False
			
			# if (csv_new):
			for name in field_names:
				print type(getattr(obj,name))
				if (type(getattr(obj, name)) is int):

					# If the integer is an id of any sort, leave it.
					# It's either a reference to another object (in 
					# which case we already changed it in the master) 
					# or it's the pk, which we don't want to change in 
					# the master
					if "id" in name:
						pass
					# If it's not an id, convert the csv string to an 
					# integer and save it to the object
					else:
						setattr(obj, name, int(row[name]))

				# If it's a datetime, convert the string to a utc-aware 
				# datetime object and save it to the object (should 
				# only be applicable to last_saved)
				elif (type(getattr(obj, name)) is datetime.datetime):
					pytz.utc.localize(datetime.datetime.strptime(row[name], '%Y-%m-%d %H:%M:%S'))
					# doesn't work, not sure why
				
				# If it's a boolean object, check if the csv has it 
				# saved as true or false (1 or 0) and then set the 
				# object field with as a boolean
				elif (type(getattr(obj, name)) is bool):
					if (row[name] == '1'):
						setattr(obj, name, True)
					else:
						setattr(obj, name, False)

				# Since ImageFieldFile is a django class and there's no 
				# easy way to evaluate the time of django classes 
				# dynamically (that I could find), convert the type to 
				# a string and compare strings.
				# If it's an ImageFieldFile, probably save as a string probably don't do any conversions since it'll save as a string to the database anyway but we'll see.
				elif (type(getattr(obj, name)).__name__ == "ImageFieldFile"):
					pass
					# NEEDS WRITING
				# if it's a unicode field, just set the object, no 
				# conversion required.

				elif (type(getattr(obj, name)) is unicode):
					print "I am a string"
					setattr(obj, name, row[name])

			# Save the object to the database
			obj.save()
				# if (model_instance == 'residence'):
				# 	obj.residence_name = row['residence_name']
				# 	obj.administrator = row['administrator']
				# 	obj.administrator = row['location']
				# 	obj.administrator = row['photo']

				# elif (model_instance == 'child'):
				# 	d_csvfile = open(d_file_1, 'rb')
				# 	d_reader = csv.DictReader(d_csvfile)
				# 	for r in d_reader:
				# 		if (r['id'] == row['residence_id'])
				# 			residence_uuid=r['uuid']
				# 			break
				# 	residence = Residence.objects.get(uuid=residence_uudi)
				# 	obj.residence_id = residence.id
				# 	d_csvfile.close()

				# 	obj.first_name = row['first_name']
				# 	obj.last_name = row['last_name']
				# 	obj.nickname = row['nickname']
				# 	obj.birthdate = datetime.datetime.strptime(
				# 		row['birthdate'], '%Y-%M-%D')
				# 	obj.gender = row['gender']
				# 	obj.birthplace = row['birthplace']
				# 	obj.intake_date = datetime.datetime.strptime(
				# 		row['intake_date'], '%Y-%M-%D')
				# 	obj.discharge_date = datetime.datetime.strptime(
				# 		row['discharge_date'], '%Y-%M-%D')
				# 	obj.photo = row['photo']
				# 	obj.priority = int(row['priority'])
				# 	if (row['is_active'] == '1'):
				# 		obj.priority = True
				# 	else:
				# 		obj.priority = False

				# obj.last_saved = (pytz.utc.localize(datetime.datetime.strptime(row['last_saved'], "%Y-%m-%d %H:%M:%S"))

	csvfile.close()
		

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

				db_merging = compare_csv(
					'database/db_merging/csvs/residence.csv', 'residence')
				
				# db_merging = compare_csv(
				# 	'database/db_merging/csvs/child.csv', 'child', 'database/db_merging/csvs/residence.csv')				

				if (db_merging == False):
					messages.add_message(request, messages.SUCCESS, 
						'Please make sure all columns are present in your CSVs!')
					return HttpResponseRedirect(reverse('tracker:import_export'))
				else:
					
					messages.add_message(request, messages.SUCCESS, 'Yes!')
					return HttpResponseRedirect(
						reverse('tracker:import_export'))
			else:
				messages.add_message(request, messages.SUCCESS, 'No!')
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
