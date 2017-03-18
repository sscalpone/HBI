# coding=utf-8

import csv
import datetime
import glob
import os
import pytz
import shutil
import zipfile
import uuid
from tempfile import NamedTemporaryFile

from import_export import resources
import dateutil.parser

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from tracker.models import Child
from tracker.models import DentalExam
from tracker.models import DischargePlan
from tracker.models import DiseaseHistory
from tracker.models import Documents
from tracker.models import MedicalExamPart1
from tracker.models import MedicalExamPart2
from tracker.models import OperationHistory
from tracker.models import Photograph
from tracker.models import PsychologicalExam
from tracker.models import Residence
from tracker.models import SocialExam
from tracker.models import CustomUser as User

from tracker.models import ImportDBForm

from tracker.views.profile import is_superuser_check


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
    elif (object_name == 'discharge_plan'):
        return DischargePlan
    elif (object_name == 'disease_history'):
        return DiseaseHistory
    elif (object_name == 'medical_exam_part1'):
        return MedicalExamPart1
    elif (object_name == 'medical_exam_part2'):
        return MedicalExamPart2
    elif (object_name == 'photograph'):
        return Photograph
    elif (object_name == 'operation_history'):
        return OperationHistory
    elif (object_name == 'user'):
        return User
    elif (object_name == 'psychological_exam'):
        return PsychologicalExam
    elif (object_name == 'social_exam'):
        return SocialExam
    else:
        return False

# Dictionary of the models that have dependencies and what those
# dependencies are, so that when they're compared to the database,
# tables aren't accidentally overwritten because the pks were the
# same.
dependencies = {
    'child': ['residence'],
    'dental_exam': ['child'],
    'discharge_plan': ['child'],
    'disease_history': ['child'],
    'documents': ['child'],
    'medical_exam_part1': ['child'],
    'medical_exam_part2': ['child'],
    'operation_history': ['child'],
    'psychological_exam': ['child'],
    'social_exam': ['child'],
    'documents': ['child'],
    'photograph': ['child'],
    'user': ['residence'],
}


"""Returns true if a given object's name can be found in the
dependencies function, meaning that the object is dependent on other
objects.
"""

def is_dependent(object_name):
    for key in dependencies:
        if (key == object_name):
            return True
    return False


"""If a given object is dependent on other objects, this function will
return a list of those dependencies. Otherwise, it returns None.
"""

def get_dependents_list(object_name):
    if (is_dependent(object_name)):
        for key in dependencies:
            if (object_name == key):
                return dependencies[key]
    else:
        return None


"""Gets all the csvs that match the names in the dependents list and
returns the csvs dict.
"""

def get_dependents_csvs(object_name, path):
    dependents_list = get_dependents_list(object_name)
    dependents_csvs = {}

    # check each key against the csvs directory
    if dependents_list:
        for dependent in dependents_list:
            for pathname in glob.glob(path):
                basename = os.path.basename(pathname)
                tablename, extension = basename.split('.')

                # if a csv matching the dependent_object exists, add
                # the csv to dependents_csv
                if (dependent == tablename):
                    dependents_csvs[dependent] = pathname

        return dependents_csvs

    # if there are no dependents, return None
    return None


"""Function to check if any of the csv files are empty (except the
header). If they're empty, compare_csv doesn't need to be called
because there's nothing to compare. Returns false is the file is empty,
returns true if it's not.
"""

def file_empty(csv_file):
    has_rows = False
    with open(csv_file, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            has_rows = True
    if (not has_rows):
        return True
    else:
        return False


"""Function to check that the csv's id field and dependent reference
ids field are populated. If not, return a list of which fields have
blank values. If they are, return None.
"""

def ids_not_empty(file, model_instance):
    blank_fields = []

    with open(file, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        dependents_names = get_dependents_list(model_instance)
        for row in reader:
            if (row['id'] == ''):
                if ('id' not in blank_fields):
                    blank_fields.append('id')
            if (model_instance != 'user'):
                if dependents_names:
                    for name in dependents_names:
                        if (row[name] == ''):
                            if (name not in blank_fields):
                                blank_fields.append(name)

    if (blank_fields):
        return blank_fields
    else:
        return None


"""Function that checks for repeated ids and uuids in a passed-in csv.
It returns a list of which fields have repetitions (list is empty if
there are no repetitions). This could be DRYer but it can easily cause
an infinite loop so it's being left alone for now.
"""

def ids_uuids_unique(file):
    # get the headers in the csv file
    # csvfile = open(file, 'rb')
    # reader = csv.reader(csvfile)
    # headers = reader.next()
    # csvfile.close()

    csvfile = open(file, 'rb')
    reader = csv.DictReader(csvfile)
    duplicate_in_field = []

    ids_count = 0
    uuids_count = 0
    unique_ids = []
    unique_uuids = []

    for row in reader:
        if (row['id'] not in unique_ids):
            unique_ids.append(row['id'])
        ids_count += 1
        if row['uuid'] != '':
            if (row['uuid'] not in unique_uuids):
                unique_uuids.append(row['uuid'])

            # counting the nonempty uuids
            uuids_count += 1
    if len(unique_ids) < ids_count:
        duplicate_in_field.append('id')

    if len(unique_uuids) < uuids_count:
        duplicate_in_field.append('uuid')

    csvfile.close()
    if duplicate_in_field:
        return duplicate_in_field
    else:
        return None

"""Function to make sure all fields in the database are accounted for
in the csv file. It compares the header in the csv to the field names
in the object and returns None if they are all there. If it finds
any missing, or finds extra fields in the csv header, it adds them to
two lists and returns them in a dict.
"""

def missing_or_extra_fields(file, obj):

    # get the headers in the csv file
    with open(file, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        headers = reader.fieldnames

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
    if not missing_headers and not extra_headers:
        return None

    # There are missing or extra fields in the csv. Return those fields
    # in a dictionary so they can be added to a message.
    else:
        return {'missing_headers': missing_headers,
                'extra_headers': extra_headers, }


"""Function that returns true if a passed_in path is an empty
directory. Otherwise it returns false.
"""

def dir_not_empty(pathname):
    if (os.listdir(pathname)):
        return True
    else:
        return False


"""Moves files in a given path into the csvs directory, first deleting
any non-csvs and csvs with multiple copies.
"""

def move_files(request, pathname):
    basename = os.path.basename(pathname)

    # If the file isn't a csv, add a not a csv message and delete file.
    if not (basename.endswith('.csv')):

        if (os.path.dirname(pathname).endswith('documents')):
            shutil.move(pathname, 'media/documents/%s' % basename)
        elif (os.path.dirname(pathname).endswith('photos')):
            shutil.move(pathname, 'media/photos/%s' % basename)
        elif (os.path.isdir(pathname)):
            messages.add_message(request, messages.ERROR,
                                 ('Unable to read %s subfolder. Please add '
                                  'all csvfiles to main folder and re-upload.'
                                  % d2))
            shutil.rmtree(pathname)
        else:
            messages.add_message(request, messages.ERROR,
                                 ('%s is not a csv file. Please only upload '
                                  ' csv files.' % basename))
            os.remove(pathname)

    # else if the file being moved to csvs is already there, add a
    # conflicting copies message and delete both files
    elif (os.path.isfile('database/db_merging/csvs/%s' % basename)):
        messages.add_message(request, messages.ERROR,
                             ('Conflicting copies of %s uploaded. Please '
                              'choose one copy and re-upload.' % basename))
        os.remove(pathname)
        os.remove('database/db_merging/csvs/%s' % basename)
    else:
        shutil.move(pathname, 'database/db_merging/csvs/%s' % basename)


def replace_blank_uuids(file):
    temp_file = NamedTemporaryFile(delete=False)

    with open(file, 'rb') as csvfile, temp_file:
        reader = csv.DictReader(csvfile)

        writer = csv.DictWriter(temp_file, reader.fieldnames, delimiter=',')
        writer.writeheader()
        for row in reader:
            if (row['uuid'] == ''):
                row['uuid'] = str(uuid.uuid4())
            writer.writerow(row)

    shutil.move(temp_file.name, file)


"""This function opens the passed-in csv file and compares it to the
master database, saving the more recent row to the master database. If
the master database doesn't have a record of the object instance being
read in, it creates a new instance and saves it to the database. It
populates blank fields with the default value (usually None but for
some cases, such as uuids, default must be specified).
"""

def compare_csv(request, file, model_instance, fix, dependent_csvs_dict):

    # Open the csv file as a dictionary so it's searchable by field
    # name
    csvfile = open(file, 'rb')
    reader = csv.DictReader(csvfile)

    obj = get_object(model_instance)
    field_names = [f.name for f in obj._meta.fields]

    row_count = 0
    for row in reader:
        uuid_csv = row['uuid']
        try:
            # Based on the model_instance string, get the object that
            # might be edited from the master db.
            obj_inst = obj.objects.get(uuid=uuid_csv)

            if (fix is False):
                if (pytz.utc.localize(datetime.datetime.strptime(
                    row['last_saved'], "%Y-%m-%d %H:%M:%S")) <=
                        getattr(obj_inst, 'last_saved')):
                    messages.add_message(request, messages.ERROR,
                                         ('%s is already up to date in the '
                                          'database, no need to update'
                                          % model_instance))
                    # will be rewritten, just here so nothing throws an error
                    return None
        except:
            # Create new instance of model who has never been in the
            # database before
            if (uuid_csv != ''):
                if (model_instance == 'user'):
                    obj_inst = obj.objects.create_user(row['username'],
                                                       row['email'],
                                                       row['password'],
                                                       uuid=uuid_csv)
                else:
                    obj_inst = obj.objects.create(uuid=uuid_csv)
            else:
                messages.add_message(request, messages.ERROR,
                                     ('Hay un UUID que falta en el %s csv.' %
                                      model_instance))

                # will be rewritten, just here so nothing throws an error
                return None

        # If object exists, compare the object's last_saved field with
        # the corresponding object in the csv. If the csv object is
        # newer, edit the master db.
        if (dependent_csvs_dict):
            for key, value in dependent_csvs_dict.iteritems():

                # if there is a dependent object for this row, get the
                # dependent object and save it applies only to user,
                # which doesn't necessarily have a dependent object all
                # other objects had the dependent object column checked
                # already
                if (row[key] != ''):
                    dependent_csvfile = open(value, 'rb')
                    dependent_reader = csv.DictReader(dependent_csvfile)

                    # get the id of the dependent object from row
                    dependent_id = row[key]

                    # get dependent object's uuid by searching the dict the
                    # row matching the dependent id
                    dependent_csvfile.seek(0)  # go to top of csv
                    dependent_uuid = ''
                    for drow in dependent_reader:
                        if (drow['id'] == dependent_id):
                            dependent_uuid = drow['uuid']
                            break
                        # if the dependent id isn't in the object,
                        # return with a message
                    if (dependent_uuid == ''):
                        messages.add_message(request, messages.ERROR,
                                             ('There is no %s with the id '
                                              '%s in %s.csv'
                                              % (key, dependent_id,
                                                 model_instance)))
                        return False
                    dependent_object = get_object(key)

                    # set the id obj_inst's dependent objects
                    setattr(obj_inst, key, dependent_object.objects.get(
                            uuid=dependent_uuid))
                    dependent_csvfile.close()  # close dependent's csv

        for name in field_names:

            # if the current cell in the csv is empty and the
            # corresponding field has a default, use the default value
            if (row[name] == ''
                    and obj_inst._meta.get_field(name).get_default()):
                    value = obj_inst._meta.get_field(name).get_default()

            # if there's no default value or the current cell is not
            # empty, use the current cell
            elif (row[name] != ''):
                value = row[name]
            else:
                continue

            # IntegerField: convert string to integer and save to
            # object
            if (obj_inst._meta.get_field(name).get_internal_type()
                    == 'IntegerField'):
                    setattr(obj_inst, name, int(value))

            # FloatField: convert string to float and save to object
            elif (obj_inst._meta.get_field(name).get_internal_type()
                    == 'FloatField'):
                setattr(obj_inst, name, float(value))

            # DateTimeField: convert string to a utc-aware datetime
            # object and save it to object
            elif (obj_inst._meta.get_field(name).get_internal_type()
                    == 'DateTimeField'):
                if (value != ''):
                    if (type(value).__name__ == 'datetime'):
                        setattr(obj_inst, name, value)
                    else:
                        try:
                            datetime_obj = dateutil.parser.parse(value,
                                                                 dayfirst=True
                                                                 )
                            setattr(obj_inst, name,
                                    pytz.utc.localize(datetime_obj))
                        except:
                            messages.add_message(request, messages.ERROR,
                                                 ('The %s datetime for the %s'
                                                  ' with the id %s cannot be '
                                                  'parsed.' %
                                                  (name, model_instance,
                                                   row['id'])))
                            break

                else:
                    setattr(obj_inst, name, None)

            # DateField: convert string to datetime object, conert that
            #  to a date object and and save it to object
            elif (obj_inst._meta.get_field(name).get_internal_type()
                    == 'DateField'):
                if (value != ''):
                    if (type(value).__name__ == 'date'):
                        setattr(obj_inst, name, value)
                    else:
                        try:
                            datetime_obj = dateutil.parser.parse(value,
                                                                 dayfirst=True
                                                                 )
                            date_obj = datetime_obj.date()
                            setattr(obj_inst, name, date_obj)
                        except:
                            messages.add_message(request, messages.ERROR,
                                                 ('The %s date for the %s '
                                                  'with the id %s cannot be '
                                                  'parsed.' %
                                                  (name, model_instance,
                                                   row['id'])))
                            break

                else:
                    setattr(obj_inst, name, None)

            # BooleanField: check if the csv has it saved as true or false (1
            # or 0) and then set the object field with as a boolean
            elif (obj_inst._meta.get_field(name).get_internal_type()
                    == 'BooleanField'):

                # For user permissions, which are saved as booleans in the
                # user model
                content_type = ContentType.objects.get_for_model(User)
                if (name == 'add_users'):
                    permission = Permission.objects.get(
                        codename='add_users',
                        content_type=content_type
                    )
                    if (value == '1'):
                        obj_inst.user_permissions.add(permission)
                    else:
                        obj_inst.user_permissions.remove(permission)
                if (name == 'delete_info'):
                    permission = Permission.objects.get(
                        codename='delete_info',
                        content_type=content_type
                    )
                    if (value == '1'):
                        obj_inst.user_permissions.add(permission)
                    else:
                        obj_inst.user_permissions.remove(permission)

                if (name == 'add_edit_forms'):
                    permission = Permission.objects.get(
                        codename='add_edit_forms',
                        content_type=content_type
                    )
                    if (value == '1'):
                        obj_inst.user_permissions.add(permission)
                    else:
                        obj_inst.user_permissions.remove(permission)
                if (name == 'not_restricted_to_home'):
                    permission = Permission.objects.get(
                        codename='not_restricted_to_home',
                        content_type=content_type
                    )
                    if (value == '1'):
                        obj_inst.user_permissions.add(permission)
                    else:
                        obj_inst.user_permissions.remove(permission)
                if (name == 'view'):
                    permission = Permission.objects.get(
                        codename='view',
                        content_type=content_type
                    )
                    if (value == '1'):
                        obj_inst.user_permissions.add(permission)
                    else:
                        obj_inst.user_permissions.remove(permission)

                if (value == '1'):
                    setattr(obj_inst, name, True)
                else:
                    setattr(obj_inst, name, False)

            # FileFieldField: just set the object, no conversion
            # required.
            elif (obj_inst._meta.get_field(name).get_internal_type()
                    == 'FileField'):
                setattr(obj_inst, name, value)

            # CharField: just set the object, no conversion required.
            elif (obj_inst._meta.get_field(name).get_internal_type()
                    == 'CharField'):
                setattr(obj_inst, name, value)

            # TextField: just set the object, no conversion required.
            elif (obj_inst._meta.get_field(name).get_internal_type() ==
                    'TextField'):
                    setattr(obj_inst, name, value)

            # If none of those are correct, print them out so I can see
            # what I'm missing
            else:
                pass
                # messages.add_message(request, messages.ERROR,
                #     ('Unknown field type: %s' %
                #      obj_inst._meta.get_field(name).get_internal_type()))
                # return False
                # print "Unknown field type: %s" % obj_inst._meta.get_field
                # (name).get_internal_type()

        # Save the object to the database
        obj_inst.save()
        messages.add_message(request, messages.SUCCESS, 'Database Imported!')
        row_count += 1
    csvfile.close()


"""This function exports the database using the import-export django
app, and imports CSVs to be read into the database. During import, it
checks for errors and deletes files that fail with an error message.
CSVs that pass are sent to compare_csvs to be compared to the master database.
"""

@login_required
@user_passes_test(is_superuser_check)
def import_export_db(request):
    if (request.POST):

#######################################################################
# DOWNLOAD DATABASE
#######################################################################

        # If request was to export the database,
        # make csv files of each table and gzip them
        if ('submit_export' in request.POST):

            # Making the csv files using django-import-export app
            # saving them to the csvs directory
            # LOOK INTO TURNING THIS INTO A LOOP
            tables = []  # logs the csv names to be zipped

            child = ChildResource().export()
            with open('csvs/child.csv', 'w') as child_csv:
                child_csv.write(child.csv)
            tables.append('csvs/child.csv')

            dental_exam = DentalExamResource().export()
            with open('csvs/dental_exam.csv', 'w') as dental_exam_csv:
                dental_exam_csv.write(dental_exam.csv)
            tables.append('csvs/dental_exam.csv')

            discharge_plan = DischargePlanResource().export()
            with open('csvs/discharge_plan.csv', 'w') as discharge_plan_csv:
                discharge_plan_csv.write(discharge_plan.csv)
            tables.append('csvs/discharge_plan.csv')

            documents = DocumentsResource().export()
            with open('csvs/documents.csv', 'w') as documents_csv:
                documents_csv.write(documents.csv)
            tables.append('csvs/documents.csv')

            disease_history = DiseaseHistoryResource().export()
            with open('csvs/disease_history.csv', 'w') as disease_history_csv:
                disease_history_csv.write(disease_history.csv)
            tables.append('csvs/disease_history.csv')

            medical_exam_part1 = MedicalExamPart1Resource().export()
            with (open('csvs/medical_exam_part1.csv', 'w')
                    as medical_exam_part1_csv):
                medical_exam_part1_csv.write(medical_exam_part1.csv)
            tables.append('csvs/medical_exam_part1.csv')

            medical_exam_part2 = MedicalExamPart2Resource().export()
            with (open('csvs/medical_exam_part2.csv', 'w')
                    as medical_exam_part2_csv):
                medical_exam_part2_csv.write(medical_exam_part2.csv)
            tables.append('csvs/medical_exam_part2.csv')

            operation_history = OperationHistoryResource().export()
            with (open('csvs/operation_history.csv', 'w') as
                    operation_history_csv):
                operation_history_csv.write(operation_history.csv)
            tables.append('csvs/operation_history.csv')

            photograph = PhotographResource().export()
            with open('csvs/photograph.csv', 'w') as photograph_csv:
                photograph_csv.write(photograph.csv)
            tables.append('csvs/photograph.csv')

            psychological_exam = PsychologicalExamResource().export()
            with (open('csvs/psychological_exam.csv', 'w') as
                    psychological_exam_csv):
                psychological_exam_csv.write(psychological_exam.csv)
            tables.append('csvs/psychological_exam.csv')

            residence = ResidenceResource().export()
            with open('csvs/residence.csv', 'w') as residence_csv:
                residence_csv.write(residence.csv)
            tables.append('csvs/residence.csv')

            social_exam = SocialExamResource().export()
            with open('csvs/social_exam.csv', 'w') as social_exam_csv:
                social_exam_csv.write(social_exam.csv)
            tables.append('csvs/social_exam.csv')

            # auth
            user = UserResource().export()
            with open('csvs/user.csv', 'w') as user_csv:
                user_csv.write(user.csv)
            tables.append('csvs/user.csv')

            # Before zipping file, remove any previously zipped
            # database file.
            if (os.path.isfile('media/hbi-db-export.zip')):
                os.remove('media/hbi-db-export.zip')

            # Zip the csvs together -- currently not compressed because
            # it's not a fan, will try again soon.
            zippy = zipfile.ZipFile('media/hbi-db-export.zip', 'a')
            for item in tables:
                zippy.write(item)

            path = "media/documents/*"
            for p in glob.glob(path):
                zippy.write(p)

            path = "media/photos/*"
            for p in glob.glob(path):
                zippy.write(p)

            # Since serving the zipped file as an attachment corrupted
            # the file (most likely because django isn't equipped to
            # serve larger files), render it in the import_export
            # template for download.
            form = ImportDBForm()

            context = {
                'zip_file': True,
                'page': 'import_export',
                'form': form.as_ul,
            }
            return render(request, 'tracker/import_export.html', context)

#######################################################################
# UPLOAD DATABASE
#######################################################################

        # If request is to import the database, get the posted file
        elif ('submit_import' in request.POST):
            form = ImportDBForm(request.POST, request.FILES)

            # If the form posted a file, get it and extract it.
            if form.is_valid():
                upload_name,
                upload_extension = request.FILES['upload'].name.split('.')

                # delete previously uploaded files, if any
                if os.path.isdir('database/db_merging'):
                    shutil.rmtree('database/db_merging')
                    os.mkdir('database/db_merging')

                # if uploaded file is a zip, extract files
                if (upload_extension == 'zip'):
                    with zipfile.ZipFile(request.FILES['upload']) as zf:
                        zf.extractall('database/db_merging')

                # if uploaded file is a csv, read it into a file in the
                # csvs directory in chunks
                elif (upload_extension == 'csv'):
                    os.mkdir('database/db_merging/csvs')
                    with open('database/db_merging/csvs/%s.csv' %
                              upload_name, 'wb+') as destination:
                        for chunk in request.FILES['upload'].chunks():
                            destination.write(chunk)

                # If file is not zipped or not csv, return with error message
                else:
                    messages.add_message(request, messages.ERROR,
                                         ('Incorrect File Type: .%s files are'
                                          ' not compatible with our database.'
                                          % upload_extension))
                    return HttpResponseRedirect(
                        reverse('tracker:import_export'))

                # create glob path to loop through all dirs in
                # db_merging
                path = 'database/db_merging/*'
                directories = []
                # create a list of all directories in db_merging
                for pathname in glob.glob(path):
                    if (os.path.isdir(pathname)):
                        # if directory is empty, remove it
                        try:
                            os.rmdir(pathname)
                        # if it's not, add the name to the list
                        except:
                            directories.append(os.path.basename(pathname))

                # After deleting all the empty directories, check that
                # db_merging isn't empty
                if (not dir_not_empty('database/db_merging')):
                    messages.add_message(request, messages.ERROR,
                                         'There is nothing left to return!')
                    return HttpResponseRedirect(
                        reverse('tracker:import_export'))

                # if there are directories, loop through them and move
                # all files to csvs directory
                if (directories):
                    # create the csvs directory that all files will be
                    # read into if it doesn't already exist
                    if 'csvs' not in directories:
                        os.mkdir('database/db_merging/csvs')
                    # if it already exists, great, remove it from the
                    # directories list so it doesn't get looped over.
                    else:
                        directories.remove('csvs')

                    # If there are stil directories without csvs in the
                    # list, loop through directories and move all files
                    # to csvs directory, deleting copies and non-csvs
                    if (directories):
                        for d in directories:
                            # loop through files and make sure they aren't
                            # directories before evaluating and moving
                            for pathname in glob.glob(
                                    'database/db_merging/%s/*' % d):
                                if (os.path.exists(pathname)
                                        and not os.path.isdir(pathname)):
                                    move_files(request, pathname)

                                # If there's a directory within a directory,
                                # return a too many levels error and delete
                                # directory
                                else:
                                    d2 = os.path.basename(pathname)
                                    for p in glob.glob(
                                        'database/db_merging/%s/%s/*' %
                                            (d, d2)):
                                        if (os.path.exists(p)
                                                and not os.path.isdir(p)):
                                            move_files(request, p)

                                        else:
                                            messages.add_message(
                                                request,
                                                messages.ERROR,
                                                ('Unable to read %s subfolder'
                                                 '. Please add all csvfiles '
                                                 'to main folder and '
                                                 're-upload.' % d2))
                                            if (os.path.exists(p)):
                                                shutil.rmtree(pathname)

                            # after moving all readable files to csvs
                            # directory, delete empty directory
                            shutil.rmtree('database/db_merging/%s' % d)

                # if there are no directories, create the csvs
                # directory
                else:
                    os.mkdir('database/db_merging/csvs')

                # move all files in db_merging to csvs directory,
                # deleting copies and non-csvs
                for pathname in glob.glob(path):
                    if (not os.path.isdir(pathname)):
                        move_files(request, pathname)

                # glob path to read all csvs in the csvs dir
                path = 'database/db_merging/csvs/*.csv'

                # Loop through the csvs directory five times:
                # First, check that all the csvs and their dependencies
                # correspond to a model.
                # Second, check that all fields are present in each
                # csv.
                # Third, make sure all files are populated. This won't
                # break anything, but might be useful information for
                # the user.
                # Fourth, indentify and delete all files with repeated
                # identifiers
                # Fifth, identify and locate dependent objects and
                # their csvs, check that the ids and uuids in both the
                # csv and the dependent csvs are unique, and then check
                # that all csvs are there again.
                for i in range(5):

                    # before each iteration, check that file isn't empty
                    if (dir_not_empty('database/db_merging/csvs')):
                        for pname in glob.glob(path):

                            # get the table name by parsing the path name
                            bname = os.path.basename(pname)
                            tname, extension = bname.split('.')

                            # FIRST LOOP: Identify and Remove CSVS and
                            # Their Dependencies that Don't Match
                            # Database Headers
                            if (i == 0):

                                # Check that each csv corresponds to a
                                # table in the database. If a table
                                # that does not exist appears, render
                                # the import_export template with an
                                # error message saying which csv
                                # doesn't correspond.
                                if (not get_object(tname)):
                                    messages.add_message(
                                        request,
                                        messages.ERROR,
                                        ('%s does not correspond to any table'
                                         ' in the database. Please re-upload '
                                         'with the correct file name.'
                                         % bname))
                                    os.remove(pname)  # remove defective csv

                                # # if the main csv corresponds to a
                                # model, check for dependents and make
                                # sure those correspond to a model.
                                if (is_dependent(tname)):
                                    dependents_list = get_dependents_list(
                                        tname)
                                    for dependent in dependents_list:
                                        if (not get_object(dependent)):
                                            messages.add_message(
                                                request,
                                                messages.ERROR,
                                                ('%s is dependent on the %s '
                                                 'model, which does not exist'
                                                 ' in our database. Please '
                                                 're-upload with the correct '
                                                 'dependencies.' %
                                                 (bname, dependent)))
                                            # remove defective csv
                                            os.remove(pname)

                            # SECOND LOOP: Identify and Remove CSVs
                            # with Missing or Extra Fields
                            elif (i == 1):
                                model_obj = get_object(tname)

                                # Check if all fields exist in the csv.
                                # If it comes up
                                mef_check = missing_or_extra_fields(
                                    pname,
                                    model_obj)
                                if (mef_check is not None):

                                    # If there are missing headers, add
                                    # a error message to be displayed
                                    # on render of all the fields
                                    # missing in that csv file.
                                    if (mef_check['missing_headers']):
                                        missing_headers = ', '.join(
                                            mef_check['missing_headers'])
                                        messages.add_message(
                                            request,
                                            messages.ERROR,
                                            ('The following fields are '
                                             'missing from %s: %s. Please add'
                                             ' those fields and re-upload' %
                                             (bname, missing_headers)
                                             ))

                                    # If there are extra headers, add a
                                    # error message to be displayed on
                                    # render of all the extra fields in
                                    # that csv file.
                                    if (mef_check['extra_headers']):
                                        extra_headers = ', '.join(
                                            mef_check['extra_headers'])
                                        messages.add_message(
                                            request,
                                            messages.ERROR,
                                            ('The following fields from %s do'
                                             ' not exist in the database: %s.'
                                             ' Please either rename or remove'
                                             ' these fields before '
                                             're-uploading.' %
                                             (bname, extra_headers)
                                             ))
                                    os.remove(pname)  # remove broken csv

                            # THIRD LOOP: Identify and Remove Empty
                            # CSVs (except header)
                            elif (i == 2):

                                if (file_empty(pname)):
                                    messages.add_message(
                                        request,
                                        messages.ERROR,
                                        ('%s is empty. If that is correct,'
                                         ' please ignore this message.' %
                                         bname))
                                    os.remove(pname)  # remove empty csv

                            # FOURTH LOOP: Look for repeating ids and
                            # uuids in csv
                            elif (i == 3):

                                empty_identifiers = ids_not_empty(
                                    pname, tname)
                                if (empty_identifiers is not None):
                                    empty_ids_str = (', ').join(
                                        empty_identifiers)
                                    messages.add_message(
                                        request,
                                        messages.ERROR,
                                        ('The following required fields have'
                                         ' blank values in %s: %s. Please '
                                         'resolve these repetitions and '
                                         're-upload.' %
                                         (bname, empty_ids_str)))
                                    os.remove(pname)  # remove csv with
                                                      # repeating ids/uuids

                                else:
                                    repeating_identifiers = ids_uuids_unique(
                                        pname)
                                    if (repeating_identifiers is not None):
                                        repeating_id_str = (', ').join(
                                            repeating_identifiers)
                                        messages.add_message(
                                            request,
                                            messages.ERROR,
                                            ('The following fields have '
                                             'repeating values that should be'
                                             ' unique in %s: %s. Please '
                                             'resolve these repetitions and '
                                             're-upload.' %
                                             (bname, repeating_id_str)))
                                        # remove csv with repeating
                                        #ids/uuids
                                        os.remove(pname)

                            # FIFTH LOOP: Indentify dependent objects
                            # and locate their csvs
                            elif (i == 4):

                                # If the current object is dependent on
                                # other objects, search the csvs
                                # directory for csvs that match the
                                # dependent objects and add those csvs
                                # to a dependents_csvs dict
                                if (is_dependent(tname)):

                                    dependents_csvs = get_dependents_csvs(
                                        tname, path)
                                    dependents_list = get_dependents_list(
                                        tname)

                                    # If there not the same number of
                                    # dependents in the objects dict
                                    # and the csvs dict, create list of
                                    # missing csvs, add a message, and
                                    # remove the csv with dependents
                                    # that don't exist.
                                    if (len(dependents_list)
                                            != len(dependents_csvs)):
                                        missing_dependents_list = []
                                        for dependent in dependents_list:
                                            if (dependent not in
                                                    dependents_csvs):
                                                # stitch list together to add
                                                # to message
                                                (missing_dependents_list.
                                                    append(dependent))

                                        #first, check that there are no
                                        # missing dependents that the main
                                        # csv might need
                                        if (missing_dependents_list):
                                            missing_dependents_str = (
                                                (', ').join(
                                                    missing_dependents_list))
                                            messages.add_message(
                                                request,
                                                messages.ERROR,
                                                ('%s needs the following csv '
                                                 'files to upload correctly'
                                                 ': %s. Please add those '
                                                 'files to your zip and '
                                                 're-upload.'
                                                 % (bname,
                                                    missing_dependents_str)))
                                            os.remove(pname)  # remove empty
                                                              # csv

                    else:
                        messages.add_message(
                            request,
                            messages.ERROR,
                            "There's nothing left to return!")
                        return HttpResponseRedirect(reverse(
                            'tracker:import_export'))

                if dir_not_empty('database/db_merging/csvs'):

                    # Must be on own loop with a specific list to loop over
                    # To make sure the dependent objects are read in first
                    read_order = ['residence', 'child', 'dental_exam',
                                  'discharge_plan', 'disease_history',
                                  'documents', 'medical_exam_part1',
                                  'medical_exam_part2', 'operation_history',
                                  'psychological_exam', 'social_exam',
                                  'documents', 'photograph', 'user']

                    for item in read_order:
                        for pname in glob.glob(path):

                            # get the table name by parsing the path name
                            bname = os.path.basename(pname)
                            tname, extension = bname.split('.')
                            if (tname == item):
                                replace_blank_uuids(pname)
                                if (is_dependent(tname)):
                                    dependents_csvs = get_dependents_csvs(
                                        tname, path)
                                    compare_csv(
                                        request,
                                        pname,
                                        tname,
                                        request.FILES['upload'],
                                        dependents_csvs)

                                # If no dependents, just pass in the csv and
                                # the table name
                                else:
                                    compare_csv(
                                        request,
                                        pname,
                                        tname,
                                        request.FILES['upload'],
                                        None)
                else:
                    messages.add_message(request, messages.ERROR,
                                         "There's nothing left to return!")
                    return HttpResponseRedirect(
                        reverse('tracker:import_export'))

                return HttpResponseRedirect(reverse('tracker:import_export'))

            else:
                messages.add_message(request, messages.SUCCESS,
                                     'Please add a file to be imported!')
                return HttpResponseRedirect(reverse('tracker:import_export'))

    else:
        form = ImportDBForm()

        # Render the help.html template
        context = {
            'page': 'import_export',
            'form': form.as_ul,
        }
        return render(request, 'tracker/import_export.html', context)

#######################################################################
#######################################################################
#######################################################################

# app tables


class ChildResource(resources.ModelResource):

    class Meta:
        model = Child
        widgets = {
            'intake_date': {'format': '%d/%m/%Y'},
            'discharge_date': {'format': '%d/%m/%Y'},
            'birthdate': {'format': '%d/%m/%Y'},
        }


class DentalExamResource(resources.ModelResource):

    class Meta:
        model = DentalExam
        widgets = {
            'date': {'format': '%d/%m/%Y'},
        }


class DischargePlanResource(resources.ModelResource):

    class Meta:
        model = DischargePlan
        widgets = {
            'date': {'format': '%d/%m/%Y'},
        }


class DocumentsResource(resources.ModelResource):

    class Meta:
        model = Documents
        widgets = {
            'date': {'format': '%d/%m/%Y'},
        }


class DiseaseHistoryResource(resources.ModelResource):

    class Meta:
        model = DiseaseHistory
        widgets = {
            'date': {'format': '%d/%m/%Y'},
        }


class MedicalExamPart1Resource(resources.ModelResource):

    class Meta:
        model = MedicalExamPart1
        widgets = {
            'date': {'format': '%d/%m/%Y'},
            'bcg_vaccine_date': {'format': '%d/%m/%Y'},
            'polio_vaccine_date': {'format': '%d/%m/%Y'},
            'dpt_vaccine_date': {'format': '%d/%m/%Y'},
            'hepatitis_b_vaccine_date': {'format': '%d/%m/%Y'},
            'flu_vaccine_date': {'format': '%d/%m/%Y'},
            'yellow_fever_vaccine_date': {'format': '%d/%m/%Y'},
            'spr_vaccine_date': {'format': '%d/%m/%Y'},
            'hpv_vaccine_date': {'format': '%d/%m/%Y'},
            'pneumococcal_vaccine_date': {'format': '%d/%m/%Y'},
        }


class MedicalExamPart2Resource(resources.ModelResource):

    class Meta:
        model = MedicalExamPart2
        widgets = {
            'date': {'format': '%d/%m/%Y'},
        }


class OperationHistoryResource(resources.ModelResource):

    class Meta:
        model = OperationHistory
        widgets = {
            'date': {'format': '%d/%m/%Y'},
        }


class PhotographResource(resources.ModelResource):

    class Meta:
        model = Photograph
        widgets = {
            'date': {'format': '%d/%m/%Y'},
        }


class PsychologicalExamResource(resources.ModelResource):

    class Meta:
        model = PsychologicalExam
        widgets = {
            'date': {'format': '%d/%m/%Y'},
        }


class ResidenceResource(resources.ModelResource):

    class Meta:
        model = Residence
        widgets = {
            'date': {'format': '%d/%m/%Y'},
        }


class SocialExamResource(resources.ModelResource):

    class Meta:
        model = SocialExam
        widgets = {
            'date': {'format': '%d/%m/%Y'},
        }

# auth tables


class UserResource(resources.ModelResource):

    class Meta:
        model = User
        exclude = ('groups', 'user_permissions',)
        widgets = {
            'date': {'format': '%d/%m/%Y'},
        }
