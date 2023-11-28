from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserLogoutView, UserProfileUpdateView, ChangePasswordView, DeleteAccountView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='user-profile-update'),
    path('password/change/', ChangePasswordView.as_view(), name='change-password'), 
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('delete/', DeleteAccountView.as_view(), name='delete-account'),
]

