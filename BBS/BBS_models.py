from django.db import models
from django.contrib import admin
import user_data.user_data_models as ud


# ！帖子(帖子标题,发帖时间,发贴用户,论坛分区,内容,点赞数,收藏数,浏览次数,是否审核通过)
class Bbsdata(models.Model):
    帖子标题 = models.CharField('帖子标题', primary_key=True, max_length=254)
    帖子内容 = models.TextField('帖子内容', null=True, max_length=9999999)
    发帖时间 = models.DateTimeField('发贴时间', null=True)
    用户 = models.ForeignKey(ud.User,on_delete=models.PROTECT)
    论坛分区 = models.CharField('论坛分区', null=True, max_length=88)
    点赞数 = models.IntegerField('点赞数', null=False, default=0)
    收藏数 = models.IntegerField('收藏数', null=False, default=0)
    浏览次数 = models.IntegerField('浏览次数', null=False, default=0)
    是否审核通过 = models.BooleanField('是否审核通过', null=False, default=0)

    class Meta:
        db_table = 'BBS数据'


# ！帖子评论(帖子标题,评论号,评论用户,评论内容,评论时间)
class Comment_data(models.Model):
    帖子标题 = models.ForeignKey(Bbsdata,on_delete=models.PROTECT)
    楼数 = models.IntegerField('楼数', )
    用户 = models.ForeignKey(ud.User,on_delete=models.PROTECT)
    评论内容 = models.TextField('评论内容', null=True, max_length=9999999)
    评论时间 = models.DateTimeField('评论时间', null=True)

    class Meta:
        db_table = '帖子评论'
        unique_together = (("帖子标题", "楼数"),)


# ！评论回复(帖子标题,上级评论号,评论号,评论用户,评论内容,评论时间)
class Reply_data(models.Model):
    回复的评论 = models.ForeignKey(Comment_data,on_delete=models.PROTECT)
    评论号 = models.IntegerField('评论号', null=True)
    用户 = models.ForeignKey(ud.User,on_delete=models.PROTECT)
    评论内容 = models.TextField('评论内容', null=True, max_length=9999999)
    评论时间 = models.DateTimeField('评论时间', null=True)

    class Meta:
        db_table = '评论回复'
        unique_together = (("回复的评论", "评论号"),)

class Report_post(models.Model):
    帖子标题 = models.ForeignKey(Bbsdata,on_delete=models.PROTECT)
    举报用户 = models.ForeignKey(ud.User,on_delete=models.PROTECT)
    举报时间=models.DateTimeField('举报时间', null=True)
    举报理由 = models.TextField('举报理由', null=True, max_length=9999999)
    是否审核通过 = models.BooleanField('是否审核通过', null=False, default=0)

    class Meta:
        db_table = '用户举报'
        unique_together = (("帖子标题", "举报用户"),)


admin.site.register(Reply_data)
admin.site.register(Report_post)
admin.site.register(Bbsdata)
