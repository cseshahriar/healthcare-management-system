import datetime
from django.urls import reverse_lazy
from patient_ms.models import Patient
from django.shortcuts import redirect
from django.views.generic import ListView, UpdateView, DetailView

from patient_ms.models import DoctorAppointment
from hospital.models import Doctor
from hospital.forms import DoctorFormUpdate
from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
)
import logging

logger = logging.getLogger(__name__)


class VisitedAppointmentList(LoginRequiredMixin, ListView):
    model = DoctorAppointment
    template_name = 'dashboard/appointment/vistied.html'

    def get_queryset(self):
        today = datetime.date.today()
        qs = self.model.objects.filter(
            doctor__user=self.request.user,
            appointment_day=today,
            status="completed",
        )
        return qs


class UnVisitedAppointmentList(LoginRequiredMixin, ListView):
    model = DoctorAppointment
    template_name = 'dashboard/appointment/not_vistied.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["doctor"] = Doctor.objects.filter(
            user=self.request.user).first()
        context["total"] = self.get_queryset().count()
        return context

    def get_queryset(self):
        today = datetime.date.today()
        qs = self.model.objects.filter(
            doctor__user=self.request.user,
            status__in=["pending", "confirmed", "cancelled"],
            appointment_day=today,
        ).order_by('serial_number')
        return qs

    def get_instance(self, request):
        pk = request.POST.get('id')
        return self.model._default_manager.filter(pk=pk).first()

    def post(self, request, *args, **kwargs):
        """post object with lines if not any payments"""
        # with page number
        submit = request.POST.get('submit')
        if submit == "confirm":
            instance = self.get_instance(request)
            # Check if instance exists
            if not instance:
                messages.warning(request, "Invoice not found.")
                return redirect('uncheck_appointment_list')

            instance.status = "confirmed"
            instance.save()
            messages.success(request, "Confirm successful!")
        elif submit == "completed":
            instance = self.get_instance(request)
            # Check if instance exists
            if not instance:
                messages.warning(request, "Invoice not found.")
                return redirect('uncheck_appointment_list')

            instance.status = "completed"
            instance.save()
            messages.success(request, "completed successful!")

        return redirect('uncheck_appointment_list')


class AllAppointmentList(LoginRequiredMixin, ListView):
    model = DoctorAppointment
    template_name = 'dashboard/appointment/all_appointment_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["doctor"] = Doctor.objects.filter(
            user=self.request.user).first()
        context["total"] = self.get_queryset().count()
        return context

    def get_queryset(self):
        qs = self.model.objects.filter(
            doctor__user=self.request.user,
        ).order_by('-created_at')
        return qs


class AllPatientList(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'dashboard/patient/list.html'


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = Doctor
    form_class = DoctorFormUpdate
    template_name = 'dashboard/profile/profile.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            logger.info(f"{'*' * 10} form.errors: {form.errors}\n")
            return self.form_invalid(form)

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        messages.success(self.request, "Successfully Updated")
        logger.info(f"{'*' * 10} self.object: {self.object}\n")
        return redirect('doctor_view', pk=self.object.pk)


class DrProfileView(LoginRequiredMixin, DetailView):
    model = Doctor
    template_name = 'dashboard/profile/profile_view.html'
