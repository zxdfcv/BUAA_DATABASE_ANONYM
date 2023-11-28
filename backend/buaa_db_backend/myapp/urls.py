from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import user, log, admin

app_name = 'myapp'
urlpatterns = [
    path('login/', user.LoginView.as_view(), name='token_obtain_pair'),
    path('register/', user.RegistrationView.as_view(), name='user_register'),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),

    path("log/login/", log.LoginLogView.as_view(), name="loginLog_list"),
    path("log/login/delete", log.LoginLogView.as_view(), name="loginLog_delete"),
    path("log/op/", log.OpLogView.as_view(), name="opLog_list"),
    path("log/op/delete", log.OpLogView.as_view(), name="opLog_delete"),
    path("log/error/", log.ErrorLogView.as_view(), name="errorLog_list"),
    path("log/error/delete", log.ErrorLogView.as_view(), name="errorLog_delete"),

    path("user/detail", user.EditUserView.as_view(), name="user_information"),
    path("user/update", user.EditUserView.as_view(), name="user_update"),
    path("user/delete", user.EditUserView.as_view(), name="user_delete"),
    path("user/update/pwd", user.UserChangePasswordView.as_view(), name="user_changePwd"),


    path("admin/user/detail", admin.UserAllDetailView.as_view(), name="user_allInformation"),
    path("admin/user/update", admin.UserAllDetailView.as_view(), name="user_allUpdate"),
    path("admin/user/list", admin.UserListView.as_view(), name="user_list"),
    path("admin/user/delete", admin.UserListView.as_view(), name="user_allDelete"),


    path("test/", user.TestView.as_view(), name="token_test"),
]
