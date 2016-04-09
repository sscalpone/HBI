# coding=utf-8

import csv
import datetime
import glob
import os
import pytz
import shutil
import zipfile

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
from tracker.models import DiseaseHistory
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

"""Function to check if any of the csv files are empty (except the
header). If they're empty, compare_csv doesn't need to be called 
because there's nothing to compare. Returns false is the file is empty,
returns true if it's not.
"""
def file_empty(csv_file):
	# get the headers in the csv file
	csvfile = open(csv_file, 'rb')
	reader = csv.DictReader(csvfile)
	has_rows = False
	for line in reader:
		has_rows = True
	csvfile.close()
	if (not has_rows):
		return True
	else:
		return False
	

"""Function that gets and returns any dependent objects by searching 
the dependencies dict, calling get_object, and appending them to a list
to be returned. Returns None if no dependent objects are found.
"""
def get_dependent_objects(object_name):
	# Dictionary of the models that have dependencies and what those 
	# dependencies are, so that when they're compared to the database, 
	# tables aren't accidentally overwritten because the pks were the 
	# same.
	dependencies = {
		'child': ['residence'],
		'dental_exam': ['child', 'signature'],
		'disease_history': ['child', 'signature'],
		'medical_exam_part1': ['child', 'signature'],
		'medical_exam_part2': ['child', 'signature'],
		'operation_history': ['child', 'signature'],
		'psychological_exam': ['child', 'signature'],
		'social_exam': ['child', 'signature'],
		'documents': ['child', 'signature'],
		'photograph': ['child'],
		'user_uuid': ['user'],
		'growth': ['child', 'medical_exam_part1'],
	}

	# Search the dependencies dict for passed model name
	for key in dependencies:
		# If the model has dependencies, get the dependencies' objects
		# and add them to a list to be returned
		if object_name == key:
			dependent_objects = {}
			for value in dependencies[key]:
				dependent_objects[value] = get_object(value)
			return dependent_objects

		# If the model has no dependencies, return None
		else:
			return None


"""Function returns an object based on the string that matches it's 
name, and returns False if that string doesn't match one of the models
listed. This will have to be updated if models are added.
"""
def get_object(object_name):
	if (object_name == 'residence'):
		return Residence
	elif (object_name == 'child'):
		return Child
	elif (object_name == 'dental_exam'):
		return DentalExam
	elif (object_name == 'documents'):
		return Documents
	elif (object_name == 'disease_history'):
		return DiseaseHistory
	elif (object_name == 'growth'):
		return Growth
	elif (object_name == 'medical_exam_part1'):
		return MedicalExamPart1
	elif (object_name == 'medical_exam_part2'):
		return MedicalExamPart2
	elif (object_name == 'photograph'):
		return Photograph
	elif (object_name == 'operation_history'):
		return OperationHistory
	elif (object_name == 'user_uuid'):
		return UserUUID
	elif (object_name == 'psychological_exam'):
		return PsychologicalExam
	elif (object_name == 'signature'):
		return Signature
	elif (object_name == 'social_exam'):
		return SocialExam
	else:
		return False

"""Function to make sure all fields in the database are accounted for 
in the csv file. It compares the header in the csv to the field names 
in the object and returns None if they are all there. If it finds 
any missing, or finds extra fields in the csv header, it adds them to 
two lists and returns them in a dict.
"""
def missing_or_extra_fields(file, obj):
	# get the headers in the csv file
	csvfile = open(file, 'rb')
	reader = csv.reader(csvfile)
	headers = reader.next()
	csvfile.close()

	# get field names from object
	field_names = [f.name for f in obj._meta.fields]
	field_strings = [str(fn) for fn in field_names]
	
	missing_headers = list()
	extra_headers = list()
	# Check for missing fields in csv
	for name in field_strings:
		if name not in headers:
			missing_headers.append(name)
	# Check for extra fields in csv
	for h in headers:
		if h not in field_strings:
			extra_headers.append(h)
	
	# All fields are there and there are no extra fields. Return None.
	if not missing_headers or not extra_headers:
		return None
	# There are missing or extra fields in the csv. Return those fields 
	# in a dictionary so they can be added to a message.
	else:
		return {'missing_headers': missing_headers, 'extra_headers': extra_headers,}

"""This function opens the passed-in csv file and compares it to the 
master database, saving the more recent row to the master database.
"""
def compare_csv(file, model_instance, dependent_objects_dict=None):
	# Open the csv file as a dictionary so it's searchable by field 
	# name
	csvfile = open(file, 'rb')
	reader = csv.DictReader(csvfile)

	# Iterate through the csv file, matching the UUIDs in the file to 
	# the children in the master database. If they exist, compare the
	# entire csv row to the Child and update appropriately. If they 
	# don't exist, create new children in the master.
	for row in reader:
		uuid_csv = row['uuid']
		obj_inst = None # currently for if obj_inst, but hopefully that'll be written out
		try:
			# Based on the model_instance string, get the object that
			# might be edited from the master db.
			obj = get_object(model_instance)
			obj_inst = obj.objects.get(uuid=uuid_csv)
		
		except:
			# Create new instance of model who has never been in the 
			# database before
			if (not row['uuid']):
				pass
			
			# Create new instance of model who has been in the 
			# database, but not the master
			else:
				pass

		# If object exists, compare the object's last_saved field with
		# the corresponding object in the csv. If the csv object is 
		# newer, edit the master db.
		if obj_inst:
			if (pytz.utc.localize(datetime.datetime.strptime(
				row['last_saved'], "%Y-%m-%d %H:%M:%S")) > getattr(obj_inst, 'last_saved')):
				if dependent_objects_list:
						for key, value in dependent_objects_list:
							dependent_id = row[key]
							value.objects.get(pk=dependent_id)

							# get dependent_id from row and use it to search the pks in dependent
							# get uuid from dependent
							# get object with uuid and get it's pk
							# save pk to dependent_id in obj

				for name in field_names:

					
					# IntegerField: convert string to integer and save to object
					if (obj_inst._meta.get_field(name).get_internal_type() == 'IntegerField'):
							setattr(obj_inst, name, int(row[name]))

					# FloatField: convert string to float and save to object
					elif (obj_inst._meta.get_field(name).get_internal_type() == 'FloatField'):
						setattr(obj_inst, name, float(row[name]))

					# DateTimeField: convert string to a utc-aware datetime object and save it to object (should only be applicable to last_saved)
					elif (obj_inst._meta.get_field(name).get_internal_type() == 'DateTimeField'):
						setattr(obj_inst, name, pytz.utc.localize(datetime.datetime.strptime(row[name], '%Y-%m-%d %H:%M:%S')))

					# DateField: convert string to datetime object, conert that to a date object and and save it to object
					elif (obj_inst._meta.get_field(name).get_internal_type() == 'DateField'):
						setattr(obj_inst, name, datetime.datetime.strptime(row[name], '%d/%m/%Y').date())
					
					# BooleanField: check if the csv has it saved as true or false (1 or 0) and then set the object field with as a boolean
					elif (obj_inst._meta.get_field(name).get_internal_type() == 'BooleanField'):
						if (row[name] == '1'):
							setattr(obj_inst, name, True)
						else:
							setattr(obj_inst, name, False)

					# FileFieldField: just set the object, no conversion required.
					elif (obj_inst._meta.get_field(name).get_internal_type() == 'FileField'):
						setattr(obj_inst, name, row[name])
						# NEEDS WRITING

					# CharField: just set the object, no conversion required.
					elif (obj_inst._meta.get_field(name).get_internal_type() == 'CharField'):
						setattr(obj_inst, name, row[name])

					# TextField: just set the object, no conversion required.
					elif (obj_inst._meta.get_field(name).get_internal_type() == 'TextField'):
						setattr(obj_inst, name, row[name])

					# If none of those are correct, print them out so I can see what I'm missing
					else:
						print "Unknown field type: %s" % obj_inst._meta.get_field(name).get_internal_type()

				# Save the object to the database
				obj_inst.save()

			else:
				pass

	csvfile.close()
		
"""This function exports the database using the import-export django 
app, and imports csvs to be read into the database.
"""
def import_export_db(request):
	if (request.POST):

		# If request was to export the database, 
		# make csv files of each table and gzip them
		if ('submit_export' in request.POST):
			
			# Making the csv files using django-import-export app
			# saving them to the csvs directory
			# LOOK INTO TURNING THIS INTO A LOOP
			tables = [] # logs the csv names to be zipped

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

			disease_history = DiseaseHistoryResource().export()
			with open('csvs/disease_history.csv', 'w') as disease_history_csv:
				disease_history_csv.write(disease_history.csv)
			tables.append('csvs/disease_history.csv')

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

			# Before zipping file, remove any previously zipped 
			# database file.
			if (os.path.isfile('media/hbi-db-export.zip')):
				os.remove('media/hbi-db-export.zip')

			# Zip the csvs together -- currently not compressed because it's not a fan, will try again soon.
			zippy = zipfile.ZipFile('media/hbi-db-export.zip', 'a')
			for item in tables:
				zippy.write(item)

			# Since serving the zipped file as an attachment corrupted
			#  the file (most likely because django isn't equipped to 
			# serve larger files), render it in the import_export 
			# template for download.
			form = ImportDBForm()

			context = {
				'zip_file': True,
				'page': 'import_export',
				'form': form.as_ul,
			}
			return render(request, 'tracker/import_export.html', context)





		# If request is to import the database, get the posted file
		elif ('submit_import' in request.POST):
			form = ImportDBForm(request.POST, request.FILES)

			# If the form posted a file, get it and extract it.
			if form.is_valid():
				upload_name, upload_extension = request.FILES['upload'].name.split('.')
				if os.path.isdir('database/db_merging/csvs'):
					shutil.rmtree('database/db_merging/csvs')
				if (upload_extension == 'zip'):
					with zipfile.ZipFile(request.FILES['upload']) as zf:
						zf.extractall('database/db_merging')
					# Check that csvs directory was created
					if (not os.path.isdir('database/db_merging/csvs')):
						# If not, check how many directories are in file
						path = 'database/db_merging/*'
						dir_count = 0
						for p in glob.glob(path):
							if os.path.isdir(p):
								i++
						# If there are no directories in the file, 
						# return "don't zip single files" error message
						if (dir_count == 0):
							messages.add_message(request, messages.ERROR, 'There was a problem unzipping your file. If you are uploading a single file, do not upload it in a zip format. Otherwise, please re-compress and try again.')
							return HttpResponseRedirect(reverse('tracker:import_export'))
						
						# If there are two or more directories, return "too many folders" error message
						elif (dir_count > 1):
							messages.add_message(request, messages.ERROR, 'There was a problem unzipping your file. If you are zipping multiple folders together, please zip them separately.')
							return HttpResponseRedirect(reverse('tracker:import_export'))
						
						# If there's only one directory, get it and rename it 'csvs'
						else:
							for p in glob.glob(path):
								if isdir(p):
									os.rename(p, 'csvs')
									messages.add_message(request, messages.SUCCESS, 'In the future, please make sure the folder you upload is called csvs.')


				elif (upload_extension == 'csv'):
					os.mkdir('database/db_merging/csvs')
					with open('database/db_merging/csvs/%s.csv' % upload_name, 'wb+') as destination:
						for chunk in request.FILES['upload'].chunks():
							destination.write(chunk)
				# If file is not zipped or not csv (not currently written yet), return with error message
				else:
					messages.add_message(request, messages.ERROR, 'Incorrect File Type: .%s files are not compatible with our database.' % upload_extension)
					return HttpResponseRedirect(reverse('tracker:import_export'))

				path = 'database/db_merging/csvs/*'
				for pathname in glob.glob(path):
					basename = os.path.basename(pathname)
					if (not basename.endswith('.csv')):
						messages.add_message(request, messages.ERROR, ('%s needs to be a csv file to be read (if file is already a csv, please add the extension .csv).' % basename))
						os.remove(pathname) # remove empty csv


				# Create a glob path so the paths to the csvs can be 
				# passed to functions for every csv through a loop
				path = 'database/db_merging/csvs/*.csv'

				# Loop through the csvs directory four times:
				# First, check that all the csvs correspond to a model.
				# Second, check that all fields are present in each 
				# csv.
				# Third, make sure all files are populated. This won't break anything, but might be useful information for the user.
				# Fourth, compare the csv to the database and save the 
				# more recent data
				for i in range(5):
					for pname in glob.glob(path):
						# get the table name by parsing the path name
						bname = os.path.basename(pname)
						tname, extension = bname.split('.')
						
						# FIRST LOOP: Identify and Remove CSVS that Don't Match Database Headers
						if (i == 0):
							# Check that each csv corresponds to a table in the database. If a table that does not exist appears, render the import_export template with an error message saying which csv doesn't correspond.
							if (not get_object(tname)):
								messages.add_message(request, messages.ERROR, 
									('%s does not correspond to any table in the '
									'database. Please re-upload with the correct '
									'file name.' % bname))
								os.remove(pname) # remove defective csv
						
						# SECOND LOOP: Identify and Remove CSVs with Missing or Extra Fields
						elif (i == 1):
							model_obj = get_object(tname)

							# Check if all fields exist in the csv. If it comes up
							mef_check = missing_or_extra_fields(pname, model_obj)
							if (mef_check is not None):
								# If there are missing headers, add a error message to be displayed on render of all the fields missing in that csv file.
								if (mef_check['missing_headers']):
									missing_headers = ', '.join(
										mef_check['missing_headers'])
									messages.add_message(request, messages.ERROR,
										('The following fields are missing from %s'
										': %s. Please add those fields and '
										're-upload' % (bname, missing_headers)))

								# If there are extra headers, add a error message to be displayed on render of all the extra fields in that csv file.
								if (mef_check['extra_headers']):
									extra_headers = ', '.join(
										mef_check['extra_headers'])
									messages.add_message(request, messages.ERROR,
										('The following fields from %s do not '
										'exist in the database: %s. Please either'
										' rename or remove these fields before '
										're-uploading.' % (bname, extra_headers)
										))
								os.remove(pname) # remove broken csv
						
						# THIRD LOOP: Identify and Remove Empty CSVs (except header)
						elif (i == 2):
							if (file_empty(pname)):
								messages.add_message(request, messages.ERROR, 
									('%s is empty. If that is correct, please ignore this message.' % bname))
								os.remove(pname) # remove empty csv

						# FOURTH LOOP: Indentify dependent objects and locate their csvs
						elif (i == 3):
							# If the current object is dependent on other objects, search the csvs directory for csvs that match the dependent objects and add those csvs to a dependents_csvs dict
							dependents_objects = get_dependent_objects(tname)
							if (dependents_objects is not None):
								dependents_csvs = {}

								# check each key against the csvs directory
								for key in dependents_objects:
									for pathname in glob.glob(path):
										basename = os.path.basename(pathname)
										tablename, extension = basename.split('.')

										# if a csv matching the dependent_object exists, add the csv to dependents_csv
										if (key == tablename):
											dependents_csvs[key]=pathname
								# If there not the same number of dependents in the objects dict and the csvs dict, create list of missing csvs, add a message, and remove the csv with dependents that don't exist.
								if (len(dependents_objects) != len(dependents_csvs)):
									missing_dependents_list = []
									for key in dependents_objects:
										if key not in dependents_csvs:
											missing_dependents.append(key) # stitch list together to add to message
									missing_dependents = ('.csv, ').join(missing_dependents_list)
									messages.add_message(request, messages.ERROR,
										('%s needs the following files to upload correctly'
										': %s. Please add those files to your zip and '
										're-upload.' % (bname, missing_dependents)))
									os.remove(pname) # remove empty csv


						# FIFTH LOOP: Finally, Compare CSV to Database
						# Currently not a part of the loop for sake of testing without breaking anything
						elif (i == 4):
							# If there are dependent objects (that exist in the csvs directory)
							if (dependents_objects is not None):
								compare_csv(pname, tname, dependents_objects, dependents_csvs)

							# If no dependents, just pass in the csv and the table name
							else:
								compare_csv(pname, tname)

						# compare_csv(
						# 	'database/db_merging/csvs/residence.csv', 'residence')

							# compare_csv(
							# 	'database/db_merging/csvs/child.csv', 'child', 'database/db_merging/csvs/child.csv')

				messages.add_message(request, messages.SUCCESS, 'Database Imported!')
				return HttpResponseRedirect(
					reverse('tracker:import_export'))

			else:
				messages.add_message(request, messages.SUCCESS, 'Please add a file to be imported!')
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

class DiseaseHistoryResource(resources.ModelResource):

    class Meta:
        model = DiseaseHistory

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
