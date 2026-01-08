"""Admin registrations for medical models."""

from django.contrib import admin

from .models import Doctor, Patient, PatientDoctorMapping


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name', 'owner', 'date_of_birth', 'gender')
	search_fields = ('first_name', 'last_name', 'owner__email')
	list_filter = ('gender',)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name', 'specialization', 'email', 'phone_number')
	search_fields = ('first_name', 'last_name', 'specialization', 'email')


@admin.register(PatientDoctorMapping)
class PatientDoctorMappingAdmin(admin.ModelAdmin):
	list_display = ('patient', 'doctor', 'assigned_by', 'created_at')
	search_fields = ('patient__first_name', 'patient__last_name', 'doctor__first_name', 'doctor__last_name')
