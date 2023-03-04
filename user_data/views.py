from django.http import JsonResponse
from django.shortcuts import render, redirect
from user_data.user_data_models import User, Sick_children, parent_children


def get(request):
    """
        凡是来访问这个视图的请求, 就返回注册页面
        :param request: 请求注册页面
        :return: 注册页面
        """
    return render(request, 'login/load.html')
    # test2.html指的是返回志愿者登录+注册的页面


def getV(request):
    """
        凡是来访问这个视图的请求, 就返回注册页面
        :param request: 请求注册页面
        :return: 注册页面
        """
    return render(request, 'login/志愿者注册.html')
    # test2.html指的是返回志愿者登录+注册的页面


def getP(request):
    """
        凡是来访问这个视图的请求, 就返回注册页面
        :param request: 请求注册页面
        :return: 注册页面
        """
    return render(request, 'login/患者监护人注册.html')


def getO(request):
    """
        凡是来访问这个视图的请求, 就返回注册页面
        :param request: 请求注册页面
        :return: 注册页面
        """
    return render(request, 'login/社会组织注册.html')


def check_username(request):
    """
    检测用户名的有效性, 从前端
    GET username/(?P<username>\w{1,8})/
    """
    # 去数据库查询用户名,通过判断数量可以获知该用户是否存在
    username = request.GET.get("username")
    data = {
        "count": User.objects.filter(用户ID=username).count()
    }
    # 将数据传输到路由,使JS代码进行进一步的处理
    return JsonResponse(data)


def check_mobile_view(request):
    """
    校验手机号是否存在
    GET /mobile/(?P<mobile>w{1-11}/
    """
    mobile = request.GET.get("mobile")
    data = {
        "count": User.objects.filter(手机号=mobile).count()
    }

    return JsonResponse(data)


def register(request):
    userID = request.POST.get('userID')
    password = request.POST.get('password')
    mobile = request.POST.get('mobile')
    email = request.POST.get('email')
    type = request.POST.get('type')
    if userID and password and mobile and email:
        if User.objects.filter(用户ID=userID, 密码=password, 手机号=mobile, 邮箱=email).count() > 0:
            data = {"code": 1,
                    "message": "用户已注册"}
        else:
            User.objects.create(用户ID=userID, 密码=password, 手机号=mobile, 邮箱=email, 用户类型=type,
                                用户头像="/headpicture/touxiang.png")
            data = {"code": 0,
                    "message": "注册成功！"}
    else:
        data = {"code": 2,
                "message": "以上内容不得为空"}

    return JsonResponse(data)


def registerP(request):
    userID = request.POST.get('userID')
    password = request.POST.get('password')
    mobile = request.POST.get('mobile')
    email = request.POST.get('email')
    type = request.POST.get('type')
    sickchildren = request.POST.get('sickchildren')
    income = request.POST.get('income')

    if userID and password and mobile and email and sickchildren and income:
        if User.objects.filter(用户ID=userID, 密码=password, 手机号=mobile, 邮箱=email).count() > 0:
            data = {"code": 1,
                    "message": "用户已注册"}
        else:
            User.objects.create(用户ID=userID, 密码=password, 手机号=mobile, 邮箱=email, 用户类型=type, 家庭年收入=income,用户头像="/headpicture/touxiang.png")
            Sick_children.objects.create(患病儿童姓名=sickchildren)
            parent_children.objects.create(用户_id=userID, 患病儿童_id=sickchildren)
            data = {"code": 0,
                    "message": "注册成功！"}
    else:
        data = {"code": 2,
                "message": "以上内容不得为空"}

    return JsonResponse(data)


def registerO(request):
    userID = request.POST.get('userID')
    password = request.POST.get('password')
    mobile = request.POST.get('mobile')
    email = request.POST.get('email')
    type = request.POST.get('type')
    zuzhiming = request.POST.get('zuzhiming')
    orgtype = request.POST.get('orgtype')
    des = request.POST.get('des')
    if userID and password and mobile and email and zuzhiming and orgtype and des:
        if User.objects.filter(用户ID=userID, 密码=password, 手机号=mobile, 邮箱=email).count() > 0:
            data = {"code": 1,
                    "message": "用户已注册"}
        else:
            User.objects.create(用户ID=userID, 密码=password, 手机号=mobile, 邮箱=email, 用户类型=type, 姓名_组织名=zuzhiming,
                                组织类型=orgtype, 组织描述=des,用户头像="/headpicture/touxiang.png")
            data = {"code": 0,
                    "message": "注册成功！"}
    else:
        data = {"code": 2,
                "message": "以上内容不得为空"}

    return JsonResponse(data)


# def get2(request):
#   return render(request, '注册登录页/test.html')
# test2.html指的是返回注册页面

def logintest(request):
    userID = request.POST.get('userID')
    password = request.POST.get('password')
    if userID and password:
        if User.objects.filter(用户ID=userID, 密码=password).count() == 1:
            data = {"code": 0,
                    "message": "恭喜您，登录成功！"}
            user = User.objects.get(用户ID=userID, 密码=password)
            request.session['userID'] = user.用户ID
            request.session['is_login'] = True
            request.session['type'] = user.用户类型
            request.session['shiming'] = user.是否实名认证
            request.session['zuzhi'] = user.是否通过社会组织认证
        else:
            data = {"code": 1,
                    "message": "用户名或密码错误！"}
    else:
        data = {"code": 2,
                "message": "用户名或密码为空"}
    return JsonResponse(data)


def logout(request):
    if not request.session.get('is_login', None):
        return render(request, 'BBS-shop/index.html')  # 如果本来就未登录 那就不用登出
    del request.session['userID']
    del request.session['is_login']
    return redirect('/webxxdd/')  # 退出登录


def index(request):
    return render(request, 'BBS-shop/index.html')  # 登录成功后返回网站首页


def touxiang(request):
    userID = request.POST.get("userID")
    user = User.objects.get(用户ID=userID)
    data = user.用户头像.url
    return JsonResponse(data,safe=False)
