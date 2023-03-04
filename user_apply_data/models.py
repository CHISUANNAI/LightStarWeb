from django.db import models
import user_data.user_data_models as ud
import Activity.models as am
from BBS.BBS_models import Bbsdata


# ！用户收藏活动(用户ID[f],活动ID[f],收藏时间)

class User_collect_activity(models.Model):
    用户 = models.ForeignKey(ud.User, on_delete=models.PROTECT)
    活动 = models.ForeignKey(am.Activity, on_delete=models.PROTECT)
    收藏时间 = models.DateTimeField('收藏时间', null=True)

    class Meta:
        db_table = '用户收藏活动'
        unique_together = (("用户", "活动"),)


# ！用户点赞活动(用户ID[f],活动ID[f],点赞时间)

class User_thumb_activity(models.Model):
    用户 = models.ForeignKey(ud.User, on_delete=models.PROTECT)
    活动 = models.ForeignKey(am.Activity, on_delete=models.PROTECT)
    点赞时间 = models.DateTimeField('点赞时间', null=True)

    class Meta:
        db_table = '用户点赞活动'
        unique_together = (("用户", "活动"),)


# ！用户收藏帖子(用户ID[f],帖子标题[f],收藏时间)

class User_collect_post(models.Model):
    用户 = models.ForeignKey(ud.User, on_delete=models.PROTECT)
    帖子 = models.ForeignKey(Bbsdata, on_delete=models.PROTECT)
    收藏时间 = models.DateTimeField('收藏时间', null=True)

    class Meta:
        db_table = '用户收藏帖子'
        unique_together = (("用户", "帖子"),)


# ！用户点赞帖子(用户ID[f],帖子标题[f],点赞时间)
class User_thumb_post(models.Model):
    用户 = models.ForeignKey(ud.User, on_delete=models.PROTECT)
    帖子 = models.ForeignKey(Bbsdata, on_delete=models.PROTECT)
    点赞时间 = models.DateTimeField('点赞时间', null=True)

    class Meta:
        db_table = '用户点赞帖子'
        unique_together = (("用户", "帖子"),)


# !活动报名(用户ID[f],活动名称[f])

class Activity_registration(models.Model):
    用户 = models.ForeignKey(ud.User, on_delete=models.PROTECT)
    发起的活动 = models.ForeignKey(am.SetActivity, on_delete=models.PROTECT)

    class Meta:
        db_table = '活动报名'
        unique_together = (("用户", "发起的活动"),)


