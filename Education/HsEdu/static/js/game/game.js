var openidTemp;
var overFlag = 0;
$(document).ready(function(e) {
    // $.cookie("WX_OpenId","oQE6Bt6PVtEL9XzfDSI_Xj0Ed0e8");
    openidTemp = $.cookie('WX_OpenId');

    $('body').on('touchmove',function(event){event.preventDefault();});

});

$.extend({
    get26Letter:function () {
      var letterArray = new Array(26);
        letterArray[0] = "A";
          			letterArray[00] = 'A';
      letterArray[01] = 'B';
      letterArray[02] = 'C';
      letterArray[03] = 'D';
      letterArray[04] = 'E';
      letterArray[05] = 'F';
      letterArray[06] = 'G';
      letterArray[07] = 'H';
      letterArray[08] = 'I';
      letterArray[09] = 'J';
      letterArray[10] = 'K';
      letterArray[11] = 'L';
      letterArray[12] = 'M';
      letterArray[13] = 'N';
      letterArray[14] = 'O';
      letterArray[15] = 'P';
      letterArray[16] = 'Q';
      letterArray[17] = 'R';
      letterArray[18] = 'S';
      letterArray[19] = 'T';
      letterArray[20] = 'U';
      letterArray[21] = 'V';
      letterArray[22] = 'W';
      letterArray[23] = 'X';
      letterArray[24] = 'Y';
      letterArray[25] = 'Z';

      return letterArray;
    },
    StringFormat: function () {
        if (arguments.length == 0)
            return null;
        var str = arguments[0];
        for (var i = 1; i < arguments.length; i++) {
            var re = new RegExp('\\{' + (i - 1) + '\\}', 'gm');
            str = str.replace(re, arguments[i]);
        }
        return str;
    },
    format: function (source, args) {
        var result = source;
        if (typeof(args) == "object") {
            if (args.length == undefined) {
                for (var key in args) {
                    if (args[key] != undefined) {
                        var reg = new RegExp("({" + key + "})", "g");
                        result = result.replace(reg, args[key]);
                    }
                }
            } else {
                for (var i = 0; i < args.length; i++) {
                    if (args[i] != undefined) {
                        var reg = new RegExp("({[" + i + "]})", "g");
                        result = result.replace(reg, args[i]);
                    }
                }
            }
        }
        return result;
    },

    openGameSetting: function () {
        if (overFlag == 1)
        {
            alert("您的账号已过期，您可以选择分享游戏获得减免（请查看详情），或者可直接支付赞助开发者")
            return;
        }
        location.href = "game_setting.html";
    },
    setUserInfo: function (openid, username, headimg) {
            openidTemp = openid;
            $.cookie("WX_OpenId", openid);
            $.cookie("WxName", username);
            $.cookie("HeadImg", headimg);

            //    设置头像数据
            $("#uName").text(username);
            $("#user_head").attr('src', headimg);
        },
    openErrorBook: function () {
        if (overFlag == 1)
        {
            alert("您的账号已过期，您可以选择分享游戏获得减免（请查看详情），或者可直接支付赞助开发者")
            return;
        }
        location.href = "game_error_book.html";
    },

    StartGame: function () {
        if (overFlag == 1)
        {
            alert("您的账号已过期，您可以选择分享游戏获得减免（请查看详情），或者可直接支付赞助开发者")
            return;
        }
        // var openid = $.cookie('WX_OpenId');
        // openid = "abcdef";
        // alert(openidTemp);
        location.href = "game_map.html?openid=" + openidTemp;
    },

    notifyServerSuccess:function () {
        // alert("notifyServerSuccess")
        var rtnCmd = "/api/game/?Command=Share_Success";

        $.post(rtnCmd, {openid: openidTemp},
            function (data)
            {
            },
            "json");//这里返回的类型有：json,html,xml,text
    },

    setOverDate:function (flag) {
        overFlag = flag;
    },
    startCharge:function () {
        codeName = "GAME_PAY";
        window.location ="https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx75e53a9db8f89fce&redirect_uri=http%3a%2f%2fwww.h-sen.com%2fpayCall.html%3frescode%3d" + codeName + "%26openid%3d" + openidTemp + "&response_type=code&scope=snsapi_base&state=#wechat_redirect";
    },
});