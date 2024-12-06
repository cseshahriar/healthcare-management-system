import logging
import datetime
from django.db.models import Q
from django.urls import reverse_lazy
from patient_ms.models import Patient
from django.shortcuts import redirect
from django.views.generic import ListView, UpdateView, DetailView

from patient_ms.models import DoctorAppointment
from hospital.models import Doctor
from hospital.forms import DoctorFormUpdate, DoctorDegreeFormSet
from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
)

from hospital.uility import sent_sms
logger = logging.getLogger(__name__)


class VisitedAppointmentList(LoginRequiredMixin, ListView):
    model = DoctorAppointment
    template_name = 'dashboard/appointment/vistied.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["doctor"] = Doctor.objects.filter(
            user=self.request.user).first()
        context["total"] = self.get_queryset().count()
        q = self.request.GET.get('q')
        context["q"] = q
        return context

    def get_queryset(self):
        today = datetime.date.today()
        qs = self.model.objects.filter(
            doctor__user=self.request.user,
            appointment_day=today,
            status="completed",
        )
        q = self.request.GET.get('q')
        if q:
            q = q.strip()
            qs = qs.filter(
                patient__phone__icontains=q
            )

        date = self.request.GET.get('date')
        if date:
            date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            qs = qs.filter(appointment_day=date)
        return qs


class UnVisitedAppointmentList(LoginRequiredMixin, ListView):
    model = DoctorAppointment
    template_name = 'dashboard/appointment/not_vistied.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["doctor"] = Doctor.objects.filter(
            user=self.request.user).first()
        context["total"] = self.get_queryset().count()
        q = self.request.GET.get('q')
        context["q"] = q
        return context

    def get_queryset(self):
        today = datetime.date.today()
        qs = self.model.objects.filter(
            doctor__user=self.request.user,
            status__in=["pending", "cancelled"],
            appointment_day=today,
        ).order_by('serial_number')
        q = self.request.GET.get('q')
        if q:
            q = q.strip()
            qs = qs.filter(
                patient__phone__icontains=q
            )

        date = self.request.GET.get('date')
        if date:
            filter_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            qs = qs.filter(appointment_day=filter_date)
        return qs

    def get_instance(self, request):
        pk = request.POST.get('id')
        return self.model._default_manager.filter(pk=pk).first()

    def post(self, request, *args, **kwargs):
        """post object with lines if not any payments"""
        doctor = Doctor.objects.filter(user=request.user).first()
        # with page number
        submit = request.POST.get('submit')
        if submit == "confirm":
            appointment_date = request.POST.get('appointment_date')
            appointment_time = request.POST.get('appointment_time')
            instance = self.get_instance(request)
            # Check if instance exists
            if not instance:
                messages.warning(request, "Invoice not found.")
                return redirect('uncheck_appointment_list')

            if instance.serial_number <= doctor.daily_appointment_limit:  # limit exceeded check  # noqa
                instance.status = "confirmed"
                if appointment_date != '':
                    instance.appointment_day = datetime.datetime.strptime(
                        appointment_date, '%Y-%m-%d'
                    ).date()

                if appointment_time != '':
                    instance.appointment_time = datetime.datetime.strptime(
                        appointment_time, '%H:%M'
                    ).time()
                instance.save()
                messages.success(request, "Confirm successful!")
                # ================================= send sms ==================
                try:
                    logger.info(f"{'*' * 10} sms block called\n")
                    api_key = doctor.api_key  # config
                    sender_id = doctor.senderid  # config
                    address = doctor.address
                    serial_number = instance.serial_number
                    date = instance.appointment_day.strftime('%Y-%m-%d')
                    time = instance.appointment_time.strftime('%H:%M')
                    msg = f"Your appointment is confirmed. Serial: {serial_number}, Date: {date}, Time:{time}, address: {address}"  # noqa
                    logger.info(f"{'*' * 10} sms body : {msg}\n")
                    response = sent_sms(
                        api_key=api_key,
                        senderid=sender_id,
                        phone=instance.patient.phone,
                        message=msg
                    )
                    logger.info(f"{'*' * 10} sms response: {response}\n")
                except Exception:
                    logger.info(
                        self.request,
                        "Oops! Unable to send SMS. Please try again."
                    )
            else:
                messages.warning(
                    request, "Sorry, Today appointment is fulfilled.")
                return redirect('uncheck_appointment_list')
        elif submit == "completed" or submit == "completed_paid":
            instance = self.get_instance(request)
            # Check if instance exists
            if not instance:
                messages.warning(request, "Invoice not found.")
                return redirect('uncheck_appointment_list')

            instance.status = "completed"
            if submit == "completed_paid":
                instance.paid = True

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
        q = self.request.GET.get('q')
        context["q"] = q
        return context

    def get_queryset(self):
        qs = self.model.objects.filter(
            doctor__user=self.request.user,
        ).order_by('-appointment_day')

        q = self.request.GET.get('q')
        logger.info(f"{'*' * 10} q: {q}\n")
        if q:
            q = q.strip()
            qs = qs.filter(
                patient__phone__icontains=q
            )
            logger.info(f"{'*' * 10} q qs: {qs}\n")

        date = self.request.GET.get('date')
        if date:
            filter_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            logger.info(f"{'*' * 10} date: {filter_date} {type(filter_date)}\n")
            qs = qs.filter(appointment_day=filter_date)
            logger.info(f"{'*' * 10} date qs: {qs}\n")

        return qs.distinct()

    def post(self, request, *args, **kwargs):
        """post object with lines if not any payments"""
        doctor = Doctor.objects.filter(user=request.user).first()
        # with page number
        submit = request.POST.get('submit')
        if submit == "confirm":
            appointment_date = request.POST.get('appointment_date')
            appointment_time = request.POST.get('appointment_time')
            instance = self.get_instance(request)
            # Check if instance exists
            if not instance:
                messages.warning(request, "Invoice not found.")
                return redirect('uncheck_appointment_list')

            if instance.serial_number <= doctor.daily_appointment_limit:  # limit exceeded check  # noqa
                instance.status = "confirmed"
                if appointment_date != '':
                    instance.appointment_day = datetime.datetime.strptime(
                        appointment_date, '%Y-%m-%d'
                    ).date()

                if appointment_time != '':
                    instance.appointment_time = datetime.datetime.strptime(
                        appointment_time, '%H:%M'
                    ).time()
                instance.save()
                messages.success(request, "Confirm successful!")
                # ================================= send sms ==================
                try:
                    logger.info(f"{'*' * 10} sms block called\n")
                    api_key = doctor.api_key  # config
                    sender_id = doctor.senderid  # config
                    address = doctor.address
                    serial_number = instance.serial_number
                    date = instance.appointment_day.strftime('%Y-%m-%d')
                    time = instance.appointment_time.strftime('%H:%M')
                    msg = f"Your appointment is confirmed. Serial: {serial_number}, Date: {date}, Time:{time}, address: {address}"  # noqa
                    logger.info(f"{'*' * 10} sms body : {msg}\n")
                    response = sent_sms(
                        api_key=api_key,
                        senderid=sender_id,
                        phone=instance.patient.phone,
                        message=msg
                    )
                    logger.info(f"{'*' * 10} sms response: {response}\n")
                except Exception:
                    logger.info(
                        self.request,
                        "Oops! Unable to send SMS. Please try again."
                    )
            else:
                messages.warning(
                    request, "Sorry, Today appointment is fulfilled.")
                return redirect('uncheck_appointment_list')
        elif submit == "completed" or submit == "completed_paid":
            instance = self.get_instance(request)
            # Check if instance exists
            if not instance:
                messages.warning(request, "Invoice not found.")
                return redirect('uncheck_appointment_list')

            instance.status = "completed"
            if submit == "completed_paid":
                instance.paid = True

            instance.save()
            messages.success(request, "completed successful!")

        return redirect('uncheck_appointment_list')

class AllPatientList(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'dashboard/patient/list.html'


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = Doctor
    form_class = DoctorFormUpdate
    template_name = 'dashboard/profile/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()
        doctor_degree_formset = DoctorDegreeFormSet(
            self.request.POST or None, instance=self.object,
            prefix="degree"
        )
        context["doctor_degree_formset"] = doctor_degree_formset
        context["total"] = self.get_queryset().count()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        self.object = self.get_object()
        doctor_degree_formset = DoctorDegreeFormSet(
            self.request.POST, instance=self.object,
            prefix="degree"
        )
        if form.is_valid() and doctor_degree_formset.is_valid():
            return self.form_valid(form, doctor_degree_formset)
        else:
            logger.info(f"{'*' * 10} form.errors: {form.errors}\n")
            return self.form_invalid(form, doctor_degree_formset)

    def form_valid(self, form, doctor_degree_formset):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        doctor_degree = doctor_degree_formset.save()
        messages.success(self.request, "Successfully Updated")
        logger.info(f"{'*' * 10} self.object: {self.object}\n")
        return redirect('doctor_view', pk=self.object.pk)

    def form_invalid(self, form, doctor_degree_formset):
        """If the form is invalid, render the invalid form."""
        messages.warning(self.request, "Form Invalid")
        return self.render_to_response(self.get_context_data(
            form=form, doctor_degree_formset=doctor_degree_formset))


class DrProfileView(LoginRequiredMixin, DetailView):
    model = Doctor
    template_name = 'dashboard/profile/profile_view.html'
