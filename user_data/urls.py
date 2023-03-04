from django.urls import path, re_path

from user_data.views import get, check_username,check_mobile_view,register,logintest,logout,index,registerP,registerO,getV,getP,getO
urlpatterns = [
    path('', index),
    path('logout/',logout),
    path('login/', get),  # 该url进入志愿者登录注册的主页面
    path('username/', check_username),  # 该url控制注册的时候userID是否被占用
    path('mobile/', check_mobile_view),  # 该url控制注册的时候该手机号是否被占用
    path('login/success/', logintest),  # 该url是在登录注册页面 点击登录按钮之后测试用户名和密码是否匹配
    # path('login/Volunteer/register/', get2),  # 该url是登录注册页面 点击注册按钮之后进入 志愿者注册页面
    path('registerV/success/', register),  # 该url是 点注册按钮之后测试注册是否成功
    path('registerP/success/', registerP),
    path('registerO/success/', registerO),
    path('registerV/', getV),
    path('registerP/', getP),
    path('registerO/', getO)
]

