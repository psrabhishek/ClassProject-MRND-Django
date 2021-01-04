from django import forms
from onlineapp.models import College


class AddCollege(forms.ModelForm):
    class Meta:
        model = College
        exclude = ['id']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter College name'}),
            'location': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter College location'}),
            'acronym': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter College acronym'}),
            'contact': forms.EmailInput(attrs={'class': 'input', 'placeholder': 'Enter College contact'}),
        }
