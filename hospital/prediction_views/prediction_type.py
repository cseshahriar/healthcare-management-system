import datetime
from django.urls import reverse_lazy
from patient_ms.models import Patient
from django.views.generic import TemplateView
from patient_ms.models import DoctorAppointment
from hospital.models import Doctor
from hospital.forms import DoctorFormUpdate
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)


class PredictionType(TemplateView):
    model = DoctorAppointment
    template_name = 'dashboard/prediction/type.html'

    def get_context_data(self, **kwargs):
        kwargs.setdefault('view', self)
        if self.extra_context is not None:
            kwargs.update(self.extra_context)

        qs = DoctorAppointment.objects.filter(
            doctor__user=self.request.user, is_visited=True
        )
        kwargs['visit_count'] = qs.count()
        return kwargs