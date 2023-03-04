
from Activity.models import SetActivity
from os import umask
from django.db.models.fields import CommaSeparatedIntegerField
from django.shortcuts import render
import json
from django.http import JsonResponse
from BBS.BBS_models import Bbsdata, Comment_data, Report_post,Reply_data
from user_data.user_data_models import Sick_children, User, parent_children
from user_apply_data.models import User_thumb_post,User_collect_post,Activity_registration
from charity_sale.models import ItemImage,Saleitems
from django.http import HttpResponse
import datetime
from django.db.models import Q

        #request.params = request.GET
        #request.params = json.loads(request.body)
def organization_identify(request):
     userid=request.POST['userid']
     name=request.POST['name']
     description=request.POST['description']
     catalog=request.POST['catalog']
     user=User.objects.get(用户ID=userid)
     try:
          user.姓名_组织名=name
          user.组织描述=description
          user.组织类型=catalog
          user.认证图片=request.FILES.get('photo') 
          user.save()
     except:
         return JsonResponse({'ret': 1,"result":"上传失败！"})

    
     return JsonResponse({'ret': 0,"result":"上传成功"})
    
def get_organization_identify(request):
    if request.method == 'GET':
        request.params = request.GET
        userid=request.params['userid']
        iteminfo=list(User.objects.filter(用户ID=userid).values("姓名_组织名","组织类型","组织描述","是否通过社会组织认证"))
        return JsonResponse({'ret': 0,"组织认证信息初始化":iteminfo})

def volunteer_identify(request):
     userid=request.POST['userid']
     name=request.POST['name']
     identity_card_num=request.POST['identity_card_num']
     user=User.objects.get(用户ID=userid)
     try:
          user.姓名_组织名=name
          user.身份证号=identity_card_num
          user.认证图片=request.FILES.get('photo') 
          user.save()
     except:
         return JsonResponse({'ret': 1,"result":"上传失败！"})

    
     return JsonResponse({'ret': 0,"result":"上传成功"})
    

def get_volunteer_identify(request):
    request.params = request.GET
    userid=request.params['userid']
    iteminfo=list(User.objects.filter(用户ID=userid).values("姓名_组织名","身份证号","是否实名认证"))
    return JsonResponse({'ret': 0,"用户认证信息初始化":iteminfo})

def edit_my_information(request):
    userid=request.POST['userid']
    telephone=request.POST['telephone']
    email=request.POST['email']
    try:
        user=User.objects.get(用户ID=userid)
        user.邮箱=email
        user.手机号=telephone
        user.用户头像=request.FILES.get('photo')
        user.save()
    except:
        return JsonResponse({  
                'ret': 1,"messgae":"上传失败！"
        })

    return JsonResponse({  
                'ret': 0,"messgae":"上传成功！"
        })

def get_volunteer_information(request):
    request.params = request.GET
    userid=request.params['userid']
    iteminfo=User.objects.filter(用户ID=userid).values("姓名_组织名","用户头像","是否实名认证","用户类型")
    iteminfo2=User.objects.get(用户ID=userid)
    iteminfo=list(iteminfo)
    iteminfo[0]["用户头像"]=iteminfo2.用户头像.url
    if iteminfo[0]["用户类型"]=="Vol":
        iteminfo[0]["用户类型"]="志愿者"
    elif iteminfo[0]["用户类型"]=="Org":
        iteminfo[0]["用户类型"]="社会组织"
    elif iteminfo[0]["用户类型"]=="Par":
        iteminfo[0]["用户类型"]="患者家属"
    return JsonResponse({'ret': 0,"info":iteminfo})

def get_edit_my_item(request):
    request.params = request.GET
    userid=request.params['itemid']
    iteminfo=list(Saleitems.objects.filter(商品编号=userid).values("商品名","商品描述","发布日期","价格"))
    return JsonResponse({'ret': 0,"该商品信息":iteminfo})

def my_thumb(request):
    request.params = request.GET
    userid=request.params['userid']
    mythumblist=User_thumb_post.objects.filter(用户_id=userid).order_by("-点赞时间").values()
    mythumblist=list(mythumblist)
    return JsonResponse({'ret': 0, 'mythumblist': mythumblist})

def my_collection(request):
    request.params = request.GET
    userid=request.params['userid']
    my_collection=User_collect_post.objects.filter(用户_id=userid).order_by("-收藏时间").values()
    my_collection=list(my_collection)
    return JsonResponse({'ret': 0, 'my_collection': my_collection})

def my_post(request):
    request.params = request.GET
    userid=request.params['userid']
    my_post_true=Bbsdata.objects.filter(用户_id=userid,是否审核通过=1).order_by("-发帖时间").values()
    my_post_true=list(my_post_true)
    my_post_false=Bbsdata.objects.filter(用户_id=userid,是否审核通过=0).order_by("-发帖时间").values()
    my_post_false=list(my_post_false)
    return JsonResponse({'ret': 0, '审核通过的帖子': my_post_true,"待审核的帖子":my_post_false})

def my_comment_reply(request):
    request.params = request.GET
    userid=request.params['userid']
    mypost=Bbsdata.objects.filter(用户_id=userid).order_by("-发帖时间").values_list('帖子标题', flat=True)
    mycomment=Comment_data.objects.filter(帖子标题_id__in=mypost).values().order_by("-评论时间")
    mycomment=list(mycomment)
    

    previouscomment=Comment_data.objects.filter(Q(用户_id=userid)|Q(帖子标题_id__in=mypost)).order_by("-评论时间").values_list('id', flat=True)
    previousreply=Reply_data.objects.filter(回复的评论_id__in=previouscomment).order_by("-评论时间").values()
 
    previousreply=list(previousreply)
    for i in range(len(previousreply)):
        m=previousreply[i]["回复的评论_id"]
        thecomment=Comment_data.objects.filter(id=m).values()
        thecomment=thecomment[0]["评论内容"]
        previousreply[i]["回复的评论的内容"]=thecomment

        
        
    return JsonResponse({'ret': 0, '我的帖子评论': mycomment,"我收到的回复":previousreply})

def my_item_forsale(request):
    request.params = request.GET
    userid=request.params['userid']
    p_c=parent_children.objects.filter(用户_id=userid).values_list('id', flat=True)
    my_item_true=Saleitems.objects.filter(所属家长_患儿_id__in=p_c,是否已卖出=0).values()
    my_item_true=list(my_item_true)
    for i in range(len(my_item_true)):
        imageurl=ItemImage.objects.get(商品_id=my_item_true[i]["商品编号"])
        my_item_true[i]["商品图片url"]=imageurl.商品图片.url
    
    my_item_false=Saleitems.objects.filter(所属家长_患儿_id__in=p_c,是否已卖出=1).values()
    my_item_false=list(my_item_false)
    for i in range(len(my_item_false)):
        imageurl=ItemImage.objects.get(商品_id=my_item_false[i]["商品编号"])
        my_item_false[i]["商品图片url"]=imageurl.商品图片.url
    return JsonResponse({'ret': 0, '未卖出': my_item_true,'已卖出':my_item_false})

def my_registered_actitity(request):
    request.params = request.GET
    userid=request.params['userid']
    activityname=Activity_registration.objects.filter(用户_id=userid).values_list('发起的活动_id', flat=True)
    myactivity=SetActivity.objects.filter(发起活动名称__in=activityname).values()
    myactivity=list(myactivity)
   
    return JsonResponse({'ret': 0, '我报名的活动': myactivity})

 
def my_set_actitity(request):
    request.params = request.GET
    userid=request.params['userid']
    myactivity=SetActivity.objects.filter(组织类用户_id=userid).values()
    myactivity=list(myactivity)
    alllist=[]
    for i in range(len(myactivity)):
        register=Activity_registration.objects.filter(发起的活动_id=myactivity[i]["发起活动名称"]).values()
        register=list(register)
        for m in range(len(register)):
            register[m]["用户手机号"]=User.objects.get(用户ID=register[m]["用户_id"]).手机号
            register[m]["用户姓名"]=User.objects.get(用户ID=register[m]["用户_id"]).姓名_组织名
        thislist=[]
        thislist.append(myactivity[i])
        thislist.append(register)
        alllist.append(thislist)

      
    return JsonResponse({'ret': 0, '我发起的活动': alllist})  
'''
def upload_headpicture(request):
    if request.method == 'POST':  
     
        try:
            thisuser = User.objects.get(用户ID=request.POST['userid'])
        except User.DoesNotExist:
              return JsonResponse({
                'ret': 1,
                'msg':'用户不存在'
              })
        thisuser.用户头像=request.FILES.get('photo')
        thisuser.save()

        #return JsonResponse({'ret': 0,"result":"上传成功"})
        return render(request, 'BBS-shop/测试.html',{'img':thisuser.用户头像})
    return render(request, 'BBS-shop/测试.html')

def upload_identifypicture(request):
    if request.method == 'POST':  
        try:
            thisuser = User.objects.get(用户ID=request.POST['userid'])
        except User.DoesNotExist:
              return JsonResponse({
                'ret': 1,
                'msg':'用户不存在'
              })
        thisuser.认证图片=request.FILES.get('photo')
        thisuser.save()
        #return JsonResponse({'ret': 0,"result":"上传成功"})
        return render(request, 'BBS-shop/测试.html',{'img':thisuser.认证图片})
    return render(request, 'BBS-shop/测试.html')

def upload_child_identifypicture(request):
    if request.method == 'POST':  
        try:
            c_p=parent_children.objects.get(用户_id=request.POST['userid'])
            children=Sick_children.objects.get(患病儿童姓名=c_p.患病儿童_id) 
        except User.DoesNotExist:   
              return JsonResponse({
                'ret': 1,
                'msg':'用户不存在'
              })
        children.认证图片=request.FILES.get('photo')
        children.save()
        #return JsonResponse({'ret': 0,"result":"上传成功"})
        return render(request, 'BBS-shop/测试.html',{'img':children.认证图片})
    return render(request, 'BBS-shop/测试.html')
'''
def get_parent_identify(request):
    request.params = request.GET
    userid=request.params['userid']
    userlist=list(User.objects.filter(用户ID=userid).values("姓名_组织名","是否实名认证","用户类型","身份证号"))
    p_c=parent_children.objects.get(用户_id=userid)
    childlist=list(Sick_children.objects.filter(患病儿童姓名=p_c.患病儿童_id).values("年龄","患病儿童姓名","是否实名认证","身份证号"))
    child=Sick_children.objects.get(患病儿童姓名=p_c.患病儿童_id)
    
    return JsonResponse({'ret': 0,"用户信息":userlist,"患儿信息":childlist})



def parent_identify(request):
     userid=request.POST['userid']
     parent_name=request.POST['parent_name']
     parent_identity_card_num=request.POST['parent_identity_card_num']
     child_identity_card_num=request.POST['child_identity_card_num']
     age=request.POST['age']
     sex=request.POST['sex']
    
     user=User.objects.get(用户ID=userid)
     p_c=parent_children.objects.get(用户_id=userid)
     child=Sick_children.objects.get(患病儿童姓名=p_c.患病儿童_id)
     
     try:
         user.姓名_组织名=parent_name
         user.身份证号=parent_identity_card_num
         user.认证图片=request.FILES.get('p_photo')
         child.身份证号=child_identity_card_num
         child.年龄=age
         child.性别=sex
         child.认证图片=request.FILES.get('c_photo')
     
         user.save()
         child.save()
     except:
         return JsonResponse({'ret': 1,"result":"上传失败！"})
     return JsonResponse({'ret': 0,"result":"上传成功"})
    
def openmine(request):
    return render(request,"BBS-shop/mine.html")