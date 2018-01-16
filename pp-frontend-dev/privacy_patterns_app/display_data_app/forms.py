from django import forms
from .models import FilterModel

class FilterForm(forms.ModelForm):
    class Meta:
        model = FilterModel
        fields = ['filter_options']