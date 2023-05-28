from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm, CustomCreationForm
from django.contrib import messages
from django.contrib.auth.hashers import make_password

# Create your views here.
def home_page(request):

    return render(request, 'homepage.html', {})


class CustomLogInView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'registration/login-view.html'
    
    def get_success_url(self) -> str:
        return reverse('dashboard')

def register(request):
    print(request.method)
    if request.method == 'POST':
        form = CustomCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.master_pin = make_password(user.master_pin)
            user.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login-view')  # Redirect to login page after successful registration
        else:
            print(form.errors)
    else:
        form = CustomCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})