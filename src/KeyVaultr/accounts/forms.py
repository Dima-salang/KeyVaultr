from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

User = get_user_model()
class CustomCreationForm(UserCreationForm):
    master_pin = forms.CharField(
        widget=forms.PasswordInput(),
        help_text="IMPORTANT: Enter a secure PIN to protect your account. Keep this somewhere safe as it will be used to access your sensitive information."
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2', 'master_pin')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['master_pin'].label = 'Master PIN'


    def save(self, commit=True):
            user = super().save(commit=False)
            if commit:
                user.save()
            return user


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('email', 'username')  # Include the email field


class CustomAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))
    master_pin = forms.CharField(
        widget=forms.PasswordInput(),
        label="Master PIN",
    )


    class Meta:
        model = CustomUser
        fields = '__all__'


    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        try:
            User.objects.get(email=email, username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("Invalid email")
        except User.MultipleObjectsReturned:
            raise forms.ValidationError("This email is already registered in the system. Use another one.")
        return email
    
    def clean_master_pin(self):
        master_pin = self.cleaned_data.get('master_pin')
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        email = self.cleaned_data.get('email')
        try:
            user = User.objects.get(username=username, email=email)
            if not check_password(master_pin, user.master_pin):
                print(master_pin)
                print(user.master_pin)
                raise forms.ValidationError("Invalid Master PIN")
        except user.DoesNotExist:
            raise forms.ValidationError("Invalid Master PIN")
        return master_pin
