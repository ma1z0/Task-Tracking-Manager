from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrAssigneeLimited(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        if request.user == obj.owner:
            return True
        
        if request.user == obj.assignee and request.method == "PATCH":
            return True
        
        return False