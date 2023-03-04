from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from BBS import comment, views



urlpatterns = [
   # path('list_BBS_content/',views.dispatcher)
   path("show_post_html",views.show_post_html),
   path('list_BBS_content',views.dispatcher),
   path('comment',comment.dispatcher),
   path("open_post",views.open_post,name='open_post'),
   path("list_catalog_post",views.list_catalog_post),
   
]
