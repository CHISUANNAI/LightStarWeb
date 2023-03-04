# import typing_extensions
from django.db.models.fields import CommaSeparatedIntegerField
from django.shortcuts import render
import json
from django.http import JsonResponse
from BBS.BBS_models import Bbsdata, Comment_data, Reply_data
from user_data.user_data_models import User
from user_apply_data.models import User_thumb_post,User_collect_post
# Create your views here.
from django.http import HttpResponse
import datetime

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
    if action == 'add_comment_floor':
        return add_comment_floor(request)

    elif action == 'add_floor_reply':
        return add_floor_reply(request)
 
    elif action == 'list_floor_reply':
        return list_floor_reply(request)
'''     
    elif action == 'add_collection':
        return add_collection(request)
    
    elif action == 'add_post':
        return add_post(request)

    else:
        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})
'''
def add_comment_floor(request):
 
     title = request.params['title']
     commentcontent = request.params['commentcontent']
     commentuserid = request.params['commentuserid']
     commentlist=Comment_data.objects.filter(帖子标题_id=title).values()
     commentlist=list(commentlist)
     i=len(commentlist)
     i=i+1
     try:
        record =Comment_data.objects.create(帖子标题_id=title,楼数=i,评论内容=commentcontent,评论时间=datetime.datetime.now(),用户_id=commentuserid)
     except:
        return  JsonResponse({
                'ret': 1,
                'msg': "评论失败！帖子可能已经不存在！"
        })
     record.save()
     return JsonResponse({'ret': 0})

def add_floor_reply(request):
    

     title = request.params['title']
     replycontent = request.params['replycontent']
     replyuserid = request.params['replyuserid']
     floor=request.params['floor']
    
     
     thisreply=Comment_data.objects.get(帖子标题_id=title,楼数=floor)
     thisid=thisreply.id
     reply=Reply_data.objects.filter(回复的评论_id=thisid).values().distinct()
     i=len(list(reply))
     i=i+1
     allreply=Reply_data.objects.values().distinct()
     j=len(list(allreply))
     j=j+1
     try:
        record =Reply_data.objects.create(评论号=j,评论内容=replycontent,评论时间=datetime.datetime.now(),回复的评论_id=thisid,用户_id=replyuserid)
     except:
        return  JsonResponse({
                'ret': 1,
                'msg':"回复失败！"
        })
     record.save()
     return JsonResponse({'ret': 0})

def list_floor_reply(request):
     title = request.params['title']
     floor=request.params['floor']
     thisreply=Comment_data.objects.get(帖子标题_id=title,楼数=floor)
     thisid=thisreply.id
     allreply=Reply_data.objects.filter(回复的评论_id=thisid).values()
     allreply=list(allreply)
     i=len(allreply)
     return JsonResponse({'ret': 0,"allreply":allreply,"count":i})
