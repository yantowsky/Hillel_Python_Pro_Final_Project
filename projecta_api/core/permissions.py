from rest_framework.permissions import BasePermission

from accounts.models import User


class IsOwnerPatientOrOwnerDoctorOrAdmin(BasePermission):
    """
    Object-level permissions:
    - ADMIN: everything
    - PATIENT: obj.patient == user
    - DOCTOR: obj.doctor == user
    """

    def has_object_permission(self, request, view, obj) -> bool:
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if user.role == User.Role.ADMIN:
            return True

        if user.role == User.Role.PATIENT and getattr(obj, "patient_id", None) == user.id:
            return True

        if user.role == User.Role.DOCTOR and getattr(obj, "doctor_id", None) == user.id:
            return True

        return False