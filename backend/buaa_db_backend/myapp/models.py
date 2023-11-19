from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    phone = models.CharField(max_length=13, null=True, blank=True, unique=True)
    nickname = models.CharField(verbose_name="昵称", max_length=36, null=True, blank=True)
    avatar = models.FileField(verbose_name="头像", upload_to='avatar/', null=True, blank=True)
    description = models.TextField(verbose_name="个人简介", max_length=120, null=True, blank=True)

    class Meta:
        db_table = "buaa_db_user"
        verbose_name = "用户"
