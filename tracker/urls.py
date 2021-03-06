from django.conf.urls import patterns, url

from tracker.views import main
from tracker.views import residence
from tracker.views import child
from tracker.views import documents
from tracker.views import dental_exam
from tracker.views import discharge_plan
from tracker.views import disease_history
from tracker.views import education_plan
from tracker.views import medical_exam_part1
from tracker.views import medical_exam_part2
from tracker.views import psychological_exam
from tracker.views import operation_history
from tracker.views import photograph
from tracker.views import social_exam
from tracker.views import exam_views
from tracker.views import profile
from tracker.views import help_email
from tracker.views import import_export_db

urlpatterns = patterns('',
    # ex: /tracker/
    url(r'^$', main.index, name='index'),
    url(r'^login/$', main.login, name='login'),
    url(r'^logout/$', main.logout, name='logout'),

    url(r'^user/$', profile.index, name='profiles'),
    url(r'^users/new/$', profile.new, name='add_profile'),
    url(r'^user/(?P<profile_id>\d+)', profile.view, name='profile'),

    url(r'^help/$', help_email.send_email, name='help'),

    url(r'^import_export/$', import_export_db.import_export_db, name='import_export'),

    url(r'^residences/$', residence.index, name='residences'),
    url(r'^residences/new/$', residence.new, name='add_residence'),
    url(r'^residence/(?P<residence_id>\d+)', residence.view,
        name='residence'),
    url(r'^residence/edit/(?P<residence_id>\d+)', residence.edit,
        name='edit_residence'),

    url(r'^child/new/(?P<residence_id>\d+)', child.new, name='add_child'),
    url(r'^child/edit/(?P<child_id>\d+)', child.edit, name='edit_child'),
    url(r'^child/(?P<child_id>\d+)', exam_views.index, name='child'),

    url(r'^documents/(?P<child_id>\d+)/(?P<exam_id>\d+)', documents.view, name='document'),
    url(r'^documents/edit/(?P<child_id>\d+)/(?P<exam_id>\d+)',
        documents.edit, name='edit_document'),
    url(r'^documents/new/(?P<child_id>\d+)', documents.new, name='new_document'),

    url(r'^dental_exam/(?P<child_id>\d+)/(?P<exam_id>\d+)', dental_exam.view,
        name='dental_exam'),
    url(r'^dental_exam/edit/(?P<child_id>\d+)/(?P<exam_id>\d+)',
        dental_exam.edit, name='edit_dental_exam'),
    url(r'^dental_exam/new/(?P<child_id>\d+)', dental_exam.new,
        name='new_dental_exam'),

    url(r'^discharge_plan/(?P<child_id>\d+)/(?P<exam_id>\d+)',
        discharge_plan.view, name='discharge_plan'),
    url(r'^discharge_plan/edit/(?P<child_id>\d+)/(?P<exam_id>\d+)',
        discharge_plan.edit, name='edit_discharge_plan'),
    url(r'^discharge_plan/new/(?P<child_id>\d+)', discharge_plan.new,
        name='new_discharge_plan'),

    url(r'^disease_history/(?P<child_id>\d+)/(?P<exam_id>\d+)',
        disease_history.view, name='disease_history'),
    url(r'^disease_history/edit/(?P<child_id>\d+)/(?P<exam_id>\d+)',
        disease_history.edit, name='edit_disease_history'),
    url(r'^disease_history/new/(?P<child_id>\d+)', disease_history.new,
        name='new_disease_history'),

    url(r'^education_plan/(?P<child_id>\d+)/(?P<exam_id>\d+)',
        education_plan.view, name='education_plan'),
    url(r'^education_plan/edit/(?P<child_id>\d+)/(?P<exam_id>\d+)',
        education_plan.edit, name='edit_education_plan'),
    url(r'^education_plan/new/(?P<child_id>\d+)', education_plan.new,
        name='new_education_plan'),

    url(r'^medical_exam_part1/(?P<child_id>\d+)/(?P<exam_id>\d+)',
        medical_exam_part1.view, name='medical_exam_part1'),
    url(r'^medical_exam_part1/edit/(?P<child_id>\d+)/(?P<exam_id>\d+)',
        medical_exam_part1.edit, name='edit_medical_exam_part1'),
    url(r'^medical_exam_part1/new/(?P<child_id>\d+)', medical_exam_part1.new,
        name='new_medical_exam_part1'),

    url(r'^medical_exam_part2/new/(?P<child_id>\d+)/(?P<exam_id>\d+)',
        medical_exam_part2.view, name='medical_exam_part2'),
    url(r'^medical_exam_part2/edit/(?P<child_id>\d+)/(?P<exam_id>\d+)',
        medical_exam_part2.edit, name='edit_medical_exam_part2'),
    url(r'^medical_exam_part2/new/(?P<child_id>\d+)', medical_exam_part2.new,
        name='new_medical_exam_part2'),

    url(r'^graph/(?P<child_id>\d+)/growth.png',
        medical_exam_part1.growth_png, name='growth_png'),
    url(r'^graph/(?P<child_id>\d+)', medical_exam_part1.graph_growth,
        name='growth_graph'),

    url(r'^operation_history/(?P<child_id>\d+)/(?P<exam_id>\d+)',
        operation_history.view, name='operation_history'),
    url(r'^operation_history/edit/(?P<child_id>\d+)/(?P<exam_id>\d+)',
        operation_history.edit, name='edit_operation_history'),
    url(r'^operation_history/new/(?P<child_id>\d+)', operation_history.new,
        name='new_operation_history'),

    url(r'^psychological_exam/(?P<child_id>\d+)/(?P<exam_id>\d+)',
        psychological_exam.view, name='psychological_exam'),
    url(r'^psychological_exam/edit/(?P<child_id>\d+)/(?P<exam_id>\d+)',
        psychological_exam.edit, name='edit_psychological_exam'),
    url(r'^psychological_exam/new/(?P<child_id>\d+)', psychological_exam.new,
        name='new_psychological_exam'),

    url(r'^photo/(?P<child_id>\d+)/(?P<exam_id>\d+)', photograph.view,
        name='photo'),
    url(r'^photo/edit/(?P<child_id>\d+)/(?P<exam_id>\d+)', photograph.edit,
        name='edit_photo'),
    url(r'^photo/new/(?P<child_id>\d+)', photograph.new, name='new_photo'),
    url(r'^photo/delete/(?P<child_id>\d+)/(?P<exam_id>\d+)',
        photograph.delete, name='delete_photo'),

    url(r'^social_exam/(?P<child_id>\d+)/(?P<exam_id>\d+)', social_exam.view,
        name='social_exam'),
    url(r'^social_exam/edit/(?P<child_id>\d+)/(?P<exam_id>\d+)',
        social_exam.edit, name='edit_social_exam'),
    url(r'^social_exam/new/(?P<child_id>\d+)', social_exam.new,
        name='new_social_exam'),
)
