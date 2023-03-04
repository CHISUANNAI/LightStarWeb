// 全局变量
var isPao = false;
var isVo = false;
var isCo = false;
var roal="";
var isDe=false;
var userid ;
var islogin=document.getElementById("islogin").innerText;
if (islogin) {
  userid = document.getElementById("session").innerText;
}
else{
  userid="morenzhi";
}
function findr() {
	var result;
	var obj = {};
    obj.Id= $("#Id").val();
    $.ajax({
        url : "../user_apply_data/get_volunteer_information?userid="+userid,
        type : "get",
        async: false, //使用同步请求，因为异步请求不能将返回值传给全局变量；
        dataType : "json",
        data:obj,
        success : function(data) {
            result=data.info[0].用户类型;
        }
    });
    return result;
}
roal=findr();
function findde() {
	var result;
	var obj = {};
    obj.Id= $("#Id").val();
    $.ajax({
        url : "../user_apply_data/get_volunteer_information?userid="+userid,
        type : "get",
        async: false, //使用同步请求，因为异步请求不能将返回值传给全局变量；
        dataType : "json",
        data:obj,
        success : function(data) {
            result=data.info[0].是否实名认证;
        }
    });
    return result;
}
isDe=findde();

if (roal == "患者家属") {
    isPao = true;
} else if (roal == "志愿者") {
    isVo = true;
} else {
    isCo = true;
}
// 信息
var upinfo = new Vue({
    el: "#ainfo",
    data: {
        userid: userid,
        myinfo:[],
        avaurl:"",
    },
    methods: {
        lookinfo(){
            var that = this;
            axios.get("../user_apply_data/get_volunteer_information?userid=" + this.userid).then(function (response) {
               console.log(response);
               var list=response.data.info[0];
               that.avaurl="background-image: url('"+list.用户头像+"')";
               console.log(that.avaurl)
               that.myinfo=list;
            }, function (err) { })
            this.goodslist = that.goodslist;
            this.avaurl=that.avaurl;
        }
    }
})
upinfo.lookinfo();

// 查看评论与回复;
var sref = new Vue({
    el: "#myModal7",
    data: {
        isref: true,
        bcon: "查看回复",
        userID: userid,
        conlist: [],
        reflist: [],
        tilist: [],
    },
    methods: {
        aswitch() {
            this.isref = !this.isref;
            if (this.isref) {
                this.bcon = "查看回复";
            }
            else {
                this.bcon = "查看评论";
            }
        },
        lookcon() {
            var that = this;
            axios.get("../user_apply_data/my_comment_reply?userid=" + this.userID).then(function (response) {
                var list = response.data.我的帖子评论;
                var list1 = response.data.我收到的回复;
                var list2 = [];
                for (var i = 0; i < list.length; i++) {
                    list[i].评论时间 = list[i].评论时间.substring(0, 10) + " " + list[i].评论时间.substring(11, 19);
                    list2[i] = list[i].帖子标题_id;
                }
                for (var i = 0; i < list1.length; i++) {
                    list1[i].评论时间 = list1[i].评论时间.substring(0, 10) + " " + list1[i].评论时间.substring(11, 19);
                }
                that.conlist = list;
                that.reflist = list1;
                that.tilist = list2;
            }, function (err) { })
            this.conlist = that.conlist;
            this.reflist = that.reflist;
            this.tilist = that.tilist;
        },
        look(n) {
            console.log(this.tilist)
            window.location.href = encodeURI("/BBS/open_post?posttitle=" + this.tilist[n]);
        }
    }
})
sref.lookcon();
// 个人信息修改
var info = new Vue({
    el: "#myModal1",
    data: {
        isV: isVo,
        isPa: isPao,
        isC: isCo,
        isDe: false,
        userid: userid,
    },
    methods: {
        asuccess() {
            alert("修改成功！")
        }
    }
})
// 我的点赞
var mylike = new Vue({
    el: "#myModal2",
    data: {
        mylikelist: [],
        userID: userid,
        tilist: [],
    },
    methods: {
        looklike() {
            var that = this;
            axios.get("../user_apply_data/my_thumb?userid=" + this.userID).then(function (response) {
                var list = response.data.mythumblist;
                var list1 = [];
                for (var i = 0; i < list.length; i++) {
                    list[i].点赞时间 = list[i].点赞时间.substring(0, 10) + " " + list[i].点赞时间.substring(11, 19);
                    list1[i] = list[i].帖子_id;
                }
                that.tilist = list1;
                that.mylikelist = list;
            }, function (err) { })
        },
        look(n) {
            console.log(this.tilist)
            window.location.href = encodeURI("/BBS/open_post?posttitle=" + this.tilist[n]);
        }
    }
})
mylike.looklike();
// 我的收藏
var mycollect = new Vue({
    el: "#myModal3",
    data: {
        mycollectlist: [],
        userID: userid,
        tilist: [],
    },
    methods: {
        lookcollect() {
            var that = this;
            axios.get("../user_apply_data/my_collection?userid=" + this.userID).then(function (response) {
                var list = response.data.my_collection;
                var list1 = [];
                for (var i = 0; i < list.length; i++) {
                    list[i].收藏时间 = list[i].收藏时间.substring(0, 10) + " " + list[i].收藏时间.substring(11, 19);
                    list1[i] = list[i].帖子_id;
                }
                that.tilist = list1;
                that.mycollectlist = list;
            }, function (err) { })
        },
        look(n) {
            console.log(this.tilist)
            window.location.href = encodeURI("/BBS/open_post?posttitle=" + this.tilist[n]);
        }
    }
})
mycollect.lookcollect();
// 活动查看与编辑
var ac = new Vue({
    el: "#myModal4",
    data: {
        isV: isVo,
        isPa: isPao,
        isC: isCo,
        isDe: false,
        userID: userid,
        aclist: [],
        Caclist: [],
        Aaclist: [],
        acname: "",
    },
    methods: {
        De(n) {
            this.isDe = !this.isDe;
            this.acname = this.Caclist[n][0].发起活动名称;
            var list = this.Caclist[n][1];
            this.Aaclist = list;
        },
        PVshow() {
            var that = this;
            axios.get("../user_apply_data/my_registered_actitity?userid=" + this.userID).then(function (response) {
                var list = response.data.我报名的活动;
                that.aclist = list;
            }, function (err) { })
            this.aclist = that.aclist;

        },
        Cshow() {
            var that = this;
            axios.get("../user_apply_data/my_set_actitity?userid=" + this.userID).then(function (response) {
                var list = response.data.我发起的活动;
                that.Caclist = list;
            }, function (err) { })
            this.Caclist = that.Caclist;

        },

    }
})
if (isPao || isVo) {
    ac.PVshow();
} else {
    ac.Cshow();
}
// 身份认证
var iedCer = new Vue({
    el: "#myModal5",
    data: {
        isV: isVo,
        isPa: isPao,
        isC: isCo,
        isDe: isDe,
        userid: userid,
        Painfo: [],
        isupdate: false,
    },
    methods: {
        showifo() {
            var that = this;
            if (this.isPa) {
                axios.get("../user_apply_data/get_parent_identify?userid=" + this.userid).then(function (response) {
                    var list = response.data;
                    that.Painfo = list;
                }, function (err) { })

            } else if (this.isC) {
                axios.get("../user_apply_data/get_organization_identify?userid=" + this.userid).then(function (response) {
                    console.log(response)
                    var list = response.data.组织认证信息初始化[0];
                    that.Painfo = list;
                    console.log(list);
                }, function (err) { })
            } else {
                axios.get("../user_apply_data/get_volunteer_identify?userid=" + this.userid).then(function (response) {
                    console.log(response)
                    var list = response.data.用户认证信息初始化[0];
                    that.Painfo = list;
                    console.log(list);
                }, function (err) { })
            }
            this.Painfo = that.Painfo;
        },
        aupdate() {
            this.isupdate = !this.isupdate;
        }
    }
})
iedCer.showifo();
$(function () {
    /** 验证文件是否导入成功  */
    $("#formr1").ajaxForm(function (data) {
        if (data.ret == 1) {
            alert("上传失败");
        } else {
            alert("上传成功");
        }
    });
});
$(function () {
    /** 验证文件是否导入成功  */
    $("#formr2").ajaxForm(function (data) {
        if (data.ret == 0) {
            alert("上传成功");
        } else {
            alert("上传失败");
        }
    });
});
$(function () {
    /** 验证文件是否导入成功  */
    $("#formr3").ajaxForm(function (data) {
        console.log(data);
        if (data.ret == 0) {
            alert("上传成功");
        } else {
            alert("上传失败");
        }
    });
});
// 义卖查看与编辑
var shop = new Vue({
    el: "#myModal8",
    data: {
        isPa: isPao,
        ised: true,
        userid: userid,
        goli: [],
        itemid: [],
        iteminfo: [],
        num: 4,
    },
    methods: {
        ed(n) {
            this.ised = !this.ised;
            var that = this;
            var list = [];
            axios.get("../user_apply_data/get_edit_my_item?itemid=" + this.itemid[n]).then(function (response) {
                list = response.data.该商品信息[0];
                console.log(list);
                that.iteminfo = list;
            }, function (err) { })
            this.iteminfo = that.iteminfo;
            this.num = this.itemid[n];
        },
        can() {
            this.ised = !this.ised;

        },
        lookshop() {
            var that = this;
            axios.post("../Charity_sale/my_item", {
                userid: this.userid,
            }).then(
                function (response) {

                    var list = response.data.allitem;
                    var list1 = [];
                    for (var i = 0; i < list.length; i++) {
                        if (list[i].是否已卖出) { list[i].是否已卖出 = "已卖出" } else {
                            list[i].是否已卖出 = "未卖出"
                        }
                        list1[i] = list[i].商品编号;
                    }
                    that.goli = list;
                    that.itemid = list1;

                },
                function (err) {
                    console.log(err);
                })
            this.goli = that.goli;
            this.itemid = that.itemid;
        }
    }
})
shop.lookshop();
$(function () {
    /** 验证文件是否导入成功  */
    $("#forms1").ajaxForm(function (data) {
        console.log(data);
        if (data.ret == 0) {
            alert("上传成功");
        } else {
            alert("上传失败");
        }
    });
});
// 帖子查看
var post = new Vue({
    el: "#myModal6",
    data: {
        userid: userid,
        posyli: [],
        npost: [],
        ppost: [],
        tilist: [],
    },
    methods: {
        lookpost() {
            var that = this;
            axios.get("../user_apply_data/my_post?userid=" + this.userid).then(function (response) {
                var list = response.data.待审核的帖子;
                var list1 = response.data.审核通过的帖子;
                var list2 = [];
                for (var i = 0; i < list1.length; i++) {
                    list1[i].发帖时间 = " " + list1[i].发帖时间.substring(0, 10) + " " + list1[i].发帖时间.substring(11, 19);
                    list2[i] = list1[i].帖子标题;
                }
                that.tilist = list2;
                that.npost = list;
                that.ppost = list1;
            }, function (err) { })
            this.npost = that.npost;
            this.ppost = that.ppost;
            this.tilist = that.tilist;
        },
        look(n) {
            console.log(this.tilist)
            window.location.href = encodeURI("/BBS/open_post?posttitle=" + this.tilist[n]);
        }
    }
})
post.lookpost();
