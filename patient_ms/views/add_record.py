import logging

from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import View
from django.contrib.auth.mixins import (
    UserPassesTestMixin, LoginRequiredMixin
)
from django.contrib import messages
from patient_ms.models import (
    DoctorAppointment,
    DoctorPrescription,
    Patient
)
from patient_ms.forms import (
    DoctorPrescriptionForm,
    record_file_formset
)
from hospital.models import Doctor

logger = logging.getLogger(__name__)


class DoctorPrescriptionView(
    UserPassesTestMixin,
    LoginRequiredMixin,
    View
):
    model = DoctorPrescription
    form_class = DoctorPrescriptionForm
    file_form = record_file_formset
    template_name = 'dashboard/record/add_record.html'

    def test_func(self):
        """Tests if the user is active"""
        return self.request.user.is_active  # any active user

    def get(self, request, pk):
        appointment = DoctorAppointment.objects.filter(pk=pk).first()
        patient_object = appointment.patient.patient_data  # user.patient
        context = {
            'form': self.form_class,
            'file': self.file_form,
            'patient_object': patient_object,
            'object': appointment
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        appointment = DoctorAppointment.objects.filter(pk=pk).first()
        patient_object = appointment.patient.patient_data  # user.patient

        form = self.form_class(request.POST)
        file_form = self.file_form(request.POST, request.FILES)
        logger.info(f"{'*' * 10} patient_object: {patient_object}\n")
        try:
            if appointment and form.is_valid() and file_form.is_valid():
                save_object = form.save(commit=False)
                save_object.appointment = appointment
                save_object.doctor = self.request.user
                save_object.patient = patient_object
                save_object.save()
                logger.info(f"{'*' * 10} save_object: {save_object}\n")

                for file_form_object in file_form:
                    if file_form_object.is_valid():
                        file = file_form_object.save(commit=False)
                        file.record = save_object
                        file.save()
                return HttpResponseRedirect(self.get_success_url())
            else:
                logger.info(f"{'*' * 10} form.errors: {form.errors}\n")
                logger.info(f"{'*' * 10} file_form.errors: {file_form.errors}\n")
                messages.warning(self.request, "Unable to save record")
                return reverse_lazy("add_record", {'pk': appointment.pk})
        except Exception as e:
            logging.debug(request, f"Unable to save record {e}")
            messages.warning(self.request, "Unable to save record")
            return reverse_lazy("add_record", {'pk': appointment.pk})

    def get_success_url(self):
        messages.success(self.request, "Successfully new Prescription added")
        logger.debug("Successfully new Prescription added")
        return reverse_lazy("checked_appointment_list")
