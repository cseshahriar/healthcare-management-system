from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.db.models import Avg

from address.models import District, Division, Upazila, Thana


class CommonField(models.Model):
    ''' Abstract Mdoel '''
    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('cancelled', _('Cancelled')),
        ('confirmed', _('Confirmed')),
        ('completed', _('Completed')),
    )
    status = models.CharField(
        _('Status'), max_length=20, choices=STATUS_CHOICES, default='pending',
        null=True, blank=True
    )
    created_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        blank=True, null=True, related_name="%(app_label)s_%(class)s_createdby"
    )
    update_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        blank=True, null=True, related_name="%(app_label)s_%(class)s_updated"
    )
    deleted_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        blank=True, null=True, related_name="%(app_label)s_%(class)s_deleted"
    )
    order = models.CharField(
        _("Order"),
        max_length=255,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(
        _('Is Deleted'), default=False
    )

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    class Meta:
        abstract = True


class Slider(CommonField):
    ''' Home page sliders '''
    caption = models.CharField(max_length=150)
    slogan = models.CharField(max_length=120)
    image = models.ImageField(upload_to='sliders/')
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    service_page_url = models.URLField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.caption[:20]

    class Meta:
        verbose_name_plural = 'Slider'


class Speciality(CommonField):
    ''' Doctor speciality '''
    name = models.CharField(max_length=150)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = 'Doctor Speciality'


class Service(CommonField):
    ''' Hospital services '''
    title = models.CharField(max_length=120)
    description = models.TextField()
    items = models.ManyToManyField(to='Item',)
    thumbnail = models.ImageField(upload_to='services/')
    cover = models.ImageField(upload_to='services/')
    image1 = models.ImageField(upload_to='services/', blank=True, null=True)
    image2 = models.ImageField(upload_to='services/', blank=True, null=True)

    def __str__(self):
        return self.title


class Item(CommonField):
    title = title = models.CharField(max_length=120)

    def __str__(self):
        return self.title


class Subject(CommonField):
    ''' Doctor subject '''
    name = models.CharField(max_length=255)  # Medicine, Urology
    description = models.TextField(blank=True)

    def __str__(self):
        return str(self.name)


class Degree(CommonField):
    ''' Doctor degree '''
    name = models.CharField(max_length=255)  # MBBS, MS(ortho), PhD
    description = models.TextField(blank=True)

    def __str__(self):
        return str(self.name)


class Doctor(CommonField):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        blank=True, null=True, related_name="doctor"
    )
    name = models.CharField(max_length=120, null=True, blank=True)
    doctor_id = models.CharField(
        max_length=255, null=True, unique=True
    )
    speciality = models.ManyToManyField(
        Speciality, blank=True, related_name="specialities"
    )
    picture = models.ImageField(
        upload_to="doctors/", null=True, blank=True
    )
    details = models.TextField(blank=True, null=True)
    present_hospital = models.CharField(max_length=120, blank=True, null=True)
    twitter = models.CharField(max_length=120, blank=True, null=True)
    facebook = models.CharField(max_length=120, blank=True, null=True)
    instagram = models.CharField(max_length=120, blank=True, null=True)
    division = models.ForeignKey(
        Division, models.SET_NULL,
        related_name='doctor_division',
        null=True
    )
    district = models.ForeignKey(
        District, models.SET_NULL,
        related_name='doctor_district',
        null=True
    )
    upazila = models.ForeignKey(
        Upazila, models.SET_NULL,
        related_name='doctor_upazila',
        null=True, blank=True
    )
    post_code = models.PositiveIntegerField(
        null=True,
        help_text='Numeric 4 digits (ex: 1234)',
        validators=[RegexValidator(
            r"^[\d]{4}$", message='Numeric 4 digits (ex: 1234)'
        )]
    )
    address = models.TextField(
        null=True, help_text='Ex: 2/17, Mirpur-11',
        verbose_name="Chamber Address"
    )
    # working_symptoms = models.ManyToManyField(Symptom)
    is_vacation_mode = models.BooleanField(
        verbose_name="Activate Vacation Mode", default=False)
    year_of_experience = models.TextField(
        max_length=4, help_text="i.e 5", null=True, blank=False
        # Years of Experience Overall
    )
    availability_days = models.TextField(
        max_length=255, help_text="Sat, Sun, Mon, Tue, Wed, Thur",
        null=True, blank=False
    )
    availability_time = models.TextField(
        max_length=255, help_text="10:00 AM - 12:00 PM & 05:00 PM - 10:00 PM",
        null=True, blank=False
    )

    def __str__(self):
        return str(self.name)

    @property
    def average_rating(self):
        # Calculate the average rating
        average = self.ratings.aggregate(Avg('stars'))['stars__avg']
        return average if average is not None else 0.0  # Return 0 if no ratings

    @property
    def get_full__address(self):
        save_present_address = ''
        if self.address:
            save_present_address = ''.join(self.address)
        if self.upazila:
            save_present_address += f', {self.upazila} ,'
        if self.district:
            save_present_address += f' {self.district}'
        if self.post_code:
            save_present_address += f' - {self.post_code} ,'
        if self.division:
            save_present_address += f'{self.division} ,'
        save_present_address += 'Bangladesh '

        return save_present_address


class DoctorDegree(CommonField):
    doctor = models.ForeignKey(
        Doctor, on_delete=models.PROTECT, related_name='doctor_degrees')
    degree = models.ForeignKey(
        Degree, on_delete=models.PROTECT, related_name='doctor_degrees')
    subject = models.ForeignKey(
        Subject, on_delete=models.PROTECT, related_name='doctor_degrees')
    institute = models.CharField(max_length=255)
    passing_year = models.CharField(
        max_length=4, verbose_name="Year of Awarded",
    )


class Expertize(CommonField):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Faq(CommonField):
    question = models.CharField(max_length=120)
    answer = models.TextField()

    def __str__(self):
        return self.question


class Gallery(CommonField):
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to="gallery/")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Galleries"


class Contact(CommonField):
    name = models.CharField(
        max_length=120, null=True, blank=True
    )
    email = models.EmailField(
        _('Email Address'), max_length=255, blank=True, null=True
    )
    phone = models.CharField(
        _('Mobile Phone'), max_length=12, unique=True,
        validators=[RegexValidator(  # min: 10, max: 12 characters
            r'^[\d]{10,12}$', message='Format (ex: 0123456789)'
        )]
    )
    subject = models.CharField(
        max_length=120, null=True
    )

    message = models.TextField(
        blank=True, null=True
    )
    response = models.BooleanField(
        default=False
    )

    def __str__(self):
        return str(self.name)


class Feedback(CommonField):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        blank=True, null=True, related_name="feedbacks"
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    patient_type = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField(_("Feedback"), max_length=500, blank=False)
    images = models.ImageField(
        _("Photo"), upload_to="feedbacks/", null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Symptom(CommonField):
    """ Symptoms model """
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.name
