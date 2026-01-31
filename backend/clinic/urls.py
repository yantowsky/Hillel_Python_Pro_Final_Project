from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api import AppointmentViewSet, DoctorViewSet

router = DefaultRouter()
router.register("doctors", DoctorViewSet, basename="doctors")
router.register("appointments", AppointmentViewSet, basename="appointments")

urlpatterns = [
    path("", include(router.urls)),
]
