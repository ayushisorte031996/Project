from rest_framework.permissions import BasePermission
from .models import Organization

class IsSuperAdminOrAdminOnly(BasePermission):
    def has_permission(self, request, view):
        get_user = request.user.username
        if get_user.role == 'Super Admin':
            return True
        elif get_user.role == 'Admin':
            organization_id = view.kwargs.get('organization_id')
            if organization_id:
                organization = Organization.objects.get(id=organization_id)
                return organization.admin == request.user
        return False
