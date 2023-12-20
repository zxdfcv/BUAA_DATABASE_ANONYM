from rest_framework.permissions import BasePermission


class HasLoginLogVDPermission(BasePermission):
    def has_permission(self, request, view):
        has_permission = (
                request.user.has_perm('myapp.view_loginlog') and
                request.user.has_perm('myapp.delete_loginlog'))
        return request.user.is_staff or has_permission


class HasOpLogVDPermission(BasePermission):
    def has_permission(self, request, view):
        has_permission = (
                request.user.has_perm('myapp.view_oplog') and
                request.user.has_perm('myapp.delete_oplog'))
        return request.user.is_staff or has_permission


class HasErrorLogVDPermission(BasePermission):
    def has_permission(self, request, view):
        has_permission = (
                request.user.has_perm('myapp.view_errorlog') and
                request.user.has_perm('myapp.delete_errorlog'))
        return request.user.is_staff or has_permission


class CanEditUserPermission(BasePermission):
    def has_permission(self, request, view):
        is_self = str(request.user.id) == request.GET.get('user_id', '')
        has_permission = (
                request.user.has_perm('myapp.change_user') and
                request.user.has_perm('myapp.delete_user') and
                request.user.has_perm('myapp.view_user'))
        return (request.user.is_staff or has_permission) and is_self

    # username_param = view.kwargs.get('username')  # 假设用户名是从 URL 参数中获取的
    #
    # # 获取请求中的用户对象
    # try:
    #     user = get_user_model().objects.get(username=username_param)
    # except get_user_model().DoesNotExist:
    #     return False  # 用户不存在，拒绝权限
    #
    # # 检查权限
    # is_admin_or_self = request.user.is_staff or str(request.user.id) == str(user.id)
    # has_permission = (
    #         request.user.has_perm('myapp.change_user') and
    #         request.user.has_perm('myapp.delete_user') and
    #         request.user.has_perm('myapp.view_errorlog')
    # )
    #
    # return is_admin_or_self and has_permission


class CanViewClassificationPermission(BasePermission):
    def has_permission(self, request, view):
        has_permission = (
                request.user.has_perm('myapp.view_classification1') and
                request.user.has_perm('myapp.view_classification2'))
        return request.user.is_staff or has_permission


class CanFollowPermission(BasePermission):
    def has_permission(self, request, view):
        has_permission = (
                request.user.has_perm('myapp.add_follow') and
                request.user.has_perm('myapp.delete_follow'))
        return request.user.is_staff or has_permission


class CanEditProductPermission(BasePermission):
    def has_permission(self, request, view):
        is_self = str(request.user.id) == request.data.get('merchant', '')
        has_permission = (
                request.user.has_perm('myapp.add_product') and
                request.user.has_perm('myapp.change_product') and
                request.user.has_perm('myapp.delete_product') and
                request.user.has_perm('myapp.view_product'))
        return (request.user.is_staff or has_permission) and is_self


class CanEditCommentPermission(BasePermission):
    def has_permission(self, request, view):
        has_permission = (
                request.user.has_perm('myapp.add_comment') and
                request.user.has_perm('myapp.delete_comment')
                and request.user.has_perm('myapp.view_comment')
        )
        return request.user.is_staff or has_permission


class CanEditReplyPermission(BasePermission):
    def has_permission(self, request, view):
        has_permission = (
                request.user.has_perm('myapp.add_reply') and
                request.user.has_perm('myapp.delete_reply')
                and request.user.has_perm('myapp.view_reply')
        )
        return request.user.is_staff or has_permission


class CanBuyPermission(BasePermission):
    def has_permission(self, request, view):
        has_permission = (
                request.user.has_perm('myapp.add_order') and
                request.user.has_perm('myapp.change_order')
                and request.user.has_perm('myapp.view_order')
                and request.user.has_perm('myapp.delete_order')
        )
        return request.user.is_staff or has_permission
