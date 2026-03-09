from django.contrib import admin

from doctors.models import DoctorRequest
from doctors.utils import send_doctor_approved_email

# Register your models here.


@admin.register(DoctorRequest)
class DoctorRequestAdmin(admin.ModelAdmin):

    list_display = ['user', 'status']

    def save_model(self, request, obj, form, change):

        if change:
            old_obj = DoctorRequest.objects.get(pk=obj.pk)

            # Check if status changed to approved
            if old_obj.status != "approved" and obj.status == "approved":
                send_doctor_approved_email(obj.user)

        super().save_model(request, obj, form, change)