from django import forms
from django.forms import modelformset_factory
from hospital.models import Symptom


class SymptomSearchForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "Please enter symptom's i.e fever, back pain",
                "rows": 3,
                "cols": 100,
                "style": "width: 100%",
                "class": "form-control",
                "required": True,
            }
        ),
        label="Please write symptom's i.e. fever, back pain",
        help_text="Please write with comma separated i.e fever, back pain etc"
    )

    class Meta:
        model = Symptom
        fields = ("name", )


SymptomSearchFormSet = modelformset_factory(
    Symptom, form=SymptomSearchForm, extra=1, can_delete=True
)
