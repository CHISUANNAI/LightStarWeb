from django.contrib import admin

# Register your models here.
from django.contrib import admin
from . import user_data_models

admin.site.register(user_data_models.User)
admin.site.register(user_data_models.Sick_children)
admin.site.register(user_data_models.parent_children)
