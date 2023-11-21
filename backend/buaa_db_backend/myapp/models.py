from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    # 需要添加用户评价系统吗？
    GENDER_CHOICES = [
        ('M', '男'),
        ('F', '女'),
        ('O', 'Other'),
    ]
    phone = models.CharField(max_length=13, null=True, blank=True, unique=True)
    nickname = models.CharField(verbose_name="昵称", max_length=36, null=True, blank=True)
    gender = models.CharField(verbose_name="性别", max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    avatar = models.FileField(verbose_name="头像", upload_to='avatar/', null=True, blank=True)
    description = models.TextField(verbose_name="个人简介", max_length=120, null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = "buaa_db_user"
        verbose_name = "用户"


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower} follows {self.following}"

    class Meta:
        db_table = "buaa_db_follow"
        verbose_name = "关注"


class Classification1(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "buaa_db_classification_1"
        verbose_name = "一级分类"


class Classification2(models.Model):
    name = models.CharField(max_length=255, unique=True)
    classification_1 = models.ForeignKey(Classification1, on_delete=models.CASCADE, related_name='c1_c2')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "buaa_db_classification_2"
        verbose_name = "二级分类"


class Product(models.Model):
    STATUS_CHOICES = [
        ('A', '全新'),
        ('B', '几乎全新'),
        ('C', '轻微使用痕迹'),
        ('D', '明显使用痕迹'),
        ('E', '有一定问题'),
    ]
    ADDR_CHOICES = [
        ('1', '学院路校区'),
        ('2', '沙河校区'),
        ('3', '两校区均可')
    ]
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    merchant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_product')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, blank=True, null=True)
    addr = models.CharField(max_length=1, choices=ADDR_CHOICES)
    classification_1 = models.ForeignKey(Classification1, on_delete=models.CASCADE, related_name='c1_product')
    classification_2 = models.ForeignKey(Classification2, on_delete=models.CASCADE, related_name='c2_product')
    description = models.TextField(max_length=1000, blank=True, null=True)
    video = models.FileField(upload_to='product_videos/', null=True, blank=True)
    views = models.IntegerField(default=0)
    wants = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    collectors = models.ManyToManyField(User, blank=True, related_name='商品收藏')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "buaa_db_product"
        verbose_name = "商品"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_image')
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f'{self.product.name} - {self.id}'

    class Meta:
        db_table = "buaa_db_product_image"
        verbose_name = "商品图片"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_comment')
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    like_count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user} - {self.product} - {self.created_at}'

    class Meta:
        db_table = "buaa_db_comment"
        verbose_name = "商品评论"


class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reply')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_reply')
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    like_count = models.IntegerField(default=0)

    mentioned_users = models.ManyToManyField(User, blank=True, related_name='被回复')

    def __str__(self):
        return f'{self.user} - {self.comment.product} - {self.created_at}'

    class Meta:
        db_table = "buaa_db_reply"
        verbose_name = "评论回复"


class LoginLog(models.Model):
    username = models.CharField(max_length=50, blank=True, null=True)
    ip = models.CharField(max_length=100, blank=True, null=True)
    ua = models.CharField(max_length=200, blank=True, null=True)
    log_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.username} - {self.ip} - {self.log_time}'

    class Meta:
        db_table = "buaa_db_login_log"
        verbose_name = "登入日志"


class OpLog(models.Model):
    re_ip = models.CharField(max_length=100, blank=True, null=True)
    re_time = models.DateTimeField(auto_now_add=True, null=True)
    re_url = models.CharField(max_length=200, blank=True, null=True)
    re_method = models.CharField(max_length=10, blank=True, null=True)
    re_content = models.CharField(max_length=200, blank=True, null=True)
    access_time = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f'{self.re_ip} - {self.re_url} - {self.re_time}'

    class Meta:
        db_table = "buaa_db_op_log"
        verbose_name = "操作日志"


class ErrorLog(models.Model):
    ip = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    method = models.CharField(max_length=10, blank=True, null=True)
    content = models.CharField(max_length=200, blank=True, null=True)
    log_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.ip} - {self.url} - {self.log_time}'

    class Meta:
        db_table = "buaa_db_error_log"
        verbose_name = "错误日志"
