from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AppointmentViewSet, MedicalRecordViewSet

router = DefaultRouter()
router.register("appointments", AppointmentViewSet, basename="appointments")
router.register("medical-records", MedicalRecordViewSet, basename="medical-records")

urlpatterns = [
    path("", include(router.urls)),
]