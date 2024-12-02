from datetime import datetime
from django.views.generic import DetailView
from patient_ms.views.get_pdf import render_pdf
from patient_ms.models import DoctorAppointment


class AppointmentCopyPDFView(DetailView):
    model = DoctorAppointment
    template_name = 'appointment/download.html'

    def get(self, request, pk, ):
        save_object = self.model.objects.get(pk=pk)
        context = {'object': save_object}
        today_date = datetime.today().strftime('%Y-%m-%d')  # Format: YYYY-MM-DD
        file_name = f"appointment_copy-{save_object.pk}-{today_date}"

        return render_pdf(
            request, self.template_name, context, file_name
        )
