from django.urls import path
from . import views
from . import registation_view
from address.views import (
    load_district,
    load_upazila
)
from .dashboard import (
    VisitedAppointmentList,
    UnVisitedAppointmentList,
    AllAppointmentList,
    AllPatientList,
    ProfileUpdate,
    DrProfileView,
)
from Core.views import (
    dr_change_password
)
from hospital import prediction_views
from hospital.views import search_doctor

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path(
        'dashboard/', views.DoctorDashboard.as_view(), name='doctor_dashboard'
    ),
    path('services/', views.ServiceListView.as_view(), name="services"),
    path('services/<int:pk>/', views.ServiceDetailView.as_view(),
         name="service_details"),
    path('doctors/', views.DoctorListView.as_view(), name="doctors"),
    path('doctors/<int:pk>/', views.DoctorDetailView.as_view(),
         name="doctor_details"),
    path('faqs/', views.FaqListView.as_view(), name="faqs"),
    path('gallery/', views.GalleryListView.as_view(), name="gallery"),
    path('contact/', views.ContactView.as_view(), name="contact"),
    path(
        'registration/type/',
        registation_view.RegistrationTypePages.as_view(),
        name="registration_type"
    ),
    path(
        'registration/',
        registation_view.RegistrationPages.as_view(), name="registration"
    ),
    path(
        'login/', views.LoginView.as_view(), name="login"
    ),
    path(
        'logout/', views.logout_request, name="logout"
    ),
    path('load-district/', load_district, name='load_district'),
    path('load-upazila/', load_upazila, name='load_upazila'),
    # Appointments
    path(
        'pending/appointment/list/',
        UnVisitedAppointmentList.as_view(), name='uncheck_appointment_list'
    ),
    path(
        'confirm/appointment/list/',
        VisitedAppointmentList.as_view(), name='checked_appointment_list'
    ),
    path(
        'all/appointment/list/',
        AllAppointmentList.as_view(), name='all_appointment_list'
    ),
    path('patient/list/', AllPatientList.as_view(), name='patient_list'),
    # doctor dashboard urls
    path(
        'doctor/<int:pk>/update/',
        ProfileUpdate.as_view(), name='doctor_update'
    ),
    path('doctor/<int:pk>/view/', DrProfileView.as_view(), name='doctor_view'),
    path(
        'doctor/password/change/',
        dr_change_password, name='dr_change_password'
    ),
    # Prediction url
    path(
        'prediction/type/', prediction_views.PredictionType.as_view(),
        name='prediction_type'
    ),
    path(
        'recommendation/doctors', search_doctor, name='search_doctor'
    ),

]
