from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import user, log, admin, classification

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


    path("classification/viewC_1", classification.Classification1ListView.as_view(), name="classification1_view"),
    path("classification/viewC_2", classification.Classification2ListView.as_view(), name="classification2_view"),
    path("classification/createC_1", classification.EditClassification1View.as_view(), name="classification1_create"),
    path("classification/createC_2", classification.EditClassification2View.as_view(), name="classification2_create"),
    path("classification/updateC_1", classification.EditClassification1View.as_view(), name="classification1_update"),
    path("classification/updateC_2", classification.EditClassification2View.as_view(), name="classification2_update"),
    path("classification/deleteC_1", classification.EditClassification1View.as_view(), name="classification1_delete"),
    path("classification/deleteC_2", classification.EditClassification2View.as_view(), name="classification2_delete"),



    path("test/", user.TestView.as_view(), name="token_test"),
]
