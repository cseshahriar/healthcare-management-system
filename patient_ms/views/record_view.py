import logging
from datetime import datetime
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import (
    UserPassesTestMixin, LoginRequiredMixin, PermissionRequiredMixin
)
from django.contrib import messages
from django.urls import reverse_lazy
from patient_ms.models import (
    DoctorPrescription,
    Patient
)
from patient_ms.views.get_pdf import render_pdf

logger = logging.getLogger(__name__)


class ViewAllSavedRecord(
    UserPassesTestMixin,
    LoginRequiredMixin,
    View
):
    template_name = 'dashboard/record/record_view.html'
    model = DoctorPrescription

    def test_func(self):
        """Tests if the user is active"""
        return self.request.user.is_active  # any active user

    def get(self, request, pk):
        try:
            patient_object = Patient.objects.get(
                pk=pk
            )
        except Exception as e:
            logging.debug(request, f'Unable to get data {e}')
            patient_object = None

        objects_list = self.model.objects.filter(
            patient=patient_object
        ).order_by('-created_at')
        context = {
            "objects_list": objects_list,
            "patient": patient_object
        }
        return render(request, self.template_name, context)


class ViewAllDownloadRecord(UserPassesTestMixin, LoginRequiredMixin, View):
    template_name = 'dashboard/record/record_view_pdf.html'
    model = DoctorPrescription

    def test_func(self):
        """Tests if the user is active"""
        return self.request.user.is_active  # any active user

    def get(self, request, pk):
        prescription_pk = request.GET.get('prescription_pk')
        try:
            patient_object = Patient.objects.get(
                pk=pk
            )
        except Exception as e:
            logging.debug(request, f'Unable to get data {e}')
            patient_object = None

        prescription = self.model.objects.filter(pk=prescription_pk).first()
        today_date = datetime.today().strftime('%Y-%m-%d')  # Format: YYYY-MM-DD
        file_name = f"prescription_copy-{prescription.pk}-{today_date}"

        context = {
            "object": prescription,
            "patient": patient_object
        }
        return render_pdf(request, self.template_name, context, file_name)
