from django.db import models
import user_data.user_data_models as ud
from django.contrib import admin
# Create your models here.
#义卖商品(商品编号,商品名,商品描述,用户ID,价格,是否已卖出)
#商品图片(商品编号[f]商品图片)
class Saleitems(models.Model):

    
    商品编号 = models.IntegerField('商品编号',primary_key=True)
    商品名 = models.CharField('商品名', null=True, max_length=109)
    商品描述 = models.TextField('商品描述', null=True, max_length=9999)
    所属家长_患儿 = models.ForeignKey(ud.parent_children,on_delete=models.PROTECT)
    是否已卖出 = models.BooleanField('是否已卖出', null=False, default=0)
    价格=models.IntegerField("价格",null=True,)
    发布日期=models.DateField("发布日期",null=True)
    class Meta:
        db_table = '义卖商品'

#商品图片(商品编号[f]商品图片)
class ItemImage(models.Model):
    
    商品= models.ForeignKey(Saleitems,on_delete=models.PROTECT)
    商品图片 = models.ImageField('商品图片', null=False, upload_to="picture", height_field='url_height',width_field='url_width')
    url_height = models.PositiveIntegerField(default=75)
    url_width = models.PositiveIntegerField(default=75)

    class Meta:
        db_table = '商品图片'
        unique_together = (("商品", "商品图片"),)
    
admin.site.register(ItemImage)
admin.site.register(Saleitems)
