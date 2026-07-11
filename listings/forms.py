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
class AddReview(forms.ModelForm):

    stars = forms.TypedChoiceField(
        choices= BusinessReview.choices,
        coerce=int,
        initial=5,
        empty_value=None,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = BusinessReview
        fields = ['stars', 'description']
        widgets = {
            'stars': forms.Select(attrs={'class': 'form-control','empty':"Rate Our Business"}),
            'description': forms.Textarea(attrs={'class': 'form-control review-desc-field',  'rows': 4,"placeholder":"Add your Review Message"}),
        }