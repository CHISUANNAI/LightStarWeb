from django.urls import path, re_path

from Activity.views import showact, showdetail, showsetact,addsetact,showall,apply,listact
urlpatterns = [

    path('', showact),  # 该url进入活动页面
 #   path('list/', dispatcher),
  #  path('pic/', show),
    path('showarticle/', showdetail), # 该url点击不同侧边栏 显示不同的活动详情(除图片外）
   # path('showarticle/', showpic),
   # path('showpic/', showpic),
    path('showsetact', showsetact),# 该url点击进入发起活动页面
    path('addsetact/',addsetact),  #该url 发起活动加入后台数据库(等待审核)
    path('showall/',showall) ,#该url 点击显示全部 显示代办活动的全部
    path('showall/success/',listact),
  #  path('testname',testname)
    path('showall/apply/',apply) #该url 是用户报名活动
]
