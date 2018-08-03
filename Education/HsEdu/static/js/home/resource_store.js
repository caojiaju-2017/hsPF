$.extend({
    openResourceDetail: function (codeName) {
        var openId = $.cookie("OpenId");
        location.href = "/res_detail.html?Command=Open_Resource&code=" + codeName + "&openid=" + openId;
    },
});