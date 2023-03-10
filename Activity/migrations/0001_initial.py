# Generated by Django 3.2.5 on 2021-07-26 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('活动id', models.CharField(max_length=5, primary_key=True, serialize=False, verbose_name='活动id')),
                ('活动标题', models.CharField(max_length=200, null=True, verbose_name='活动标题')),
                ('活动名称', models.CharField(max_length=200, null=True, verbose_name='活动名称')),
                ('活动日期', models.DateField(null=True, verbose_name='活动日期')),
                ('活动地点', models.CharField(max_length=200, null=True, verbose_name='活动地点')),
                ('社会组织', models.CharField(max_length=200, null=True, verbose_name='社会组织')),
                ('活动简介', models.TextField(max_length=9999999, null=True, verbose_name='活动简介')),
                ('活动详细介绍', models.TextField(max_length=9999999, null=True, verbose_name='活动详细介绍')),
            ],
            options={
                'db_table': '活动表',
            },
        ),
        migrations.CreateModel(
            name='SetActivity',
            fields=[
                ('发起活动名称', models.CharField(max_length=200, primary_key=True, serialize=False, verbose_name='发起活动名称')),
                ('发起活动日期', models.DateField(null=True, verbose_name='发起活动日期')),
                ('发起活动地点', models.CharField(max_length=200, null=True, verbose_name='发起活动地点')),
                ('发起活动简介', models.TextField(max_length=9999999, null=True, verbose_name='发起活动简介')),
                ('报名截止日期', models.DateField(null=True, verbose_name='报名截止日期')),
                ('组织类用户', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='user_data.user')),
            ],
            options={
                'db_table': '发起活动表',
            },
        ),
        migrations.CreateModel(
            name='SetActivityPicture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('活动图片', models.ImageField(height_field='url_height', upload_to='picture', verbose_name='活动图片', width_field='url_width')),
                ('url_height', models.PositiveIntegerField(default=75)),
                ('url_width', models.PositiveIntegerField(default=75)),
                ('活动', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Activity.setactivity')),
            ],
            options={
                'db_table': '发起活动图片表',
                'unique_together': {('活动', '活动图片')},
            },
        ),
        migrations.CreateModel(
            name='ActivityPicture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('活动图片', models.ImageField(height_field='url_height', upload_to='picture', verbose_name='活动图片', width_field='url_width')),
                ('url_height', models.PositiveIntegerField(default=75)),
                ('url_width', models.PositiveIntegerField(default=75)),
                ('活动', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Activity.activity')),
            ],
            options={
                'db_table': '活动图片表',
                'unique_together': {('活动', '活动图片')},
            },
        ),
    ]
