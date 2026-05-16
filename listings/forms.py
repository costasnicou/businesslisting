from django import forms
from .models import *
class BusinessHoursAdminForm(forms.ModelForm):

    class Meta:
        model = BusinessHours
        fields = "__all__"

        widgets = {
            "open_time": forms.TimeInput(
                attrs={
                    "type": "time",
                    "step": "60"
                },
                format="%H:%M"
            ),

            "close_time": forms.TimeInput(
                attrs={
                    "type": "time",
                    "step": "60"
                },
                format="%H:%M"
            ),
        }