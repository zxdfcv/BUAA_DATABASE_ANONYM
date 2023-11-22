from rest_framework.permissions import BasePermission


class HasLoginLogVDPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('myapp.view_loginlog') and request.user.has_perm('myapp.delete_loginlog')


class HasOpLogVDPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('myapp.view_oplog') and request.user.has_perm('myapp.delete_oplog')


class HasErrorLogVDPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('myapp.view_errorlog') and request.user.has_perm('myapp.delete_errorlog')
