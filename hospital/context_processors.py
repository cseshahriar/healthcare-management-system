from .models import Doctor, Service


def footer_content(request):
    services = Service.objects.filter(is_active=True).order_by('order')
    doctors = Doctor.objects.filter(is_active=True).order_by('order')
    context = {
        'services': services,
        'doctors': doctors
    }
    return context
