window.onload = function () {

    var url = decodeURI(window.location.href);
    var para = url.getQueryString("posttitle").replace("#", "");
    $("#posttitle").text(para);
    //获取帖子标题
    function show(title, s) {
        var m = "#" + title;
        //   $(m).text(((JSON.stringify(s).replace("\"","")).replace("\"","")));
          $(m).html((((JSON.stringify(s).replace("\"", "")).replace("\"", "")).replace(/\\n/g, "<br>")).replace(/\\r/g, "\n"));
    }
    $.ajax({
        type: "get",
        data: { action: "list_one_content", title: para },
        url: "../BBS/list_BBS_content",
        dataType: "json",
        success: function (data) {
            show("帖子内容", data.postcontent[0].帖子内容)
            show("用户姓名", data.postcontent[0].用户_id)
            show("论坛分区", data.postcontent[0].论坛分区)
            $("#楼主头像").css("background","url("+data.postcontent[0].用户头像+")");
             $("#楼主头像").css("background-size","100%");
            //$("#帖子内容").text((JSON.stringify(data.postcontent[0].帖子内容))).replace(/\n/g,"<br/>");
            $("#发帖年月日").text((JSON.stringify(data.postcontent[0].发帖时间).replace("\"", "")).replace("\"", "").substring(0, 10));
            $("#发帖时刻").text((JSON.stringify(data.postcontent[0].发帖时间).replace("\"", "")).replace("\"", "").substring(11, 19));
            var litag = "";
            for (var i = 0; i < data.commentlist.length; i++) {
                l = data.allreply[i].length;
                var buildCount = data.commentlist[i].楼数;
                var id = data.commentlist[i].用户_id;
                var otherContent = data.commentlist[i].评论内容;
                var t = data.commentlist[i].评论时间;
                var touxiang=data.commentlist[i].用户头像;
                litag += "<li><div class='content-other clearfix container'>" +
                    "<div class='other-info fl'>" +
                    "<div class='ava' style='background-image: url("+ touxiang +")'"+"</div>" +
                    "<p class='nic'>" + id + "</p>" +
                    " <p class='floor'>" + buildCount + "楼</p>" +
                    "<p class='time'>" + t.substring(0, 10)  +
                    t.substring(11, 19) + "</p>" +
                    "</div>" +
                    "<div class='content-detail '>" +
                    "<p>" + otherContent + "</p>" +
                    "<button type='button'  class='ref-bot  fr' onclick='aopen(" + i + ")' title='回复层主' ></button>" +
                    "</div>" +
                    "<div class='ref clearfix '>" +
                    "<textarea class='ref-box' id='r" + i + "' cols='30' rows='4' placeholder='输入你的回复内容'></textarea>" +
                    "<button type='button' class='sub' id='s" + i + "' onclick='refthis(" + i + ")' onmousedown='chas(" + i + ")' onmouseup='chasb(" + i + ")'>回复</button>" +
                    "<button type='button' onclick='aopen(" + i + ")' class='con' id='c" + i + "' onmousedown='chac(" + i + ")' onmouseup='chacb(" + i + ")'>取消</button>";
                for (var j = 0; j < l; j++) {
                    litag += "<p><span>" + data.allreply[i][j].用户_id + "：</span><span>" + data.allreply[i][j].评论内容 + "</span> &nbsp&nbsp&nbsp" + "<span>" + data.allreply[i][j].评论时间.substring(0, 10) + " " + data.allreply[i][j].评论时间.substring(11, 19) + "</span>" + "</p>";
                }
                litag += "</div>" +
                    "</div></li>"

            }
            var ultag = document.getElementById("other-content");
            ultag.innerHTML = litag;
            $(".ref-box").hide();
            $(".sub").hide();
            $(".con").hide();
        }

    })

}
//打开回复楼层框
function aopen(n) {
    s1 = "#r" + n;
    s2 = "#s" + n;
    s3 = "#c" + n;
    $(s1).slideToggle();
    $(s2).slideToggle();
    $(s3).slideToggle();
}
function refthis(n) {
    re = "#r" + n;
    $.ajax({
        type: "post",
        data: JSON.stringify({
            action: "add_floor_reply", title: document.getElementById("posttitle").innerText, replyuserid: document.getElementById("userid").innerText,
            replycontent: $(re).val(), floor: n + 1
        }),
        url: "../BBS/comment",
        dataType: "json",
        success: function (data) {
            $("#json").text(JSON.stringify(data));
            console.log(data);
        }
    })
    window.location.reload();
}
//按钮按下的变色
function chas(n) {
    str = "#s" + n;
    $(str).attr("class", "sub-af");
}
function chasb(n) {
    str = "#s" + n;
    $(str).attr("class", "sub");
}
function chac(n) {
    str = "#c" + n;
    $(str).attr("class", "con-af");
}
function chac(n) {
    str = "#c" + n;
    $(str).attr("class", "con");
}
String.prototype.getQueryString = function (name) {
    var reg = new RegExp("(^|&|\\?)" + name + "=([^&]*)(&|$)"), r;
    if (r = this.match(reg)) return unescape(r[2]);
    return null;
}

var url = decodeURI(window.location.href);
var para = url.getQueryString("posttitle");
var a ;
var islogin=document.getElementById("islogin").innerText;
if (islogin) {
  a = document.getElementById("session").innerText;
}
else{
  a="morenzhi";
}

// 侧边栏及点赞收藏举报操作
var aside = new Vue({
    el: "#aside",
    data: {
        isLike: true,
        isCollect: false,
        dlike: "alter_thumb",
        dcollect: "alter_collection",
        userID: a,
        title: para,
        reason:"",
        dreport:"report_post",
    },
    methods: {
        test() {
            console.log(this.title);
        },
        likeif() {
            if(this.userID==="morenzhi"){
                 alert("请先登录！");
          setTimeout(function () {
                     //登录成功后1.5s回到页面首页
                     window.location.href ='/user_data/login/'
                 }, 1000);
            }
            else{
            var that = this;
            axios.get("../BBS/list_BBS_content?action=if_thumb&userID=" + this.userID + "&title=" + this.title).then(function (response) {
                if (response.data.ret == 1) {
                    that.isLike = true;
                } else {
                    that.isLike = false;
                };
            }, function (err) { }) }
        },
        like() {
                        if(this.userID==="morenzhi"){
                 alert("请先登录！");
          setTimeout(function () {
                     //登录成功后1.5s回到页面首页
                     window.location.href ='/user_data/login/'
                 }, 1000);
            }
                        else{
            this.isLike = !this.isLike;
            axios.post("../BBS/list_BBS_content", {
                action: this.dlike,
                title: this.title,
                userID: this.userID,
            }).then(
                function (response) {
                    // console.log(response);
                },
                function (err) {
                    console.log(err);
                }
            ) }
        },
        collect() {
            if(this.userID==="morenzhi"){
                 alert("请先登录！");
          setTimeout(function () {
                     //登录成功后1.5s回到页面首页
                     window.location.href ='/user_data/login/'
                 }, 1000);
            }
            else{
            this.isCollect = !this.isCollect;
            axios.post("../BBS/list_BBS_content", {
                action: this.dcollect,
                title: this.title,
                userID: this.userID,
            }).then(
                function (response) {
                    console.log(response);
                },
                function (err) {
                    console.log(err);
                }
            ) }
        },
        collectif() {
            if(this.userID==="morenzhi"){
                 alert("请先登录！");
          setTimeout(function () {
                     //登录成功后1.5s回到页面首页
                     window.location.href ='/user_data/login/'
                 }, 1000);
            }
            else{
            var that = this;
            axios.get("../BBS/list_BBS_content?action=if_collect&userID=" + this.userID + "&title=" + this.title).then(function (response) {
                if (response.data.ret == 1) {
                    that.isCollect = true;
                } else {
                    that.isCollect = false;
                };
            }, function (err) { })}
        },
        report(){
            if(this.userID==="morenzhi"){
                 alert("请先登录！");
          setTimeout(function () {
                     //登录成功后1.5s回到页面首页
                     window.location.href ='/user_data/login/'
                 }, 1000);
            }
            else{
            axios.post("../BBS/list_BBS_content", {
                action: this.dreport,
                title: this.title,
                userid: this.userID,
                reason:this.reason,
            }).then(
                function (response) {
                    console.log(response);
                },
                function (err) {
                    console.log(err);
                }
            )
        }}

    }

});

// 帖子回复
var reply = new Vue({
    el: "#reply",
    data: {
        action: "add_comment_floor",
        title: para,
        commentuserid: a,
        commentcontent: "",
        isChange: true,
    },
    methods: {
        test: function () {
            console.log(this.commentcontent);
        },
        posting: function () {
            if(this.commentuserid==="morenzhi"){
                 alert("请先登录！");
          setTimeout(function () {
                     //登录成功后1.5s回到页面首页
                     window.location.href ='/user_data/login/'
                 }, 1000);
            }
            else{
            var that = this;
            axios.post("../BBS/comment", {
                action: this.action,
                title: this.title,
                commentuserid: this.commentuserid,
                commentcontent: this.commentcontent,
            }).then(
                function (response) {
                    console.log(response);
                    window.location.reload();
                },
                function (err) {
                    console.log(err);
                }
            )}
        },
        change: function () {
            this.isChange = !this.isChange;
        }
    }
})
// 楼层回复
