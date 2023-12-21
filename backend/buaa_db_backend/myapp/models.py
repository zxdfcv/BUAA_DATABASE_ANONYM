from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    # 需要添加用户评价系统吗？
    GENDER_CHOICES = [
        ('M', '男'),
        ('F', '女'),
        ('O', '未知'),
    ]
    phone = models.CharField(max_length=13, null=True, blank=True)
    nickname = models.CharField(verbose_name="昵称", max_length=36, null=True, blank=True)
    gender = models.CharField(verbose_name="性别", max_length=1, choices=GENDER_CHOICES, blank=True, null=True,
                              default='O')
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
    create_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.follower} follows {self.following}"

    class Meta:
        db_table = "buaa_db_follow"
        verbose_name = "关注"


class Classification1(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image = models.FileField(upload_to='c1_images/', null=True, blank=True)
    description = models.TextField(max_length=1000, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "buaa_db_classification_1"
        verbose_name = "一级分类"


class Classification2(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image = models.FileField(upload_to='c2_images/', null=True, blank=True)
    classification_1 = models.ForeignKey(Classification1, on_delete=models.CASCADE, related_name='c1_c2')
    description = models.TextField(max_length=1000, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True, null=True)

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

    off_shelve = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    wants = models.IntegerField(default=0)
    is_sold = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True, null=True)

    collectors = models.ManyToManyField(User, blank=True, related_name='collect_products')

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
    # TYPE_CHOICES = [
    #     ('0', '评论区留言'),
    #     ('1', '私聊'),
    # ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_comment')
    # type = models.CharField(max_length=1, choices=TYPE_CHOICES, default=0)
    content = models.TextField(max_length=1023)
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    # like_count = models.IntegerField(default=0)
    reply_count = models.IntegerField(default=0)
    is_read = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, blank=True, related_name='like_reply')

    def __str__(self):
        return f'{self.user} - {self.product} - {self.create_time}'

    class Meta:
        db_table = "buaa_db_comment"
        verbose_name = "商品评论"


class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reply')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_reply')
    content = models.TextField(max_length=1023)
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    # like_count = models.IntegerField(default=0)
    is_read = models.BooleanField(default=False)
    comment_read = models.BooleanField(default=False)

    mentioned_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentioned_reply', blank=True,
                                       null=True)
    likes = models.ManyToManyField(User, blank=True, related_name='like_comment')

    def __str__(self):
        return f'{self.user} - {self.comment.product} - {self.create_time}'

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


class Order(models.Model):
    STATUS_CHOICES = [
        ('0', '未支付'),
        ('1', '已经支付'),
        ('2', '订单取消')
    ]
    order_number = models.CharField(max_length=64, verbose_name="订单号")
    merchant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='merchant_order')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver_order')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_order')
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=0)
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    pay_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "buaa_db_order"
        verbose_name = "订单"


class Chat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_chat')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient_chat')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_chat')
    content = models.TextField(max_length=1023)
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    image = models.ImageField(upload_to='chat_images/',null=True, blank=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender} - {self.recipient} - {self.create_time}'

    class Meta:
        db_table = "buaa_db_chat"
        verbose_name = "私聊评论"
