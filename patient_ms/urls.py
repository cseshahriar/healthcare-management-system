from django.urls import path
from patient_ms.views import (
    PatientInfoUpdate,
    DoctorAppointmentView,
    doctor_filter,
    DoctorPrescriptionView,
    ViewAllSavedRecord,
    PatientProfile,
    ForgetAppointmentSerialView,
    AppointmentConfirmationLetterView,
    AppointmentCopyPDFView,
    ViewAllDownloadRecord,
    PMSViewAllSavedRecord
)

app_name = 'patient_ms'
urlpatterns = [
    path(
        'profile/',
        PatientProfile.as_view(), name='patient_profile'
    ),
    path(
        '<int:pk>/update/',
        PatientInfoUpdate.as_view(), name='patient_info_update'
    ),
    path(
        'calender/appointment/',
        DoctorAppointmentView.as_view(), name='appointment'
    ),
    path(
        'appointment/<int:pk>/confirmation',
        AppointmentConfirmationLetterView.as_view(),
        name='appointment_confirmation'
    ),
    path(
        'appointment/<int:pk>/download',
        AppointmentCopyPDFView.as_view(),
        name='appointment_download'
    ),
    path(
        'appointment/list',
        ForgetAppointmentSerialView.as_view(), name='appointment_forget'
    ),
    path('appointment/filter/', doctor_filter, name='load_doctor'),
    # for doctor
    path(
        'doctor/appointment/<int:pk>/add/record/',
        DoctorPrescriptionView.as_view(), name='add_record'
    ),
    path(
        'doctor/appointment/<int:pk>/record/view/',
        ViewAllSavedRecord.as_view(), name='view_record'
    ),
    # for patient record
    path(
        'appointment/<int:pk>/record/view/',
        PMSViewAllSavedRecord.as_view(), name='pms_view_record'
    ),
    path(
        'patient/<int:pk>/record/pdf',
        ViewAllDownloadRecord.as_view(), name='view_record_pdf'
    ),
]
