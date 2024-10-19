from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from address.models import District, Division, Upazila, Thana
from django.utils.translation import gettext_lazy as _


class CommonField(models.Model):
    ''' Abstract Mdoel '''
    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('cancelled', _('Cancelled')),
        ('approved', _('Approved')),
        ('completed', _('Completed')),
    )
    status = models.CharField(
        _('Status'), max_length=20, choices=STATUS_CHOICES, default='pending',
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


class Doctor(CommonField):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        blank=True, null=True, related_name="doctor"
    )
    name = models.CharField(max_length=120, null=True, blank=True)
    doctor_id = models.CharField(
        max_length=255, null=True, unique=True
    )
    speciality = models.ForeignKey(
        Speciality, on_delete=models.PROTECT,
        blank=True, null=True, related_name="speciality"
    )
    picture = models.ImageField(
        upload_to="doctors/", null=True, blank=True
    )
    details = models.TextField(blank=True, null=True)
    present_hospital = models.CharField(max_length=120, blank=True, null=True)
    expertize = models.ManyToManyField(to='Expertize', blank=True)
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
        null=True
    )
    thana = models.ForeignKey(
        Thana, models.SET_NULL,
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
        null=True, help_text='Ex: 2/17, Mirpur-11'
    )

    def __str__(self):
        return str(self.name)

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
