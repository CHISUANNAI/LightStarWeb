from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin
from BBS import comment, views
from charity_sale import views
from administrator import views
from administrator.views import loginadmin, logintest, jumpindex, jumpuser, listVP, listVPpass, listO, listOpass, \
    jumporg, jumpchild, listchild, listchildpass, cal1, cal2, cal3, cal4, cal5, cal6

urlpatterns = [

    path('', loginadmin),  # 该url先进入管理员登录界面
    path('admin/', logintest),  # 该Url登录后进入首页进行管理
    path('admin/success/', jumpindex),  # 该url登录成功后进入管理员首页
    path('admin/success/user', jumpuser),  # 该url登录成功后进入用户认证管理页
    path('admin/success/user/listVP', listVP),  # 该url列出上传照片需要认证的用户
    path('admin/success/user/listVP/pass/', listVPpass),  # 该url通过身份认证
    path('admin/success/org', jumporg),  # 该url进入组织认证管理页
    path('admin/success/org/listO', listO),  # 该url列出需要认证的组织
    path('admin/success/org/listO/pass/', listOpass),  # 该url通过组织认证
    path('admin/success/child', jumpchild),  # 该url进入患病儿童管理页
    path('admin/success/child/listchild', listchild),  # 该url列出需要认证的患儿
    path('admin/success/child/listchild/pass/', listchildpass),  # 该url通过患儿认证
    path('admin/success/cal1', cal1),  # 该url计算主页多少个患儿
    path('admin/success/cal2', cal2),  # 该url计算主页多少个组织
    path('admin/success/cal3', cal3),  # 该url计算主页多少个身份认证
    path('admin/success/cal4', cal4),  # 该url计算主页多少个帖子
    path('admin/success/cal5', cal5),  # 该url计算主页多少个活动
    path('admin/success/cal6', cal6),  # 该url计算主页多少个商品
    # 以下hanhan

    path('open_admin_activity', views.open_admin_activity),
    path('open_admin_bbs', views.open_admin_bbs),
    path('open_admin_shop', views.open_admin_shop),

    path('activity_before_audit', views.activity_before_audit),
    path('report_before_audit', views.report_before_audit),
    path('salesitem_before_audit', views.salesitem_before_audit),

    path('audit_activity', views.audit_activity),
    path('audit_post', views.audit_post),
    path('audit_salesitem', views.audit_salesitem)

]
