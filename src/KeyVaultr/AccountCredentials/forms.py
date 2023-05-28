from django import forms 
from .models import AccountCredential


class CredentialCreateForm(forms.ModelForm):
    class Meta:
        model = AccountCredential
        exclude = ['user', 'encrypted_password', 'password_salt']
        widgets = {
            'password': forms.PasswordInput(),  # Set the password field widget to PasswordInput
        }