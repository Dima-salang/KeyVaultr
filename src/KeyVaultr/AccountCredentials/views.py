from typing import Optional, Type
from django import forms
from django.forms.models import BaseModelForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.http import HttpResponse, JsonResponse
from .forms import CredentialCreateForm
from .models import AccountCredential
from django.contrib.auth.hashers import make_password
from cryptography.fernet import Fernet
import os
import base64

# Create your views here.
class CredentialsCreateView(LoginRequiredMixin, CreateView):
    form_class = CredentialCreateForm
    template_name = 'create-cred.html'
    

@login_required
def dashboard(request):
    user_creds = AccountCredential.objects.filter(user=request.user).order_by('-is_favorite', '-date_created', )
    form = CredentialCreateForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            credential = form.save(commit=False)
            credential.user = request.user
            credential.set_password(request.user.master_pin)
            credential.save()
            messages.success(request, 'Credential created successfully.')
            return redirect('dashboard')  # Redirect to the dashboard or any other page

    context = {
        'user_creds': user_creds,
        'form': form,
    }
    return render(request, 'dashboard.html', context)

@login_required
def show_password(request, acc_id):
    user_cred = get_object_or_404(AccountCredential, id=acc_id, user=request.user)
    print(f"Got object: {user_cred}")
    
    if user_cred.encrypted_password and request.user.master_pin:
        print("Encrypted pass: True, Master pin: True")
        try:
            encrypted_password_bytes = user_cred.encrypted_password
            print(f"Encrypted password bytes: {encrypted_password_bytes}")
            user = request.user  # Assuming you have authenticated the user
            account = AccountCredential.objects.get(encrypted_password=encrypted_password_bytes)

            
            # Decrypt the encrypted password
            decrypted_password = account.get_password()
            response = {
                'decrypted_password': decrypted_password
            }
            return render(request, 'show-password.html', response)
        except:
            pass
    



    return render(request, 'show-password.html', {})

@login_required
def decrypt_password(request):
    print('called decrypt password function...')
    print('POST data:', request.POST)
    encrypted_password = request.POST.get('encrypted_password')
    master_pin = request.POST.get('master_pin')

    if request.method == 'POST':
        try:
            print(f"encrypted password: {encrypted_password}")
            encrypted_password_bytes = base64.urlsafe_b64decode(encrypted_password)
            print(encrypted_password_bytes)
            user = request.user  # Assuming you have authenticated the user
            
            credential = AccountCredential.objects.get(user=user, encrypted_password=encrypted_password_bytes)
            print(f"Account credential: {credential}")
            
            # Decrypt the encrypted password
            decrypted_password = credential.get_password()
            
            response = {
                'decrypted_password': decrypted_password
            }
            return JsonResponse(response)
        except AccountCredential.DoesNotExist:
            response = {
                'error': 'Invalid credentials.'
            }
            return JsonResponse(response, status=400)

    response = {
        'error': 'Missing encrypted_password or master_pin.'
    }
    return JsonResponse(response, status=400)


class CredentialUpdate(LoginRequiredMixin, UpdateView):
    model = AccountCredential
    template_name = 'update-credential.html'
    fields = ('title', 'username', 'email', 'password', 'website', 'notes', 'is_favorite')

    def form_valid(self, form):
        # Retrieve the current user
        user = self.request.user

        # Get the credential instance being updated
        credential = form.instance

        # Set the user and encrypt the password
        credential.user = user
        credential.password = form.cleaned_data['password']
        credential.set_password(user.master_pin)

        # Save the updated credential
        messages.success(self.request, 'Credential updated successfully.')
        return super().form_valid(form)
    
    def get_success_url(self):
        
        return reverse('dashboard')
    

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['password'].widget = forms.PasswordInput()
        return form


class CredentialDelete(LoginRequiredMixin, DeleteView):
    model = AccountCredential
    template_name = 'delete-credential.html'
    success_url = reverse_lazy('dashboard')


    
