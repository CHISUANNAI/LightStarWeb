# Generated by Django 3.2.5 on 2021-08-04 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('用户ID', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='用户ID')),
                ('密码', models.CharField(max_length=200, null=True, verbose_name='密码')),
            ],
            options={
                'db_table': '管理员表',
            },
        ),
    ]
