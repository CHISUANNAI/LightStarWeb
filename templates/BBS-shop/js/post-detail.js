
var a ;
var islogin=document.getElementById("islogin").innerText;
if (islogin) {
  a = document.getElementById("session").innerText;
}
else{
  a="morenzhi";
}
//发帖
var head = new Vue({
  el: "#posting",
  data: {
    action: "add_post",
    title: "",
    userid: a,
    postcontent: "",
    catalog: "",
    isChange: true,
    islogin:islogin
  },
  methods: {
    ceshi: function () {
      console.log(this.catalog);
    },
    posting: function () {
      console.log("xxx");
      var that = this;
      if (this.userid==="morenzhi"){
          alert("请先登录！");
          setTimeout(function () {
                     //登录成功后1.5s回到页面首页
                     window.location.href ='/user_data/login/'
                 }, 1000);

          }
      else{
      axios.post("../BBS/list_BBS_content", {
        action: this.action,
        title: this.title,
        userid: this.userid,
        postcontent: this.postcontent,
        catalog: this.catalog,
      }).then(
        function (response) {
         console.log(response);

          alert("发帖成功!请等待审核！");
           window.location.reload();
        },
        function (err) {
          console.log(err);
          alert("err");
        }
      )}
    },
    change: function () {
      this.isChange = !this.isChange;
    }
  }
})
//搜索
var url = decodeURI(window.location.href);
var keywordo = url.getQueryString("keyword");
var catalogo = url.getQueryString("catalog");
var search = new Vue({
  el: "#isearch",
  data: {
    action: "search_post",
    keyword: "",
    keywordo: keywordo,
    scontent: [],
    tilist:[],
    pType: catalogo
  },
  methods: {
    test() {
      console.log(this.keyword);
    },
    dsearch() {
      var that = this;
      axios.get("../BBS/list_BBS_content?action=search_post&keyword=" + this.keyword).then(function (response) {
        // console.log(response);
        var list = response.data.post_list;
        var list1=[];
        var l = list.length;
        for (var i = 0; i < l; i++) {
          list[i].发帖时间 = list[i].发帖时间.substring(0, 10) + " " + list[i].发帖时间.substring(11, 19);
          list[i].帖子内容 = list[i].帖子内容.substring(0, 100).replace(/\n/g, "<br>");
          list1[i]=list[i].帖子标题;
        }
        that.tilist=list1;
        that.scontent = list;
      }, function (err) { });
      this.pType="全部帖子";
      this.tilist=that.tilist;
    },
    dsearchout() {
      var that = this;
      axios.get("../BBS/list_BBS_content?action=search_post&keyword=" + this.keywordo).then(function (response) {
        console.log(response);
        var list = response.data.post_list;
        var list1=[];
        var l = list.length;
        for (var i = 0; i < l; i++) {
          list[i].发帖时间 = list[i].发帖时间.substring(0, 10) + " " + list[i].发帖时间.substring(11, 19);
          list[i].帖子内容 = list[i].帖子内容.substring(0, 100).replace(/\n/g, "<br>");
          list1[i]=list[i].帖子标题;
        }
        that.tilist=list1;
        that.scontent = list;
      }, function (err) { })
      this.tilist=that.tilist;
    },
    show() {
      var that = this;
      axios.get("../BBS/list_BBS_content?action=list_partial_title&catalog=" + this.pType).then(function (response) {
        // console.log(response);
        var list = response.data.retlist;
        var list1=[];
        var l = list.length;
        for (var i = 0; i < l; i++) {
          list[i].发帖时间 = list[i].发帖时间.substring(0, 10) + " " + list[i].发帖时间.substring(11, 19);
          list[i].帖子内容 = list[i].帖子内容.substring(0, 100).replace(/\n/g, "<br>");
          list1[i]=list[i].帖子标题;
        }
        that.tilist=list1;
        that.scontent = list;
      }, function (err) { })
      this.tilist=that.tilist;
    },
    look(n){
        window.location.href = encodeURI("/BBS/open_post?posttitle="+this.tilist[n]);
    }
  }
})
if (keywordo) {
  search.dsearchout();
} else {
  search.show()
}

