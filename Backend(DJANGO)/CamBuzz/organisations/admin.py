# organisations/admin.py
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import OrganisationRegistrationRequest, Organisation
from django.http import HttpResponseRedirect

admin.site.register(Organisation)

class OrganisationRegistrationRequestAdmin(admin.ModelAdmin):
    list_display = ['get_organisation_name', 'status', 'approve_action', 'reject_action']

    def get_organisation_name(self, obj):
        return obj.organisation.user.first_name  # Assuming 'first_name' is the name field
    get_organisation_name.short_description = 'Organisation Name'

    def approve_action(self, obj):
        return format_html('<a class="button" href="{}">Approve</a>', obj.get_approve_url())

    def reject_action(self, obj):
        return format_html('<a class="button" href="{}">Reject</a>', obj.get_reject_url())

    def get_queryset(self, request):
        # Exclude approved requests from the list
        return super().get_queryset(request).filter(status=OrganisationRegistrationRequest.PENDING)

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('<path:request_id>/approve/', self.approve_view, name='organisations_organisationregistrationrequest_approve'),
            path('<path:request_id>/reject/', self.reject_view, name='organisations_organisationregistrationrequest_reject'),
        ]
        return custom_urls + urls

    def approve_view(self, request, request_id):
        try:
            request_obj = OrganisationRegistrationRequest.objects.get(id=request_id)
            # Check if the request is already rejected
            if request_obj.status == OrganisationRegistrationRequest.APPROVED:
                self.message_user(request, f'Registration request for {str(request_obj.organisation.user.first_name)} has already been approved.', level='ERROR')
            else:
                request_obj.approve_view(request)
                self.message_user(request, f'Registration request for {str(request_obj.organisation.user.first_name)} has been appoved successfully.')

        except OrganisationRegistrationRequest.DoesNotExist:
            self.message_user(request, 'Error: Registration request not found.', level='ERROR')

        # Redirect back to the list view
        return HttpResponseRedirect(reverse('admin:organisations_organisationregistrationrequest_changelist'))

    def reject_view(self, request, request_id):
        try:
            request_obj = OrganisationRegistrationRequest.objects.get(id=request_id)
            # Check if the request is already rejected
            if request_obj.status == OrganisationRegistrationRequest.REJECTED:
                self.message_user(request, f'Registration request for {str(request_obj.organisation.user.first_name)} has already been rejected.', level='ERROR')
            else:
                request_obj.reject_view(request)
                self.message_user(request, f'Registration request for {str(request_obj.organisation.user.first_name)} has been rejected successfully.')

        except OrganisationRegistrationRequest.DoesNotExist:
            self.message_user(request, 'Error: Registration request not found.', level='ERROR')

        # Redirect back to the list view
        return HttpResponseRedirect(reverse('admin:organisations_organisationregistrationrequest_changelist'))
    
admin.site.register(OrganisationRegistrationRequest, OrganisationRegistrationRequestAdmin)

