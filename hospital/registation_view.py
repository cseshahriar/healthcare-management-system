import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from Core.forms import CommonSignupForm
from hospital.forms import DoctorForm
from patient_ms.forms import PatientForm


logger = logging.getLogger(__name__)


class RegistrationTypePages(View):
    template_name = 'hospital/registation_type.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        # set session variable
        return render(request, self.template_name, {})


class RegistrationPages(View):
    template_name = 'hospital/registation.html'

    def get(self, request, *args, **kwargs):
        type = request.GET.get('type', None)
        context = {
            'registration_type': type,
            "doctor_form": DoctorForm(request.POST or None, request.FILES or None),
            "signup_form": CommonSignupForm(request.POST or None),
            "patient_form": PatientForm(request.POST or None),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        registration_type = request.GET.get('type', None)
        doctor_form = DoctorForm(request.POST, request.FILES)
        signup_form = CommonSignupForm(request.POST)
        patient_form = PatientForm(request.POST)

        if registration_type == "patient":
            logger.info(f"{'*' * 10} post patient\n")
            if patient_form.is_valid() and signup_form.is_valid():
                patient_group, is_create = Group.objects.get_or_create(
                    name='Patient'
                )
                save_user = signup_form.save()
                save_user.groups.add(patient_group)
                obj = patient_form.save(commit=False)
                obj.user = save_user
                obj.save()
                messages.success(self.request, "Account successfully created")
                logger.info(f"{'*' * 10} Patient account successfully created")
                return HttpResponseRedirect('/')
            else:
                context = {
                    'registration_type': registration_type,
                    "signup_form": CommonSignupForm(request.POST or None),
                    "doctor_form": DoctorForm(
                        request.POST or None, request.FILES or None),
                    "patient_form": PatientForm(request.POST or None),
                }
                return render(request, self.template_name, context)
        else:
            logger.info(f"{'*' * 10} post doctor \n")
            if doctor_form.is_valid() and signup_form.is_valid():
                doctor_group, is_create = Group.objects.get_or_create(
                    name='Doctor'
                )
                save_user = signup_form.save()
                save_user.groups.add(doctor_group)
                obj = doctor_form.save(commit=False)
                obj.user = save_user
                obj.save()
                doctor_form.save_m2m()
                messages.success(self.request, "Account successfully created")
                logger.info(f"{'*' * 10} Doctor Account successfully created")
                return HttpResponseRedirect('/')
            else:
                context = {
                    'registration_type': registration_type,
                    "signup_form": CommonSignupForm(request.POST or None),
                    "doctor_form": DoctorForm(
                        request.POST or None, request.FILES or None),
                    "patient_form": PatientForm(request.POST or None),
                }
                return render(request, self.template_name, context)
