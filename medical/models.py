"""Domain models for patients, doctors, and their relationships."""

from django.conf import settings
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Patient(TimeStampedModel):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patients')
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    medical_history = models.TextField(blank=True)

    class Meta:
        ordering = ('first_name', 'last_name')

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()


class Doctor(TimeStampedModel):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    specialization = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=30, blank=True)

    class Meta:
        ordering = ('specialization', 'last_name')

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}".strip()


class PatientDoctorMapping(TimeStampedModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='doctor_links')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='patient_links')
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assigned_mappings')
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('patient', 'doctor')
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.patient} -> {self.doctor}"
