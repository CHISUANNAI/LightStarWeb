# import typing_extensions
from os import umask
from django.db.models.fields import CommaSeparatedIntegerField
from django.shortcuts import render
import json
from django.http import JsonResponse
from BBS.BBS_models import Bbsdata, Comment_data, Report_post,Reply_data
from user_data.user_data_models import User
from user_apply_data.models import User_thumb_post,User_collect_post
# Create your views here.
from django.http import HttpResponse
import datetime
from django.db.models import Q

def show_post_html(request):
    return render(request, "BBS-shop/post.html")

def dispatcher(request):
    # 将请求参数统一放入request 的 params 属性中，方便后续处理

    # GET请求 参数在url中，同过request 对象的 GET属性获取
    if request.method == 'GET':
        request.params = request.GET

    # POST/PUT/DELETE 请求 参数 从 request 对象的 body 属性中获取
    elif request.method in ['POST', 'PUT', 'DELETE']:
        # 根据接口，POST/PUT/DELETE 请求的消息体都是 json格式
        request.params = json.loads(request.body)

    # 根据不同的action分派给不同的函数进行处理
    action = request.params['action']
    if action == 'list_partial_title':
        return list_partial_title(request)

    elif action == 'list_one_content':
        return list_one_content(request)
       
    elif action == 'alter_thumb':
        return alter_thumb(request)
   
    elif action == 'alter_collection':
        return alter_collection(request)
    
    elif action == 'add_post':
        return add_post(request)

    elif action == 'search_post':
        return search_post(request)
    
    elif action == 'report_post':
        return report_post(request)
    
    elif action == 'if_thumb':
            return if_thumb(request)

    elif action == 'if_collect':
            return if_collect(request)




def if_thumb(request):
    title = request.params['title']
    userid = request.params['userID']
    try:
        # 根据 title 找到相应的帖子记录
        post= User_thumb_post.objects.get(帖子_id=title,用户_id=userid)
    except User_thumb_post.DoesNotExist:
        return  JsonResponse({
                'ret': 1,
                'msg': '没有点过赞！'
        })
    return JsonResponse({
                'ret': 0,
                'msg': '点过赞！'
        })


def if_collect(request):
    title = request.params['title']
    userid = request.params['userID']
    try:
        # 根据 title 找到相应的帖子记录
        post= User_collect_post.objects.get(帖子_id=title,用户_id=userid)
    except User_collect_post.DoesNotExist:
        return  JsonResponse({
                'ret': 1,
                'msg': '没有收藏过！'
        })
    return JsonResponse({
                'ret': 0,
                'msg': '收藏过！'
        })


def open_post(request):  
    return render(request,'BBS-shop/post-content.html')

def list_catalog_post(request):
    return render(request,'BBS-shop/post-detail.html')


#发出标题信息，列出标题对应的帖子全部信息、楼层评论
def list_one_content(request):
    title = request.params['title']
    try:
        # 根据 title 找到相应的帖子记录
        post = Bbsdata.objects.get(帖子标题=title)
    except Bbsdata.DoesNotExist:
        return JsonResponse({
            'ret': 1,
            'msg': '帖子被删除！'
        })
    post.浏览次数 += 1
    post.save()
    # 找到帖子有关信息
    qs = Bbsdata.objects.values()
    qs = qs.filter(是否审核通过=1)
    qs = qs.filter(帖子标题=title)
    postcontent = list(qs)
    userid = postcontent[0]["用户_id"]
    user = User.objects.get(用户ID=userid)
    postcontent[0]["用户头像"] = user.用户头像.url
    # 找到帖子的评论有关信息
    cn = Bbsdata.objects.get(帖子标题=title)
    commentlist = Comment_data.objects.filter(帖子标题_id=cn).order_by("楼数").values()
    commentlist = list(commentlist)
    for i in range(len(commentlist)):
        id = commentlist[i]["用户_id"]
        u = User.objects.get(用户ID=id)
        commentlist[i]["用户头像"] = u.用户头像.url
    i = len(commentlist)
    replylist = []
    for j in range(i):
        k = j + 1
        thiscomment = Comment_data.objects.get(帖子标题_id=title, 楼数=k)
        thisid = thiscomment.id
        thisallreply = Reply_data.objects.filter(回复的评论_id=thisid).order_by("-评论时间").values()
        thisallreply = list(thisallreply)
        replylist.append(thisallreply)

    # s1 = Comment_data.objects.filter(帖子标题_id=cn)

    return JsonResponse(
        {'ret': 0, 'postcontent': postcontent, 'commentlist': commentlist, "allreply": replylist, "count": i})

 # 发出论坛分区，列出论坛数据并按浏览量排序
def list_partial_title(request):
   
    qs = Bbsdata.objects.values()
    catalog = request.params['catalog']
    qs=qs.filter(是否审核通过=1)
    qs = qs.filter(论坛分区=catalog).order_by("-浏览次数")
    
    # 将 QuerySet 对象 转化为 list 类型
    # 否则不能 被 转化为 JSON 字符串'''
    retlist = list(qs)
    j=len(list(qs))
    return JsonResponse({'ret': 0, 'retlist': retlist,"count":j})




def alter_thumb(request):
    title = request.params['title']
    userID = request.params['userID']
    post= Bbsdata.objects.get(帖子标题=title)
    try:
        record = User_thumb_post.objects.get(帖子_id=title,用户_id=userID)
        record.delete()
    except:
        record = User_thumb_post.objects.create(点赞时间=datetime.datetime.now(),帖子_id=title,用户_id=userID)
        post.点赞数+=1
        post.save()
        return  JsonResponse({
                'ret': 0,
                'msg': "点赞成功！"
        })
    post.点赞数-=1
    post.save()
    return   JsonResponse({
                'ret': 0,
                'msg': '取消点赞成功！'
        })

def alter_collection(request):
    title = request.params['title']
    userID = request.params['userID']
    post= Bbsdata.objects.get(帖子标题=title)
    try:
        record = User_collect_post.objects.get(帖子_id=title,用户_id=userID)
        record.delete()
    except:
        record = User_collect_post.objects.create(收藏时间=datetime.datetime.now(),帖子_id=title,用户_id=userID)
        post.收藏数+=1
        post.save()
        return  JsonResponse({
                'ret': 0,
                'msg': "收藏成功！"
        })
    post.收藏数-=1
    post.save()
    return   JsonResponse({
                'ret': 0,
                'msg': '取消收藏成功！'
        })

def add_post(request):
    
     title = request.params['title']
     postcontent = request.params['postcontent']
     userid = request.params['userid']
     catalog = request.params['catalog']
     try:
        record = Bbsdata.objects.create(帖子标题=title,帖子内容=postcontent,发帖时间=datetime.datetime.now(),论坛分区=catalog,点赞数=0,收藏数=0,浏览次数=0,是否审核通过=0,用户_id=userid)
     except:
        return  JsonResponse({
                'ret': 1,
                'msg': "发帖失败！请更换标题避免重复。"
        })
     record.save()
     return JsonResponse({'ret': 0})

def search_post(request):

    keyword = request.params['keyword']
    error_msg = ''
    if not keyword:
        error_msg = '请输入关键词'
        return JsonResponse({'ret': 0, 'error_msg': error_msg,'post_list':[]})
    post_list = Bbsdata.objects.values()
    post_list = post_list.filter(Q(帖子标题__icontains=keyword)|Q(帖子内容__icontains=keyword))
    post_list=post_list.filter(是否审核通过=1)
    post_list=list(post_list)
    i=len(post_list)
    if not post_list:
        error_msg="没有找到相关数据！"
        return JsonResponse({'ret': 0, 'error_msg': error_msg,'post_list': post_list})
    return JsonResponse({'ret': 0, 'error_msg':error_msg,'post_list': post_list})

def report_post(request):
    
     posttitle = request.params['title']
     userid = request.params['userid']
     reason = request.params['reason']
     try:
        record = Report_post.objects.create(帖子标题_id=posttitle,举报用户_id=userid,举报时间=datetime.datetime.now(),是否审核通过=0,举报理由=reason)
     except:
        return  JsonResponse({
                'ret': 1,
                'msg': "举报失败！不能重复举报。"
        })
     record.save()
     return JsonResponse({'ret': 0})   
     

