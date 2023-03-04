from django.db import models
import user_data.user_data_models as ud
from django.contrib import admin


# !活动表(活动id，活动名称，活动日期，活动地点，社会组织，活动简介，活动详细介绍）
class Activity(models.Model):
    活动id = models.CharField('活动id', primary_key=True, max_length=5)
    活动标题 = models.CharField('活动标题', null=True, max_length=200)
    活动名称 = models.CharField('活动名称', null=True, max_length=200)
    活动日期 = models.DateField('活动日期', null=True)
    活动地点 = models.CharField('活动地点', null=True, max_length=200)
    社会组织 = models.CharField('社会组织', null=True, max_length=200)
    活动简介 = models.TextField('活动简介', null=True, max_length=9999999)
    活动详细介绍 = models.TextField('活动详细介绍', null=True, max_length=9999999)

    class Meta:
        db_table = '活动表'


object = Activity()


# !活动图片表(活动id，活动图片)
class ActivityPicture(models.Model):
    活动 = models.ForeignKey(Activity, on_delete=models.PROTECT)
    活动图片 = models.ImageField('活动图片', null=False, upload_to="picture", height_field='url_height',
                             width_field='url_width')
    url_height = models.PositiveIntegerField(default=75)
    url_width = models.PositiveIntegerField(default=75)

    class Meta:
        db_table = '活动图片表'
        unique_together = (("活动", "活动图片"),)


object = ActivityPicture()


# !发起活动表(发起活动名称，发起活动日期，发起活动地点，发起活动简介，报名截止日期，社会组织id)
class SetActivity(models.Model):
    发起活动名称 = models.CharField('发起活动名称', primary_key=True, max_length=200)
    发起活动日期 = models.DateField('发起活动日期', null=True)
    发起活动地点 = models.CharField('发起活动地点', null=True, max_length=200)
    发起活动简介 = models.TextField('发起活动简介', null=True, max_length=9999999)
    报名截止日期 = models.DateField('报名截止日期', null=True)
    组织类用户 = models.ForeignKey(ud.User, on_delete=models.PROTECT)
    是否通过审核 = models.BooleanField('是否通过审核',null=True,blank=True,default=0)

    class Meta:
        db_table = '发起活动表'
object = SetActivity()

# !发起活动图片表(活动id，活动图片)
class SetActivityPicture(models.Model):
    活动 = models.ForeignKey(SetActivity, on_delete=models.PROTECT)
    活动图片 = models.ImageField('活动图片', null=False, upload_to="picture", height_field='url_height',
                             width_field='url_width')
    url_height = models.PositiveIntegerField(default=75)
    url_width = models.PositiveIntegerField(default=75)

    class Meta:
        db_table = '发起活动图片表'
        unique_together = (("活动", "活动图片"),)

object = SetActivityPicture()

admin.site.register(Activity)
admin.site.register(ActivityPicture)
admin.site.register(SetActivity)
admin.site.register(SetActivityPicture)
