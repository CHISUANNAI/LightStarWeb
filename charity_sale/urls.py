from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from BBS import comment, views
from charity_sale import views



urlpatterns = [
   path('open_sale',views.open_sale),
   path('findimage',views.findimage), 
   path('additem',views.additem), 
   path('alteritem',views.alteritem), 
   path('list_all_items',views.list_all_items), 
   path('my_item',views.my_item), 
   path('edit_my_item',views.edit_my_item),
 
]
