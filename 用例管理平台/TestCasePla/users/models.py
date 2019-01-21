from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Userpro(AbstractUser):
    loginName = models.CharField(max_length=30, verbose_name="登录名")

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.loginName