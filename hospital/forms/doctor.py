from django import forms
from hospital.models import Doctor, DoctorDegree
from django.forms import inlineformset_factory


class DoctorForm(forms.ModelForm):

    class Meta:
        model = Doctor
        fields = [
            "name",
            "picture",
            'speciality',
            'doctor_id',
        ]

    def __init__(self, *args, **kwargs):
        super(DoctorForm, self).__init__(*args, **kwargs)
        self.fields["name"].required = True
        self.fields["picture"].required = True
        self.fields["speciality"].required = True


class DoctorFormUpdate(forms.ModelForm):

    class Meta:
        model = Doctor
        exclude = ['user', ]
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
                }),
            'details': forms.Textarea(
                attrs={'rows': 10, 'cols': 5}
            ),
            'year_of_experience': forms.Textarea(
                attrs={'rows': 1, 'cols': 5}
            ),
            'availability_days': forms.Textarea(
                attrs={'rows': 1, 'cols': 5}
            ),
            'availability_time': forms.Textarea(
                attrs={'rows': 1, 'cols': 5}
            ),
            'is_vacation_mode': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(DoctorFormUpdate, self).__init__(*args, **kwargs)
        self.fields["name"].required = True
        self.fields["picture"].required = True
        self.fields["present_hospital"].required = True
        self.fields["offline_fee"].required = True
        self.fields["license_number"].required = True
        self.fields["valid_license_document"].required = True
        self.fields["speciality"].required = True
        self.fields["online_fee"].required = False
        self.fields['address'].widget.attrs['rows'] = 3


class DoctorDegreeForm(forms.ModelForm):

    class Meta:
        model = DoctorDegree
        fields = [
            'degree',
            'subject',
            'institute',
            'passing_year',
        ]

    def __init__(self, *args, **kwargs):
        super(DoctorDegreeForm, self).__init__(*args, **kwargs)
        self.fields["degree"].required = True
        self.fields["subject"].required = True


DoctorDegreeFormSet = inlineformset_factory(
    Doctor, DoctorDegree, form=DoctorDegreeForm, extra=1, can_delete=True
)
