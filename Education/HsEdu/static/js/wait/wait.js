var appID = "wx75e53a9db8f89fce";
var appsecret = "c45eefc37a8a0889fa4ebe020a9eb696";

window.onload=function()
{
    $.weixinLogin();
};

$(document).ready(function()
{
});

$.extend({
    weixinLogin:function () {
    			  $.cookie("BrowserIndex",1); 
            var urlCode = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=" + appID + "&redirect_uri=http%3a%2f%2fwww.h-sen.com&response_type=code&scope=snsapi_userinfo&state=abc#wechat_redirect";
            location.href = urlCode;
        }
});
