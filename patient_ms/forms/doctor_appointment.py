from django import forms
from django.utils import timezone
from django.db.models import Count, Q, F
from django.core.exceptions import ValidationError

from hospital.models import Doctor
from patient_ms.models import DoctorAppointment

today = timezone.now().date()


class DoctorAppointmentForm(forms.ModelForm):
    class Meta:
        model = DoctorAppointment
        exclude = [
            'patient',
            "serial_number",
            "is_visited",
            'appointment_close_time',
            'status'
        ]
        widgets = {
            'division': forms.Select(attrs={
                'id': 'division'
            }),
            'district': forms.Select(attrs={
                'id': 'district'
            }),
            'upazila': forms.Select(attrs={
                'id': 'upazila'
            }),
            'appointment_day': forms.DateInput(
                attrs={
                    'type': 'date'
                }),
            'appointment_time': forms.TimeInput(
                attrs={
                    'type': 'time'
                })
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Pop the request if passed
        super(DoctorAppointmentForm, self).__init__(*args, **kwargs)
        self.fields['doctor'].required = True
        self.fields['appointment_day'].required = True
        self.fields['appointment_time'].required = True
        self.fields['problem'].required = True
        self.fields['doctor'].queryset = Doctor.objects.annotate(
            today_appointments_count=Count(
                'doctorappointment',
                filter=Q(
                    doctorappointment__created_at__date=today,
                    doctorappointment__status__in=['confirmed', 'completed']
                )  # noqa
            )
        ).filter(today_appointments_count__lt=F('daily_appointment_limit'))

    def clean(self):
        cleaned_data = super().clean()
        doctor = cleaned_data.get('doctor')
        today = timezone.now().date()
        doctor_daily_limit = doctor.daily_appointment_limit
        # max limit per day
        today_appointed_count = DoctorAppointment.objects.filter(
            created_at__date=today, doctor=doctor,
            status__in=['confirmed', 'completed']
        ).count()

        if today_appointed_count >= doctor_daily_limit:
            raise ValidationError(
                "Daily appointment limit reached for this doctor. \
                    Please try other days"
            )

        # a patient can one appointment a doctor
        if DoctorAppointment.objects.filter(
            patient=self.request.user,  # Assuming patient has a `user` field,
            doctor=doctor,
            appointment_day=today
        ).exists():
            self.add_error('doctor', 'Already a appointment exist for today for this Doctor.')  # noqa

        return cleaned_data
