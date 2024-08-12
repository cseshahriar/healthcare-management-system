"""Core > forms > registration.py"""
# DJANGO IMPORTS
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

USER_MODEL = get_user_model()


class SignupForm(UserCreationForm):
    """New user registration and signup form"""

    class Meta:
        """Meta class"""
        model = USER_MODEL
        fields = ('first_name', 'last_name', 'email', 'phone')


class CommonSignupForm(UserCreationForm):
    """New user registration and signup form"""

    class Meta:
        """Meta class"""
        model = USER_MODEL
        fields = [
            'phone'
        ]

    def __init__(self, *args, **kwargs):
        super(CommonSignupForm, self).__init__(*args, **kwargs)
        self.fields["phone"].required = True

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get("phone")
        if phone:
            if USER_MODEL.objects.filter(phone=phone).exists():
                raise forms.ValidationError("Phone number already exists.")

        return cleaned_data


class UpdateForm(forms.ModelForm):
    class Meta:
        """Meta class"""
        model = USER_MODEL
        fields = ('first_name', 'last_name', 'phone',)
