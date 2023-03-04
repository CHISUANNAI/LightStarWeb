from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse
from administrator.models import Administrator
from user_data.user_data_models import User, Sick_children, parent_children
from user_apply_data.models import User_collect_post, User_collect_activity, User_thumb_post
from charity_sale.models import Saleitems, ItemImage
import datetime
import json
from user_data.user_data_models import User, parent_children, Sick_children
from BBS.BBS_models import Bbsdata, Report_post, Comment_data, Reply_data
from Activity.models import SetActivity, SetActivityPicture


# Create your views here.

def loginadmin(request):
    return render(request, 'Administrator/login.html')


def logintest(request):
    userID = request.POST.get('userID')
    password = request.POST.get('password')
    if userID and password:
        if Administrator.objects.filter(用户ID=userID, 密码=password).count() == 1:
            data = {"code": 0,
                    "message": "欢迎进入管理员界面！"}
        else:
            data = {"code": 1,
                    "message": "访问失败！"}
    else:
        data = {"code": 2,
                "message": "用户名或密码为空"}
    return JsonResponse(data)


def jumpindex(request):
    return render(request, 'Administrator/管理员主页.html')


def jumpuser(request):
    return render(request, 'Administrator/用户认证.html')


def jumporg(request):
    return render(request, 'Administrator/组织认证.html')


def jumpchild(request):
    return render(request, 'Administrator/患儿认证.html')


def listVP(request):
    listVP = User.objects.filter(
        (Q(用户类型='Vol') & Q(认证图片__isnull=False) & Q(是否实名认证=0)) | (
                Q(用户类型='Par') & Q(认证图片__isnull=False) & Q(是否实名认证=0))).values("用户ID", "用户类型",
                                                                             "姓名_组织名",
                                                                             "身份证号")
    listVP = list(listVP)
    for i in range(len(listVP)):
        s1 = User.objects.get(用户ID=listVP[i]["用户ID"])

        listVP[i]["认证图片"] = s1.认证图片.url

    return JsonResponse({'身份认证': listVP})


def listVPpass(request):
    userID = request.POST.get("userid")
    User.objects.filter(用户ID=userID).update(是否实名认证=1)
    data = {"message": "通过认证！"}
    return JsonResponse(data)


def listO(request):
    listO = User.objects.filter(用户类型='Org', 认证图片__isnull=False, 是否通过社会组织认证=0).values("用户ID", "组织类型",
                                                                                     "姓名_组织名",
                                                                                     "组织描述")

    listO = list(listO)
    for i in range(len(listO)):
        s1 = User.objects.get(用户ID=listO[i]["用户ID"])
        listO[i]["认证图片"] = s1.认证图片.url

    return JsonResponse({'组织认证': listO})


def listOpass(request):
    userID = request.POST.get("userid")
    User.objects.filter(用户ID=userID).update(是否通过社会组织认证=1)
    data = {"message": "通过认证！"}
    return JsonResponse(data)


def listchild(request):
    listchild = Sick_children.objects.filter(认证图片__isnull=False, 是否通过患病认证=0).values("患病儿童姓名")
    listchild = list(listchild)
    for i in range(len(listchild)):
        s1 = Sick_children.objects.get(患病儿童姓名=listchild[i]["患病儿童姓名"])
        listchild[i]["认证图片"] = s1.认证图片.url
        s2 = parent_children.objects.get(患病儿童_id=listchild[i]["患病儿童姓名"])
        listchild[i]["用户ID"] = s2.用户_id

    return JsonResponse({'患儿认证': listchild})


def listchildpass(request):
    childname = request.POST.get("childname")
    Sick_children.objects.filter(患病儿童姓名=childname).update(是否通过患病认证=1)
    data = {"message": "通过认证！"}
    return JsonResponse(data)


def cal1(request):
    listchild = Sick_children.objects.filter(认证图片__isnull=False, 是否通过患病认证=0).values("患病儿童姓名")
    listchild = list(listchild)
    return JsonResponse({'患儿': listchild})


def cal2(request):
    listO = User.objects.filter(用户类型='Org', 认证图片__isnull=False, 是否通过社会组织认证=0).values("用户ID", "组织类型",
                                                                                     "姓名_组织名",
                                                                                     "组织描述")
    listO = list(listO)
    return JsonResponse({'组织': listO})


def cal3(request):
    listVP = User.objects.filter(
        (Q(用户类型='Vol') & Q(认证图片__isnull=False) & Q(是否实名认证=0)) | (
                Q(用户类型='Par') & Q(认证图片__isnull=False) & Q(是否实名认证=0))).values("用户ID", "用户类型",
                                                                             "姓名_组织名",
                                                                             "身份证号")
    listVP = list(listVP)
    return JsonResponse({'身份': listVP})


def cal4(request):
    listtiezi = Report_post.objects.filter(是否审核通过=0).order_by("举报时间").values("举报用户_id", "帖子标题_id", "举报时间", "举报理由")
    listtiezi = list(listtiezi)
    return JsonResponse({'举报帖子': listtiezi})


def cal5(request):
    myactivity = SetActivity.objects.filter(是否通过审核=0, 报名截止日期__gt=datetime.datetime.now(),
                                            发起活动日期__gt=datetime.datetime.now()).values("发起活动名称", "发起活动日期", "发起活动地点",
                                                                                       "发起活动简介", "报名截止日期")

    myactivity = list(myactivity)
    return JsonResponse({'活动': myactivity})


def cal6(request):
    allitem = Saleitems.objects.filter(是否已卖出=0).values("商品名", "商品描述", "价格", "所属家长_患儿_id")
    itemlist = list(allitem)
    return JsonResponse({'商品': itemlist})


# 以下hanhan的

def open_admin_activity(request):
    return render(request, 'Administrator/待发布活动.html')


def open_admin_bbs(request):
    return render(request, 'Administrator/被举报帖子.html')


def open_admin_shop(request):
    return render(request, 'Administrator/商品清理.html')


def activity_before_audit(request):
    request.params = request.GET
    myactivity = SetActivity.objects.filter(是否通过审核=0, 报名截止日期__gt=datetime.datetime.now(),
                                            发起活动日期__gt=datetime.datetime.now()).values("发起活动名称", "发起活动日期", "发起活动地点",
                                                                                       "发起活动简介", "报名截止日期")

    myactivity = list(myactivity)
    for i in range(len(myactivity)):
        k = myactivity[i]["发起活动名称"]
        s1 = SetActivityPicture.objects.get(活动_id=k)
        myactivity[i]["活动图片"] = s1.活动图片.url
    return JsonResponse({'我报名的活动': myactivity})


def salesitem_before_audit(request):
    request.params = request.GET
    allitem = Saleitems.objects.filter(是否已卖出=0).values("商品名", "商品描述", "价格", "所属家长_患儿_id")
    itemlist = list(allitem.values())
    count = len(itemlist)
    for i in range(count):
        m = itemlist[i]["所属家长_患儿_id"]
        children = list(parent_children.objects.filter(id=m).values())
        childrenname = children[0]["患病儿童_id"]
        userid = children[0]["用户_id"]
        telephone = User.objects.get(用户ID=userid).手机号
        childreninfo = list(Sick_children.objects.filter(患病儿童姓名=childrenname).values())
        itemlist[i]["用户id"] = userid
        itemlist[i]["患儿年龄"] = childreninfo[0]["年龄"]
        itemlist[i]["患儿性别"] = childreninfo[0]["性别"]
        itemlist[i]["患儿姓名"] = childrenname
        itemlist[i]["购买联系方式"] = telephone
        itemimage = ItemImage.objects.get(商品_id=itemlist[i]["商品编号"])
        url = itemimage.商品图片.url
        itemlist[i]["图片url"] = url

    return JsonResponse({
        'ret': 0,
        'allitem': itemlist
    })


def audit_activity(request):
    request.params = json.loads(request.body)
    name = request.params['activityname']
    try:
        activity = SetActivity.objects.get(发起活动名称=name)
    except SetActivity.DoesNotExist:
        return JsonResponse({
            'ret': 1,
            'msg': "处理失败！"
        })
    activity.是否通过审核 = 1
    activity.save()
    return JsonResponse({
        'ret': 0,
        'msg': "审核通过!"
    })


def audit_salesitem(request):
    request.params = json.loads(request.body)
    itemid = request.params['itemid']
    try:
        item = Saleitems.objects.get(商品编号=itemid)
    except Saleitems.DoesNotExist:
        return JsonResponse({
            'ret': 1,
            'msg': "处理失败！"
        })
    item.是否已卖出 = 1
    item.save()
    return JsonResponse({
        'ret': 0,
        'msg': "下架成功!"
    })


def report_before_audit(request):
    request.params = request.GET
    report = Report_post.objects.filter(是否审核通过=0).order_by("举报时间").values("举报用户_id", "帖子标题_id", "举报时间", "举报理由")
    report = list(report)
    return JsonResponse({'举报帖子': report})


def audit_post(request):
    request.params = json.loads(request.body)
    postname = request.params['postname']
    try:
        post = Bbsdata.objects.filter(帖子标题=postname)
        postcomment = Comment_data.objects.filter(帖子标题_id=postname)
        c_postcomment = Comment_data.objects.filter(帖子标题_id=postname).values_list('id', flat=True)
        postaudit = Reply_data.objects.filter(回复的评论_id__in=c_postcomment)
        report = Report_post.objects.filter(帖子标题_id=postname)
        usercollect = User_collect_post.objects.filter(帖子_id=postname)
        userthumb = User_thumb_post.objects.filter(帖子_id=postname)
        postaudit.delete()
        postcomment.delete()
        report.delete()
        usercollect.delete()
        userthumb.delete()
        post.delete()


    except SetActivity.DoesNotExist:
        return JsonResponse({
            'ret': 1,
            'msg': "处理失败！"
        })
    return JsonResponse({
        'ret': 0,
    })
