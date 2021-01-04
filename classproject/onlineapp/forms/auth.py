from django import forms


class LoginForm(forms.Form):

    username = forms.CharField(
        max_length=75,
        required=True,
        widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter username'}),
    )
    password = forms.CharField(
        max_length=75,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Enter password'}),
    )


class SignupForm(forms.Form):

    first_name = forms.CharField(
        max_length=75,
        required=True,
        widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter First Name'}),
    )
    last_name = forms.CharField(
        max_length=75,
        required=True,
        widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter Last Name'}),
    )
    username = forms.CharField(
        max_length=75,
        required=True,
        widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Choose a Username'}),
    )
    password = forms.CharField(
        max_length=75,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Enter Password'}),
    )
