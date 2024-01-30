# myapp/forms.py
from django import forms
from .utils import get_wine_names

class WineSelectionForm(forms.Form):
    wine_choices = [('CUSTOM', 'Customize')] + [(name, name) for name in get_wine_names('datasetup/wine.csv')]
    wine_select = forms.ChoiceField(choices=wine_choices, required=True)
