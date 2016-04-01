from django.contrib import admin

from import_export import resources

from tracker.models import Child
from tracker.models import DentalExam
from tracker.models import Documents
from tracker.models import MedicalExamPart1
from tracker.models import MedicalExamPart2
from tracker.models import OperationHistory
from tracker.models import Photograph
from tracker.models import Profile
from tracker.models import PsychologicalExam
from tracker.models import Residence
from tracker.models import Signature
from tracker.models import SocialExam

class ChildResource(resources.ModelResource):

    class Meta:
        model = Child


# def export_child_csv(modeladmin, request, queryset):
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename=child.csv'
#     writer = csv.writer(response, csv.excel)
#     response.write(u'\ufeff'.encode('utf8')) # BOM

#     writer.writerow([
#         smart_str(u"id"),
#         smart_str(u"uuid"),
#         smart_str(u"residence_id"),
#         smart_str(u"first_name"),
#         smart_str(u"last_name"),
#         smart_str(u"nickname"),
#         smart_str(u"birthdate"),
#         smart_str(u"gender"),
#         smart_str(u"birthplace"),
#         smart_str(u"intake_date"),
#         smart_str(u"discharge_date"),
#         smart_str(u"photo"),
#         smart_str(u"priority"),
#         smart_str(u"is_active"),
#         smart_str(u"last_saved"),
#     ])
#     for obj in queryset:
#         writer.writerow([
#             smart_str(obj.pk),
#             smart_str(obj.uuid),
#             smart_str(obj.residence_id),
#             smart_str(obj.first_name),
#             smart_str(obj.last_name),
#             smart_str(obj.nickname),
#             smart_str(obj.birthdate),
#             smart_str(obj.gender),
#             smart_str(obj.birthplace),
#             smart_str(obj.intake_date),
#             smart_str(obj.discharge_date),
#             smart_str(obj.photo),
#             smart_str(obj.priority),
#             smart_str(obj.is_active),
#             smart_str(obj.last_saved),
#         ])
#     return response
# export_child_csv.short_description = u"Export Child CSV"


# class ExportChildAdmin(admin.ModelAdmin):
#     actions = [export_child_csv]


# def export_residence_csv(modeladmin, request, queryset):
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename=residence.csv'
#     writer = csv.writer(response, csv.excel)
#     response.write(u'\ufeff'.encode('utf8')) # BOM

#     writer.writerow([
#         smart_str(u"id"),
#         smart_str(u"uuid"),
#         smart_str(u"residence_name"),
#         smart_str(u"administrator"),
#         smart_str(u"location"),
#         smart_str(u"photo"),
#         smart_str(u"last_saved"),
#     ])
#     for obj in queryset:
#         writer.writerow([
#             smart_str(obj.pk),
#             smart_str(obj.uuid),
#             smart_str(obj.residence_name),
#             smart_str(obj.administrator),
#             smart_str(obj.location),
#             smart_str(obj.photo),
#             smart_str(obj.last_saved),
#         ])
#     return response
# export_residence_csv.short_description = u"Export Residence CSV"


# class ExportResidenceAdmin(admin.ModelAdmin):
#     actions = [export_residence_csv]


admin.site.register(Child)
admin.site.register(Residence)
