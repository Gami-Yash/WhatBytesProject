"""Serializers for the medical domain models."""

from rest_framework import serializers

from .models import Doctor, Patient, PatientDoctorMapping


class PatientSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Patient
        fields = (
            'id',
            'owner',
            'first_name',
            'last_name',
            'date_of_birth',
            'gender',
            'medical_history',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'owner', 'created_at', 'updated_at')


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = (
            'id',
            'first_name',
            'last_name',
            'specialization',
            'email',
            'phone_number',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    assigned_by = serializers.StringRelatedField(read_only=True)
    patient_id = serializers.PrimaryKeyRelatedField(source='patient', queryset=Patient.objects.all(), write_only=True)
    doctor_id = serializers.PrimaryKeyRelatedField(source='doctor', queryset=Doctor.objects.all(), write_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = (
            'id',
            'patient',
            'doctor',
            'patient_id',
            'doctor_id',
            'assigned_by',
            'notes',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'patient', 'doctor', 'assigned_by', 'created_at', 'updated_at')

    def validate(self, attrs):
        patient = attrs.get('patient') or getattr(self.instance, 'patient', None)
        request = self.context.get('request')
        if request and patient and patient.owner != request.user:
            raise serializers.ValidationError('You can only map doctors to your own patients.')
        return super().validate(attrs)
