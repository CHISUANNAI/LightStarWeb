"""webxxdd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from user_data.views import index, logout,touxiang
from Activity.views import showact

urlpatterns = [
    path('admin/', admin.site.urls),
    path('webxxdd/',index),
    path('gettouxiang/',touxiang),
    path('user_data/', include('user_data.urls')),
    path('BBS/', include("BBS.urls")),
    path('Charity_sale/', include("charity_sale.urls")),
    path('user_apply_data/',include("user_apply_data.urls")),
    # path('index/', index),
    path('activity/', include('Activity.urls')),
    path('administrator/', include('administrator.urls')),  #等一下
    re_path(r'^media/(?P<path>.*)/$', serve, {"document_root": settings.MEDIA_ROOT})

    # path('logout/',logout)
] +static("/", document_root="./templates")
