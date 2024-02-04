from django.urls import path
from .views import (
    LoginView,
    ChangePasswordView,
    UserLogoutView,
    DeleteAccountView,
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('changepassword/', ChangePasswordView.as_view(), name='change-password'), 
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('deleteaccount/', DeleteAccountView.as_view(), name='delete-account'),
]

