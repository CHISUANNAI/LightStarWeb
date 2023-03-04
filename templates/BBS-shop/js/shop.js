
var a ;
var islogin=document.getElementById("islogin").innerText;
if (islogin) {
  a = document.getElementById("session").innerText;
}
else{
  a="morenzhi";
}

var goods = new Vue({
    el: "#goods",
    data: {
        goodslist: [],
    },
    methods: {
        showgoods() {
            var that = this;
            axios.post("../Charity_sale/list_all_items", {}).then(
                function (response) {
                    var list = response.data.allitem;

                    that.goodslist = list;
                },
                function (err) {
                    console.log(err);
                }
            )
            this.goodslist = that.goodslist;
        }
    }
})
goods.showgoods();
// 发起义卖
// userid（用户id）、childrenname（儿童姓名）、itemname（商品名称）、itemdescription（商品介绍）、price（价格，int）
console.log(a);

$(function(){
	/** 验证文件是否导入成功  */
	$("#form1").ajaxForm(function(data){  
        if(data.ret==1){
            alert(data.msg);}
        else if(data.ret==2){
                alert(data.msg);
                window.location.href("/user_data/login/")
            }
        else{
            alert("您已成功发布该商品！")
        }})

        });


var dosell = new Vue({
    el: "#dosell",
    data: {
        userid: a,
    },
    methods: {
        // uploadinfo() {
        //     var that = this;
        //     axios.post("../Charity_sale/additem", {
        //         userid: this.userid,
        //         childrenname: this.childrenname,
        //         itemname: this.itemname,
        //         itemdescription: this.itemdescription,
        //         price: this.price,
        //     }).then(
        //         function (response) {
        //             console.log(response)
        //         },
        //         function (err) {
        //             console.log(err);
        //         }

        //     )
            //     axios.post("../Charity_sale/uploadimage", {
            //         userid:this.userid,
            //         childrenname:this.childrenname,
            //         itemname:this.itemname,
            //         itemdescription:this.itemdescription,
            //         price:this.price,
            //     }).then(
            //         function (response) {
            //            console.log(response);
            //         },
            //         function (err) {
            //             console.log(err);
            //         }

            //     )
            // }
        }

    })
// 图片控制
window.onload = $(function () {
    $('.goodsli').jqthumb({
        width: 200,
        height: 200,
        after: function (imgObj) {
            imgObj.css('opacity', 0).animate({ opacity: 1 }, 1000);
        }
    });
});
