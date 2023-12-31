#student/urls.py
from django.urls import path
from .views import (
    StudentRegistrationView,
    StudentProfileEditView,
    StudentInfoView,
    StudentProfileEditData,
)

urlpatterns = [
    path('register/', StudentRegistrationView.as_view(), name='register'),
    path('profile/editprofile/', StudentProfileEditView.as_view(), name='edit-profile'),
    path('info/', StudentInfoView.as_view(), name='student-info'),
    path('profileeditdata/', StudentProfileEditData.as_view(), name='profileeditdata'),
]

