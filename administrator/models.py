from django.db import models
from django.contrib import admin


# Create your models here.

class Administrator(models.Model):
    用户ID = models.CharField('用户ID', primary_key=True, max_length=100)
    密码 = models.CharField('密码', null=True, max_length=200)

    class Meta:
        db_table = '管理员表'


object = Administrator()
admin.site.register(Administrator)