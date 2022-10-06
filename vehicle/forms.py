from dataclasses import field, fields
from django import forms

from .models import Vehicle





class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = "__all__"

      
