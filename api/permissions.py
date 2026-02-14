from rest_framework import permissions

class IsAdminOrRektor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_superuser or request.user.role in ['admin', 'rektor'])

class IsAdminOrRektorOrDepartment(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow read/write for admin/rektor
        if request.user.is_superuser or request.user.role in ['admin', 'rektor']:
            return True
        # For others, permissions might be more granular, handled in views
        return request.user.is_authenticated
