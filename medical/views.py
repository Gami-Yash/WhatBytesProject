"""REST views for medical resources."""

from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Doctor, Patient, PatientDoctorMapping
from .serializers import (
    DoctorSerializer,
    PatientDoctorMappingSerializer,
    PatientSerializer,
)


class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Patient.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.owner != self.request.user:
            raise PermissionDenied('You do not have permission to update this patient.')
        serializer.save()

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied('You do not have permission to delete this patient.')
        instance.delete()
        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Patient deleted successfully"},
            status=status.HTTP_200_OK
        )


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Doctor deleted successfully"},
            status=status.HTTP_200_OK
        )


class PatientDoctorMappingViewSet(viewsets.ModelViewSet):
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PatientDoctorMapping.objects.filter(patient__owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.patient.owner != self.request.user:
            raise PermissionDenied('You do not have permission to update this mapping.')
        serializer.save()

    def perform_destroy(self, instance):
        if instance.patient.owner != self.request.user:
            raise PermissionDenied('You do not have permission to modify this mapping.')
        instance.delete()


class PatientMappingByPatientView(ListAPIView):
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        return PatientDoctorMapping.objects.filter(patient__owner=self.request.user, patient_id=patient_id)
