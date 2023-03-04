var head = new Vue({
    el: "#head",
    data: {
        cardShow: false,
        timer: null,
        isLoad: true
    },
    methods: {
        load: function () {
            this.isLoad = !this.isLoad;
        },
        cardLoad: function () {
            clearTimeout(this.timer);  //清除延迟执行
            this.timer = setTimeout(() => {   //设置延迟执行
                this.cardShow = !this.cardShow
            }, 200);
            // this.cardShow=!this.cardShow
        }
    }
})
