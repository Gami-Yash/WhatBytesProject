
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from medical.views import (
    DoctorViewSet,
    PatientDoctorMappingViewSet,
    PatientMappingByPatientView,
    PatientViewSet,
)

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'mappings', PatientDoctorMappingViewSet, basename='patient-doctor-mapping')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/mappings/patient/<int:patient_id>/', PatientMappingByPatientView.as_view(), name='patient-mapping-by-patient'),
    path('api/', include(router.urls)),
]
