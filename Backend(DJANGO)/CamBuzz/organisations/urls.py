# organisations/urls.py
from django.urls import path, include
from .views import (
    OrganisationRegistrationRequestApproveView,
    OrganisationRegistrationRequestRejectView,
    OrganisationRegistrationView,
    OrganisationProfileEditView
)

urlpatterns = [
    path('registration_request/<int:pk>/approve/', OrganisationRegistrationRequestApproveView.as_view(), name='organisationregistrationrequest_approve'),
    path('registration_request/<int:pk>/reject/', OrganisationRegistrationRequestRejectView.as_view(), name='organisationregistrationrequest_reject'),        
    path('profile/editprofile/', OrganisationProfileEditView.as_view(), name='organisation-profile-edit'),        
    path('register/', OrganisationRegistrationView.as_view(), name='organisation-register'),
]

