import user_data
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from charity_sale import models
import charity_sale.models as cm
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import user_data.user_data_models as uu
from datetime import datetime
# Create your views here.
import json
def open_sale(request):
     return render(request, "BBS-shop/shop.html")

def list_all_items(request):
    allitem=cm.Saleitems.objects.filter(是否已卖出=0).order_by("-发布日期")
    itemlist=list(allitem.values())
    count=len(itemlist)
    for i in range(count):
        m=itemlist[i]["所属家长_患儿_id"]
        children=list(uu.parent_children.objects.filter(id=m).values())
        childrenname=children[0]["患病儿童_id"]
        userid=children[0]["用户_id"]
        telephone=uu.User.objects.get(用户ID=userid).手机号
        childreninfo=list(uu.Sick_children.objects.filter(患病儿童姓名=childrenname).values())
        itemlist[i]["用户id"]=userid
        itemlist[i]["患儿年龄"]=childreninfo[0]["年龄"]
        itemlist[i]["患儿性别"]=childreninfo[0]["性别"]
        itemlist[i]["患儿姓名"]=childrenname
        itemlist[i]["购买联系方式"]=telephone
        itemimage=cm.ItemImage.objects.get(商品_id=itemlist[i]["商品编号"])
        url=itemimage.商品图片.url
        itemlist[i]["图片url"]=url

    return JsonResponse({  
                'ret': 0,
                'allitem':itemlist
        })


def my_item(request):
    request.params = json.loads(request.body)
    userid = request.params['userid']
    p_c=uu.parent_children.objects.get(用户_id=userid)
    allitem=cm.Saleitems.objects.filter(所属家长_患儿_id=p_c.id).order_by("-发布日期")
    itemlist=list(allitem.values())
    count=len(itemlist)
    for i in range(count):
        m=itemlist[i]["所属家长_患儿_id"]
        children=list(uu.parent_children.objects.filter(id=m).values())
        childrenname=children[0]["患病儿童_id"]
        userid=children[0]["用户_id"]
        telephone=uu.User.objects.get(用户ID=userid).手机号
        childreninfo=list(uu.Sick_children.objects.filter(患病儿童姓名=childrenname).values())
        itemimage=cm.ItemImage.objects.get(商品_id=itemlist[i]["商品编号"])
        url=itemimage.商品图片.url
        itemlist[i]["图片url"]=url

    return JsonResponse({  
                'ret': 0,
                'allitem':itemlist
        })

def edit_my_item(request):
    if request.method == 'POST':
        itemid=request.POST['itemid']
        itemname=request.POST['itemname']
        description=request.POST['description']
        price=request.POST['price']
        item=cm.Saleitems.objects.get(商品编号=itemid)
        item.商品名=itemname
        item.商品描述=description
        item.价格=price
        item.商品名=itemname
        item.save()
        image=cm.ItemImage.objects.get(商品_id=itemid)
        image.商品图片=request.FILES.get('photo')
        image.save()  # 保存图片
        return JsonResponse({  
                'ret': 0
        })

def alteritem(request):

    request.params = json.loads(request.body)
    itemid=request.params['itemid']
    try:
        item= cm.Saleitems.objects.get(商品编号=itemid,是否已卖出=0)
    except cm.Saleitems.DoesNotExist:
        return  JsonResponse({
                'ret': 1,
                'msg': "该义卖品已售出或下架！"
        })
    item.是否已卖出=1
    item.save()
    return JsonResponse({
                'ret': 0,
                'msg': "下架成功!"
        })

def additem(request):
    # request.params = json.loads(request.body)

    userid = request.POST['userid']
    childrenname = request.POST['childrenname']
    itemname = request.POST['itemname']
    itemdescription = request.POST['itemdescription']
    price = request.POST['price']
    islogin = request.POST['islogin']

    if not islogin:
        return JsonResponse({'ret': 2,
                             'msg': "请先登录！"})
    if islogin:
        shenfen = uu.User.objects.get(用户ID=userid).是否实名认证
        type = uu.User.objects.get(用户ID=userid).用户类型
        if type == 'Vol' or type == 'Org':
            return JsonResponse({'ret': 1,
                                 'msg': "只有患儿家属才能发布商品！"
                                 })
        if type == 'Par':
            try:
                p_c = uu.parent_children.objects.get(患病儿童_id=childrenname, 用户_id=userid)
                huaner=uu.parent_children.objects.get(用户_id=userid)

            except:
                return JsonResponse({
                    'ret': 1,
                    'msg': "未绑定患儿或信息不匹配!"
                })
            if not shenfen:
                return JsonResponse({
                    'ret': 1,
                    'msg': "请先通过身份认证!"
                })
            if not huaner:
                return JsonResponse({
                    'ret': 1,
                    'msg': "请先通过患儿认证!"
                })
            else:
                p_c_id = p_c.id
                allitems = list(cm.Saleitems.objects.values())
                i = len(allitems) + 1
            try:
                record = cm.Saleitems.objects.create(商品编号=i, 商品名=itemname, 商品描述=itemdescription, 是否已卖出=0, 价格=price,
                                             所属家长_患儿_id=p_c_id, 发布日期=datetime.datetime.now().strftime('%Y-%m-%d'))
            except:
                return JsonResponse({
            'ret': 1,
            'msg': "发布商品失败"
        })
            record.save()
            new_img = cm.ItemImage(
                商品图片=request.FILES.get('photo'),  # 拿到图片
                商品_id=i  # 拿到图片的名字
            )
            new_img.save()  # 保存图片
            return JsonResponse({'ret': 0, "itemid": i})

def findimage(request):
    if request.method == 'GET':
        itemid = request.params['itemid']
    IMG=cm.ItemImage.objects.filter(id=3)
    img = cm.ItemImage.objects.filter(商品_id=itemid)
    return render(request,'BBS-shop/测试.html',{'img':img})