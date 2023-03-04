var forum = new Vue({
    el: "#forum",
    data: {
        jy: [],
        kp: [],
        qz: [],
        jl: [],
        tilist: ["", "", "", ""],
    },
    methods: {
        selectf() {
            var that = this;
            axios.get("../BBS/list_BBS_content?action=list_partial_title&catalog=经验贴").then(function (response) {
                var a = [];
                a = response.data.retlist[0];
                a.帖子内容 = a.帖子内容.substring(0, 100) + "......";
                that.jy = a;
                that.tilist[0] = a.帖子标题;
                console.log(this.tilist[0])
            }, function (err) { })
            axios.get("../BBS/list_BBS_content?action=list_partial_title&catalog=科普贴").then(function (response) {
                var a = [];
                a = response.data.retlist[0];
                a.帖子内容 = a.帖子内容.substring(0, 100) + "......";
                that.kp = a;
                that.tilist[1] = a.帖子标题;
            }, function (err) { })
            axios.get("../BBS/list_BBS_content?action=list_partial_title&catalog=求助贴").then(function (response) {
                var a = [];
                a = response.data.retlist[0];
                a.帖子内容 = a.帖子内容.substring(0, 100) + "......";
                that.qz = a;
                that.tilist[2] = a.帖子标题
            }, function (err) { })
            axios.get("../BBS/list_BBS_content?action=list_partial_title&catalog=交流贴").then(function (response) {
                var a = [];
                a = response.data.retlist[0];
                a.帖子内容 = a.帖子内容.substring(0, 100) + "......";
                that.jl = a;
                that.tilist[3] = a.帖子标题
            }, function (err) { })
            this.tilist = that.tilist;
        },
        look(n) {
            console.log(this.tilist)
            window.location.href = encodeURI("/BBS/open_post?posttitle=" + this.tilist[n]);
        }
    }
})
forum.selectf();
// 义卖展示
// var goods = new Vue({
//     el: "#shop",
//     data: {
//         goodslist: [],
//     },
//     methods: {
//         showgoods() {
//             var that = this;
//             axios.post("../Charity_sale/list_all_items", {}).then(
//                 function (response) {
//                     var list = response.data.allitem;
//                     console.log(list);
//                     that.goodslist = list;
//                     console.log(that.goodslist[0])
//                 },
//                 function (err) {
//                     console.log(err);
                    
//                 }
//             )
//             this.goodslist = that.goodslist;
//         }
//     }
// })
// goods.showgoods();
// console.log(goods.goodslist)