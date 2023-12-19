#student/urls.py
from django.urls import path
from .views import (
    StudentRegistrationView,
    StudentProfileEditView
)

urlpatterns = [
    path('register/', StudentRegistrationView.as_view(), name='register'),
    path('profile/editprofile/', StudentProfileEditView.as_view(), name='edit-profile'),
]

