from typing import Any, Mapping
from django import forms
from django.contrib.auth.models import User
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList 
from .models import  payment 
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Submit

class AvailabilityForms(forms.Form):
    # user = forms.ModelChoiceField(queryset=User.objects.all(), empty_label=None, required=True)
    check_in = forms.DateTimeField(
        required=True,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    
    check_out = forms.DateTimeField(
        required=True,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )

class PaymentForm(forms.ModelForm):
    class Meta:
        model = payment
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            'amount',
            'vehicle_number',
            'Driving_license_number',
            Submit("submit","Pay",css_class="button white btn-block btn-primary")
        )
