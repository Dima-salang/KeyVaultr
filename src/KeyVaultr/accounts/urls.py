from django.urls import path
from .views import home_page, CustomLogInView, register

urlpatterns = [
    path('', home_page, name='home_page'),
    path(r'login-view/', CustomLogInView.as_view(), name='login-view'),
    path('register/', register, name='register'),
    
]