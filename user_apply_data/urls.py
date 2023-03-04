from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from BBS import comment, views
from charity_sale import views
from user_apply_data import views


urlpatterns = [
   
   path('my_thumb',views.my_thumb),
   path('my_collection',views.my_collection),
   path('my_post',views.my_post),
   path('my_comment_reply',views.my_comment_reply),
   path('my_item_forsale',views.my_item_forsale),
   path('my_registered_actitity',views.my_registered_actitity),
   path('my_set_actitity',views.my_set_actitity),
   #path('upload_headpicture',views.upload_headpicture),
   #path('upload_identifypicture',views.upload_identifypicture),
   #path('upload_child_identifypicture',views.upload_child_identifypicture),
   path('edit_my_information',views.edit_my_information),
   path('parent_identify',views.parent_identify),
   path('get_parent_identify',views.get_parent_identify),
   path('get_edit_my_item',views.get_edit_my_item),
   path('get_volunteer_identify',views.get_volunteer_identify),
   path('volunteer_identify',views.volunteer_identify),
   path('get_organization_identify',views.get_organization_identify),
   path('organization_identify',views.organization_identify),
   path('get_volunteer_information',views.get_volunteer_information),
   path('openmine', views.openmine)
  
   
   
  
  
   
]
