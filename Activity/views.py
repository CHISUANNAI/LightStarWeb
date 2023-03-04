from datetime import timezone, datetime

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from Activity.models import Activity, ActivityPicture, SetActivity, SetActivityPicture
from user_apply_data.models import Activity_registration
from user_data.user_data_models import User
import json


# Create your views here.

# def dispatcher(request):
# 将请求参数统一放入request 的 params 属性中，方便后续处理

# GET请求 参数在url中，同过request 对象的 GET属性获取
#   if request.method == 'GET':
#       request.params = request.GET

# POST/PUT/DELETE 请求 参数 从 request 对象的 body 属性中获取
#   elif request.method in ['POST', 'PUT', 'DELETE']:
# 根据接口，POST/PUT/DELETE 请求的消息体都是 json格式
#      request.params = json.loads(request.body)

# 根据不同的action分派给不同的函数进行处理
#  action = request.params['action']
#  if action == 'list_brief':
#      return listbrief(request)
#  elif action == 'showact':
#      return showact(request)
#   elif action == 'showact':
#       return showact(request)
#   elif action == 'del_customer':
#       return deletecustomer(request)

# else:
#      return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})


def showact(request):
    return render(request, '活动页new/活动.html')


# def listbrief(request, imgid):
#    pic = ActivityPicture.objects.filter(活动=imgid).first
#   return render('活动页/test.html', {'pic': pic})


# def show(request):
#    piclist = ActivityPicture.objects.all()
#    return render(request, '活动页/test.html', {'piclist': piclist})


def showdetail(request):
    actid = request.GET.get("actid")
    act = Activity.objects.get(活动id=actid)
    data = {
        "title": Activity.objects.get(活动id=actid).活动标题,
        "location": Activity.objects.get(活动id=actid).活动地点,
        "date": Activity.objects.get(活动id=actid).活动日期,
        "article": Activity.objects.get(活动id=actid).活动详细介绍,
        "piclist": ActivityPicture.objects.get(活动=act.活动id)  # 一个活动下只能添加一张图片
    }
    return render(request, '活动页new/往期活动页.html', {'data': data})  # 活动详情页显示具体文章信息


# def listbrief(request,imgid):
# pic = ActivityPicture.objects.filter(活动=imgid).first
#  return render('新活动页/C.html', {'pic': pic})

# def showpic(request):
#  piclist = ActivityPicture.objects.all()
#  return render(request, '新活动页/C.html', {'piclist': piclist})


def showsetact(request):
    return render(request, '活动页new/发起活动.html')


def addsetact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        date = request.POST.get('date')
        place = request.POST.get('place')
        des = request.POST.get('des')
        date2 = request.POST.get('date2')
        photo = request.FILES.get('photo')
        orgid = request.GET.get('orgid')
        org = User.objects.get(用户ID=orgid)
        renzhen = org.是否通过社会组织认证
        if renzhen:
            if name and date and place and des and date2 and photo and orgid:
                SetActivity.objects.create(发起活动名称=name, 发起活动日期=date, 发起活动地点=place, 发起活动简介=des, 报名截止日期=date2,
                                           组织类用户_id=orgid)
                SetActivityPicture.objects.create(活动图片=photo, 活动_id=name)
                data = {
                    "code": 1,
                    "message": "上传成功!请等待管理员审核！"
                }
            else:
                data = {
                    "code": 0,
                    "message": "以上内容不得为空！"
                }
        else:
            data = {
                "code": 2,
                "message": "请先通过社会组织认证！"
            }

    # new_img = Activity.models.SetActivityPicture(
    # 活动图片 = photo,  # 拿到图片
    # 活动_id = name   # 拿到图片的名字
    # )
    # new_img.save()  # 保存图片

    return JsonResponse(data)


def showall(request):
    return render(request, "活动页new/待办活动全部.html")


def listact(request):
    listact = SetActivity.objects.filter(是否通过审核=1, 报名截止日期__gt=datetime.now(), 发起活动日期__gt=datetime.now()).values(
        "发起活动名称", "发起活动日期",
        "发起活动地点", "发起活动简介",
        "报名截止日期")
    listact = list(listact)
    for i in range(len(listact)):
        k = listact[i]["发起活动名称"]
        s1 = SetActivityPicture.objects.get(活动_id=k)
        listact[i]["活动图片"] = s1.活动图片.url
    return JsonResponse({'待发布活动': listact})


def apply(request):
    userid = request.POST.get("userid")
    title = request.POST.get("title")

    if Activity_registration.objects.filter(用户_id=userid, 发起的活动_id=title).count() > 0:
        data = {
            "code": 0,
            "message": "您已报名过该活动！"
        }
    else:
        Activity_registration.objects.create(用户_id=userid, 发起的活动_id=title)
        data = {
            "code": 1,
            "message": "报名成功！"
        }
    return JsonResponse(data)
