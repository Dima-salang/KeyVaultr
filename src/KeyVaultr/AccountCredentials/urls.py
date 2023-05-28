from django.urls import path
from .views import CredentialsCreateView, dashboard, decrypt_password, show_password, CredentialUpdate, CredentialDelete

urlpatterns = [
    path('credentials/create', CredentialsCreateView.as_view(), name='cred-create'),
    path('credentials/dashboard', dashboard, name='dashboard'),
    path('decrypt-password/', decrypt_password, name='decrypt-password'),
    path('show/password/<int:acc_id>', show_password, name='show-password'),
    path('credentials/update/<int:pk>', CredentialUpdate.as_view(), name='cred-update'),
    path('credentials/delete/<int:pk>', CredentialDelete.as_view(), name='cred-delete'),
]