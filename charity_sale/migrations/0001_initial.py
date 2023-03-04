# Generated by Django 3.2.5 on 2021-08-04 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_data', '0003_auto_20210804_1634'),
    ]

    operations = [
        migrations.CreateModel(
            name='Saleitems',
            fields=[
                ('商品编号', models.IntegerField(primary_key=True, serialize=False, verbose_name='商品编号')),
                ('商品名', models.CharField(max_length=109, null=True, verbose_name='商品名')),
                ('商品描述', models.TextField(max_length=9999, null=True, verbose_name='商品描述')),
                ('是否已卖出', models.BooleanField(default=0, verbose_name='是否已卖出')),
                ('价格', models.IntegerField(null=True, verbose_name='价格')),
                ('发布日期', models.DateField(null=True, verbose_name='发布日期')),
                ('所属家长_患儿', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='user_data.parent_children')),
            ],
            options={
                'db_table': '义卖商品',
            },
        ),
        migrations.CreateModel(
            name='ItemImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('商品图片', models.ImageField(height_field='url_height', upload_to='picture', verbose_name='商品图片', width_field='url_width')),
                ('url_height', models.PositiveIntegerField(default=75)),
                ('url_width', models.PositiveIntegerField(default=75)),
                ('商品', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='charity_sale.saleitems')),
            ],
            options={
                'db_table': '商品图片',
                'unique_together': {('商品', '商品图片')},
            },
        ),
    ]