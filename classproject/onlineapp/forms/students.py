from django import forms
from onlineapp.models import *


class AddStudent(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['id', 'dob', 'college']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter Student name'}),
            'email': forms.EmailInput(attrs={'class': 'input', 'placeholder': 'Enter Student email'}),
            'db_folder': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter DB name'}),
            'dropped_out': forms.CheckboxInput(),
        }


class AddMock1(forms.ModelForm):
    class Meta:
        model = MockTest1
        exclude = ['id', 'total', 'student']
        widgets = {
            'problem1': forms.NumberInput(attrs={'class': 'input', 'placeholder': 'Enter marks for problem 1'}),
            'problem2': forms.NumberInput(attrs={'class': 'input', 'placeholder': 'Enter marks for problem 2'}),
            'problem3': forms.NumberInput(attrs={'class': 'input', 'placeholder': 'Enter marks for problem 3'}),
            'problem4': forms.NumberInput(attrs={'class': 'input', 'placeholder': 'Enter marks for problem 4'}),
        }
