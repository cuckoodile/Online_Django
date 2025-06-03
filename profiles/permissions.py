from rest_framework.permissions import BasePermission

class IsAdminGroup(BasePermission):
    """
    Allows access only to users in the 'Admin' group.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.groups.filter(name='Admin').exists()

class IsCustomerGroup(BasePermission):
    """
    Allows access only to users in the 'Customer' group.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.groups.filter(name='Customer').exists()

class IsShipperGroup(BasePermission):
    """
    Allows access only to users in the 'Shipper/Logistic Partner' group.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.groups.filter(name='Shipper/Logistic Partner').exists()

class IsOrderTrackerGroup(BasePermission):
    """
    Allows access only to users in the 'Orders Tracker' group.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.groups.filter(name='Orders Tracker').exists()
