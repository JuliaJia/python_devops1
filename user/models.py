from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class UserProfile(AbstractUser):
    class Meta:
        db_table = 'auth_user'
        verbose_name = "用户详细信息"
    phone = models.CharField(max_length=32, verbose_name="电话号码", null=True, blank=True)