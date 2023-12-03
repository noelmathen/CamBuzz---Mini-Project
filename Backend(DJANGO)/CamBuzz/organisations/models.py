# organisations/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.html import format_html
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from accounts.models import CustomUser

class Organisation(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, primary_key=True, )
    photo = models.ImageField(upload_to='organisation_photos/', blank=True, null=True)
    about = models.TextField()
    email = models.EmailField(unique=True)
    website_link = models.URLField(blank=True, null=True)
    linkedin_profile_link = models.URLField(blank=True, null=True)
    instagram_username = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        # Set is_active to False when creating a new instance
        if not self.id:
            self.is_active = False

        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('organisations:organisation_detail', args=[str(self.id)])
    
    # # Override save method to properly hash the password using set_password
    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         # Set is_active to False when creating a new instance
    #         self.is_active = False

    #         # Use set_password to hash the password
    #         self.set_password(self.password)

    #     super().save(*args, **kwargs)

# # Add related_name to avoid clashes
# Organisation._meta.get_field('groups').remote_field.related_name = 'organisation_groups'
# Organisation._meta.get_field('user_permissions').remote_field.related_name = 'organisation_user_permissions'


class OrganisationRegistrationRequest(models.Model):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]

    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return f"{self.organisation.user.username} - {self.get_status_display()}"
        # return f"{self.organisation.first_name} - {self.get_status_display()}"

    def get_absolute_url(self):
        return reverse('organisations:registration_request_detail', args=[str(self.id)])

    def get_approve_url(self):
        return reverse('admin:organisations_organisationregistrationrequest_approve', args=[str(self.id)])

    def get_reject_url(self):
        return reverse('admin:organisations_organisationregistrationrequest_reject', args=[str(self.id)])

    def approve_view(self, request):
        # Check if the request is already approved
        if self.status == self.APPROVED:
            raise ValidationError('This registration request has already been approved.')

        if not self.organisation.first_name or not self.organisation.email:
            raise ValidationError('Organization must provide a name and email before approval.')
        
        # Update the status to 'approved'
        self.status = self.APPROVED
        self.save()

        # Activate the user in the Organisation model
        self.organisation.is_active = True
        self.organisation.save()

        # Send an approval email
        send_approval_email(self.organisation)


    def reject_view(self, request):
        # Check if the request is already rejected
        if self.status == self.REJECTED:
            raise ValidationError('This registration request has already been rejected.')
        if not self.organisation.first_name or not self.organisation.email:
            raise ValidationError('Organization must provide a name and email before approval.')
        
        self.status = self.REJECTED
        self.save()
        
        self.organisation.is_active = False
        self.organisation.save()

        send_rejection_email(self.organisation)

# Handle Email Notifications
def send_approval_email(organisation):
    try: 
        subject = 'Your registration request has been approved'
        message = render_to_string('organisations/approval_email.txt', {'organisation': organisation})
        from_email = 'cambuzz03@gmail.com'  # Update with your email
        recipient_list = [organisation.email]
        send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        print(f"Error sending approval email: {e}")

def send_rejection_email(organisation):
    subject = 'Your registration request has been rejected'
    message = render_to_string('organisations/rejection_email.txt', {'organisation': organisation})
    from_email = 'cambuzz03@gmail.com'  # Update with your email
    recipient_list = [organisation.email]
    send_mail(subject, message, from_email, recipient_list)
    

