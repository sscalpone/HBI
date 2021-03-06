# coding=utf-8

""" Initialize models, so all models are imported to the database table.
"""
from Child import Child, ChildForm
from DentalExam import DentalExam, DentalExamForm
from DischargePlan import DischargePlan, DischargePlanForm
from Documents import Documents, DocumentsForm
from DiseaseHistory import DiseaseHistory, DiseaseHistoryForm
from EducationPlan import EducationPlan, EducationPlanForm
from ImportDB import ImportDBForm
from MedicalExamPart1 import MedicalExamPart1, MedicalExamPart1Form
from MedicalExamPart2 import MedicalExamPart2, MedicalExamPart2Form
from OperationHistory import OperationHistoryForm, OperationHistory
from PsychologicalExam import PsychologicalExam, PsychologicalExamForm
from Photograph import Photograph, PhotographForm
from Residence import Residence, ResidenceForm
from Signature import SignatureForm
from SocialExam import SocialExam, SocialExamForm
from Profile import ProfileForm
from Profile import EditNameForm, EditPasswordForm, EditIsStaffForm
from Profile import EditIsActiveForm, EditAddUsersForm, EditEmailForm
from Profile import EditDeleteInfoForm, EditAddEditFormsForm
from Profile import EditRestrictToHomeForm
from HelpEmail import HelpEmailForm
from CustomUser import CustomUser
