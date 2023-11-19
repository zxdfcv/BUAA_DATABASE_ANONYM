from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import user

app_name = 'myapp'
urlpatterns = [
    path('login/', user.LoginView.as_view(), name='token_obtain_pair'),
    path('register/', user.RegistrationView.as_view(), name='user_register'),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),

    path("test/", user.TestView.as_view(), name="token_test"),
]
