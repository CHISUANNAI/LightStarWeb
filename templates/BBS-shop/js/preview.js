
//定义id选择器
function Id(id) {
    return document.getElementById(id);
}
function changeToop(f,m) {
    var file = Id(f);
    if (file.value == '') {
        //设置默认图片
        Id(f).src = '';
    } else {
        preImg(f,m);
    }
}
//获取input[file]图片的url Important
function getFileUrl(fileId) {
    var url;
    var file = Id(fileId);
    var agent = navigator.userAgent;
    if (agent.indexOf("MSIE") >= 1) {
        url = file.value;
    } else if (agent.indexOf("Firefox") > 0) {
        url = window.URL.createObjectURL(file.files.item(0));
    } else if (agent.indexOf("Chrome") > 0) {
        url = window.URL.createObjectURL(file.files.item(0));
    }
    return url;
}
//读取图片后预览
function preImg(fileId, imgId) {
    var imgPre = Id(imgId);
    imgPre.src = getFileUrl(fileId);
}
