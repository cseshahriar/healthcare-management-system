from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from hospital.models import Doctor, CommonField
from patient_ms.models import Patient


class Appointment(CommonField):
    time_choices = (
        ('morning', "Morning"),
        ('evening', "Evening")
    )
    time = models.CharField(choices=time_choices, max_length=10)
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField(default=timezone.now)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}-{self.doctor.name}"


class Rating(CommonField):
    doctor = models.ForeignKey(
        Doctor, on_delete=models.PROTECT, related_name='ratings')
    patient = models.ForeignKey(
        Patient, on_delete=models.PROTECT, related_name='ratings')
    stars = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)]  # 1 to 5
    )
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.patient.name} - {self.stars} Stars for {self.doctor.name}'  # noqa
