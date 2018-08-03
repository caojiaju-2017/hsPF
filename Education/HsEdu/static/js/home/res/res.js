$.extend({
    contactNow: function (codeName) {
        // alert("现在给客服拨打电话？");
    },

    buyResource: function (codeName,type) {
        if (type == 0)
        {
            window.location ="https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx75e53a9db8f89fce&redirect_uri=http%3a%2f%2fwww.h-sen.com%2fpayCall.html%3frescode%3d" + codeName + "&response_type=code&scope=snsapi_base&state=#wechat_redirect";
        }
        else
        {
            location.href = './order_detail_info.html?Command=View_Order&code=' + codeName;
        }


    },
    openResource: function (codeName) {
        // alert($("#video_src").attr('src'));
        // $("#video_src").attr("src","http://19e237597p.iok.la:8081/media/video/1.mp4");
        $("#example_video_1").attr("src","http://19e237597p.iok.la:8081/media/video/1.mp4");//更新url
        $("#example_video_1").attr("autoplay","true");//直接播放
    },

    ViewRemark: function (codeName) {
    	  var openId = $.cookie("OpenId");
    		location.href = './view_remark.html?Command=View_Remark&code=' + codeName + "&openid=" + openId;
    },
    clickItem:function () {
          alert("好资源，便宜卖，你懂得；想试看，请关注公众号： hansenjiaoyucd！");
        // location.href = "https://pan.baidu.com/s/1c2Vv0mG";
    },
});