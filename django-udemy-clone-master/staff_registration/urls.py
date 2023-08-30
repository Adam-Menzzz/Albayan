from django.urls import path
from staff_registration.views import register_as_staff

app_name = 'staff_registration'

urlpatterns = [
    path('register/', register_as_staff, name='register'),
]
