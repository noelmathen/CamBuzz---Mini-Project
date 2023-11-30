# organisations/urls.py
from django.urls import path, include
from .views import (
    OrganisationRegistrationRequestApproveView,
    OrganisationRegistrationRequestRejectView,
    OrganisationRegistrationView
)

urlpatterns = [
#     path('register/', UserRegistrationView.as_view(), name='register'),
#     path('login/', UserLoginView.as_view(), name='login'),
#     path('profile/update/', UserProfileUpdateView.as_view(), name='user-profile-update'),
#     path('password/change/', ChangePasswordView.as_view(), name='change-password'), 
#     path('logout/', UserLogoutView.as_view(), name='logout'),
#     path('delete/', DeleteAccountView.as_view(), name='delete-account'),
    path('registration_request/<int:pk>/approve/', OrganisationRegistrationRequestApproveView.as_view(), name='organisationregistrationrequest_approve'),
    path('registration_request/<int:pk>/reject/', OrganisationRegistrationRequestRejectView.as_view(), name='organisationregistrationrequest_reject'),        
    path('register/', OrganisationRegistrationView.as_view(), name='organisation-register'),
]

