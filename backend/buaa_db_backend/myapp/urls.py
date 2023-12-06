from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import user, log, admin, classification, product, comment

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

    path("user/detail", user.UserDetailView.as_view(), name="user_information"),
    path("user/update", user.EditUserView.as_view(), name="user_update"),
    path("user/delete", user.EditUserView.as_view(), name="user_delete"),
    path("user/update/pwd", user.UserChangePasswordView.as_view(), name="user_changePwd"),
    path("user/follow/followers", user.FollowerListView.as_view(), name="follower_list"),
    path("user/follow/add", user.EditFollowerView.as_view(), name="follower_add"),
    path("user/follow/delete", user.EditFollowerView.as_view(), name="follower_delete"),
    path("user/follow/followings", user.FollowingListView.as_view(), name="following_list"),

    path("admin/user/detail", admin.UserAllDetailView.as_view(), name="user_allInformation"),
    path("admin/user/update", admin.UserAllDetailView.as_view(), name="user_allUpdate"),
    path("admin/user/list", admin.UserListView.as_view(), name="user_list"),
    path("admin/user/delete", admin.UserListView.as_view(), name="user_allDelete"),
    path("admin/product/list", admin.ProductDetailListView.as_view(), name="product_allList"),
    path("admin/product/create", admin.EditProductDetailView.as_view(), name="product_allCreate"),
    path("admin/product/update", admin.EditProductDetailView.as_view(), name="product_allUpdate"),
    path("admin/product/delete", admin.EditProductDetailView.as_view(), name="product_allDelete"),
    path("admin/comment/list", admin.CommentView.as_view(), name="comment_allList"),
    path("admin/comment/create", admin.CommentView.as_view(), name="comment_allCreate"),
    path("admin/comment/update", admin.CommentView.as_view(), name="comment_allUpdate"),
    path("admin/comment/delete", admin.CommentView.as_view(), name="comment_allDelete"),

    path("admin/statistics", admin.StatisticsView.as_view(), name="statistics"),

    path("classification/viewC_1", classification.Classification1ListView.as_view(), name="classification1_view"),
    path("classification/viewC_2", classification.Classification2ListView.as_view(), name="classification2_view"),
    path("classification/createC_1", classification.EditClassification1View.as_view(), name="classification1_create"),
    path("classification/createC_2", classification.EditClassification2View.as_view(), name="classification2_create"),
    path("classification/updateC_1", classification.EditClassification1View.as_view(), name="classification1_update"),
    path("classification/updateC_2", classification.EditClassification2View.as_view(), name="classification2_update"),
    path("classification/deleteC_1", classification.EditClassification1View.as_view(), name="classification1_delete"),
    path("classification/deleteC_2", classification.EditClassification2View.as_view(), name="classification2_delete"),

    path("product/list", product.ProductWithImagesView.as_view(), name='product_list'),
    path("product/create", product.EditProductView.as_view(), name='product_create'),
    path("product/update", product.EditProductView.as_view(), name='product_update'),
    path("product/delete", product.EditProductView.as_view(), name='product_delete'),
    path("product/detail", product.ProductDetailView.as_view(), name='product_detail'),
    path("product/collector/list", product.EditProductCollectorView.as_view(), name='collector_list'),
    path("product/collector/add", product.EditProductCollectorView.as_view(), name='collector_add'),
    path("product/collector/remove", product.EditProductCollectorView.as_view(), name='collector_remove'),

    path("comment/list", comment.CommentListView.as_view(), name='comment_list'),
    path("comment/my_list", comment.MyCommentsView.as_view(), name='comment_my_list'),
    path("comment/create", comment.MyCommentsView.as_view(), name='comment_create'),
    path("comment/delete", comment.MyCommentsView.as_view(), name='comment_delete'),
    path("comment/notice", comment.CommentNoticeView.as_view(), name='comment_notice'),
    path("comment/read", comment.CommentNoticeView.as_view(), name='comment_read'),
    path("comment/like", comment.EditLikesView.as_view(), name='comment_like'),
    path("comment/dislike", comment.EditLikesView.as_view(), name='comment_dislike'),

    path("test/", user.TestView.as_view(), name="token_test"),
]
