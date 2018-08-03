var kb_select_index = -1;
var xl_select_index = -1;
var xn_select_index = -1;
var xq_select_index = -1;
var openid;
window.onload=function()
{
    // 载入本地配置
    kb_select_index = parseInt($.cookie("kb_select_index"));
    // alert(kb_select_index);
    if (!kb_select_index && kb_select_index != 0)
    {
        kb_select_index = -1;
    }
    else
    {
        $.selectItem(0,"", kb_select_index);
    }

    xl_select_index = parseInt($.cookie("xl_select_index"));
    // alert(xl_select_index);
    if (!xl_select_index && xl_select_index != 0)
    {
        xl_select_index = -1;
    }
    else
    {
        $.selectItem(1,"", xl_select_index);
    }

    xn_select_index = parseInt($.cookie("xn_select_index"));
    // alert(xn_select_index);
    if (!xn_select_index && xn_select_index != 0)
    {
        xn_select_index = -1;
    }
    else
    {
        $.selectItem(2,"", xn_select_index);
    }

    xq_select_index = parseInt($.cookie("xq_select_index"));
    // alert(xq_select_index);
    if (!xq_select_index && xq_select_index != 0)
    {
        xq_select_index = -1;
    }
    else
    {
        $.selectItem(3,"", xq_select_index);
    }
    // 请求用户配置数据
};

$(document).ready(function(e) {
    openid = $.cookie('WX_OpenId');
    // $('body').on('touchmove',function(event){event.preventDefault();});
    // $('#setting_item_container_kb').addEventListener('touchmove', function(e) {e.stopPropagation();}, false);
    // $('#setting_item_container_xl').addEventListener('touchmove', function(e) {e.stopPropagation();}, false);
    // $('#setting_item_container_xn').addEventListener('touchmove', function(e) {e.stopPropagation();}, false);

    //520
    var docHeight = $(document).height();
    $("#setting_item_container_kb").height(docHeight - 660);

    $("#setting_item_container_xl").height(docHeight - 660);

    $("#setting_item_container_xn").height(docHeight - 660);

    // $("#setting_item_container_xn_chuzhong").height(docHeight - 660);
    //
    // $("#setting_item_container_xn_gaozhong").height(docHeight - 660);

    $("#setting_item_container_xq").height(docHeight - 660);


});

$.extend({
    test: function () {
        location.href = "game_setting.html";
    },
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

    selectItem: function (typeid, itemtext,iteminx) {
        // alert(typeid);
        if (typeid == 0) // 课标
        {
            if (iteminx == 0)
            {
                $("#kb_item_" + 0).attr("src","/static/Images/game/select.png");
                $("#kb_item_" + 1).attr("src","/static/Images/game/unselect.png");
                $("#kb_item_" + 2).attr("src","/static/Images/game/unselect.png");
            }
            else if(iteminx == 1)
            {
                $("#kb_item_" + 0).attr("src","/static/Images/game/unselect.png");
                $("#kb_item_" + 1).attr("src","/static/Images/game/select.png");
                $("#kb_item_" + 2).attr("src","/static/Images/game/unselect.png");
            }
            else
            {
                $("#kb_item_" + 0).attr("src","/static/Images/game/unselect.png");
                $("#kb_item_" + 1).attr("src","/static/Images/game/unselect.png");
                $("#kb_item_" + 2).attr("src","/static/Images/game/select.png");
            }

            kb_select_index = iteminx;
        }
        else if (typeid == 1) //学历
        {
            if (iteminx == 0)
            {
                $("#xl_item_" + 0).attr("src","/static/Images/game/select.png");
                $("#xl_item_" + 1).attr("src","/static/Images/game/unselect.png");
                $("#xl_item_" + 2).attr("src","/static/Images/game/unselect.png");
            }
            else if(iteminx == 1)
            {
                $("#xl_item_" + 0).attr("src","/static/Images/game/unselect.png");
                $("#xl_item_" + 1).attr("src","/static/Images/game/select.png");
                $("#xl_item_" + 2).attr("src","/static/Images/game/unselect.png");
            }
            else
            {
                $("#xl_item_" + 0).attr("src","/static/Images/game/unselect.png");
                $("#xl_item_" + 1).attr("src","/static/Images/game/unselect.png");
                $("#xl_item_" + 2).attr("src","/static/Images/game/select.png");
            }

            xl_select_index = iteminx;
        }
        else if (typeid == 2) // 学年
        {
            for (var index = 0; index < 12; index ++)
            {
                $("#xn_item_div_" + index).hide();
                $("#xn_item_" + index).attr("src","/static/Images/game/unselect.png");
            }
            if (iteminx < 6)
            {
                for (var index = 0; index < 6; index ++)
                {
                    $("#xn_item_div_" + index).show();
                }
            }
            else if (iteminx < 9)
            {
                for (var index = 6; index < 9; index ++)
                {
                    $("#xn_item_div_" + index).show();
                }
            }
            else
            {
                for (var index = 9; index < 12; index ++)
                {
                    $("#xn_item_div_" + index).show();
                }
            }
            $("#xn_item_" + iteminx).attr("src","/static/Images/game/select.png");
            $("#xn_item_div_" + iteminx).show();
            xn_select_index = iteminx;
        }
        else if (typeid == 3) // 学期
        {
            if (iteminx == 0)
            {
                $("#xq_item_" + 0).attr("src","/static/Images/game/select.png");
                $("#xq_item_" + 1).attr("src","/static/Images/game/unselect.png");
            }
            else
            {
                $("#xq_item_" + 0).attr("src","/static/Images/game/unselect.png");
                $("#xq_item_" + 1).attr("src","/static/Images/game/select.png");
            }


            xq_select_index = iteminx;
        }
    },
    switchSetting: function (type) {
        // 0 ->setting_item_container_kb
        if (type == "0")
        {
            $("#setting_item_container_kb").show();
            $("#setting_item_container_xl").hide();
            $("#setting_item_container_xn").hide();
            // $("#setting_item_container_xn_chuzhong").hide();
            // $("#setting_item_container_xn_gaozhong").hide();
            $("#setting_item_container_xq").hide();

            // 设置字体和背景
            $("#kb_item").css("background-color","#C69533");
            $("#kb_item").css("color","#ffffff");
            $("#xl_item").css("background-color","#C7F5FD");
            $("#xl_item").css("color","#000000");
            $("#xn_item").css("background-color","#C7F5FD");
            $("#xn_item").css("color","#000000");
            $("#xq_item").css("background-color","#C7F5FD");
            $("#xq_item").css("color","#000000");
        }
        else if (type == "1")
        {
            // alert(kb_select_index);
            if (kb_select_index <0 )
            {
                $.switchSetting(0);
                alert('未选中课标')
                return ;
            }
            $("#setting_item_container_kb").hide();

            $("#setting_item_container_xl").show();
            $("#setting_item_container_xn").hide();
            // $("#setting_item_container_xn_chuzhong").hide();
            // $("#setting_item_container_xn_gaozhong").hide();
            $("#setting_item_container_xq").hide();

            // 设置字体和背景
            $("#kb_item").css("background-color","#C7F5FD");
            $("#kb_item").css("color","#000000");
            $("#xl_item").css("background-color","#C69533");
            $("#xl_item").css("color","#ffffff");
            $("#xn_item").css("background-color","#C7F5FD");
            $("#xn_item").css("color","#000000");
            $("#xq_item").css("background-color","#C7F5FD");
            $("#xq_item").css("color","#000000");
        }
        else if(type == 2) // 学年
        {
            if(xl_select_index < 0)
            {
                $.switchSetting(1);
                alert("需要先选中学历");
                return;
            }
            $("#setting_item_container_kb").hide();

            $("#setting_item_container_xl").hide();

            $("#setting_item_container_xn").show();
            // $("#setting_item_container_xn_chuzhong").hide();
            // $("#setting_item_container_xn_gaozhong").hide();
                $("#xn_item_div_0").hide();
                $("#xn_item_div_1").hide();
                $("#xn_item_div_2").hide();
                $("#xn_item_div_3").hide();
                $("#xn_item_div_4").hide();
                $("#xn_item_div_5").hide();
                $("#xn_item_div_6").hide();
                $("#xn_item_div_7").hide();
                $("#xn_item_div_8").hide();
                $("#xn_item_div_9").hide();
                $("#xn_item_div_10").hide();
                $("#xn_item_div_11").hide();

            if(xl_select_index == 0)
            {
                $("#xn_item_div_9").show();
                $("#xn_item_div_10").show();
                $("#xn_item_div_11").show();
            }
            else if(xl_select_index == 1)
            {
                $("#xn_item_div_6").show();
                $("#xn_item_div_7").show();
                $("#xn_item_div_8").show();
            }
            else
            {
                $("#xn_item_div_0").show();
                $("#xn_item_div_1").show();
                $("#xn_item_div_2").show();
                $("#xn_item_div_3").show();
                $("#xn_item_div_4").show();
                $("#xn_item_div_5").show();
            }


            $("#setting_item_container_xq").hide();

            // 设置字体和背景
            $("#kb_item").css("background-color","#C7F5FD");
            $("#kb_item").css("color","#000000");
            $("#xl_item").css("background-color","#C7F5FD");
            $("#xl_item").css("color","#000000");
            $("#xn_item").css("background-color","#C69533");
            $("#xn_item").css("color","#ffffff");
            $("#xq_item").css("background-color","#C7F5FD");
            $("#xq_item").css("color","#000000");
        }
        else if (type == 3)
        {
            if(xn_select_index < 0)
            {
                $.switchSetting(2);
                alert("需要先选中学年");
                return;
            }


            $("#setting_item_container_kb").hide();

            $("#setting_item_container_xl").hide();
            $("#setting_item_container_xn").hide();
            // $("#setting_item_container_xn_chuzhong").hide();
            // $("#setting_item_container_xn_gaozhong").hide();
            $("#setting_item_container_xq").show();

            // 设置字体和背景
            $("#kb_item").css("background-color","#C7F5FD");
            $("#kb_item").css("color","#000000");
            $("#xl_item").css("background-color","#C7F5FD");
            $("#xl_item").css("color","#000000");
            $("#xn_item").css("background-color","#C7F5FD");
            $("#xn_item").css("color","#000000");
            $("#xq_item").css("background-color","#C69533");
            $("#xq_item").css("color","#ffffff");
        }
    },
    goBackPage: function () {
        // alert("fdsaf");
        history.go(-1);
    },
    saveSetting: function () {
        if (kb_select_index < 0)
        {
            alert("未选中课标");
            return;
        }

        if (xl_select_index < 0)
        {
            alert("未选中学历");
            return;
        }

        if (xn_select_index < 0)
        {
            alert("未选中学年");
            return;
        }

        if (xq_select_index < 0)
        {
            alert("未选中学科");
            return;
        }

    //    刷新cookie
        $.cookie("kb_select_index",kb_select_index);
        $.cookie("xl_select_index",xl_select_index);
        $.cookie("xn_select_index",xn_select_index);
        $.cookie("xq_select_index",xq_select_index);

    //    调用存储接口
    //     alert("Success");
    //
    //     history.go(-1);
        var rtnCmd = "/api/game/?Command=Save_Setting";

        // var openid = $.cookie('WX_OpenId');
        // openid = "abcdef";


        $.post(rtnCmd, {openid: openid, kbindex: kb_select_index, xlindex: xl_select_index,xnindex:xn_select_index,xqindex:xq_select_index},
            function (data)
            {

                var  ErrorId = data.ErrorId;
                var  Result = data.Result;

                if (ErrorId == 200)
                {
                    alert("Success!")
                   history.go(-1);
                }
                else
                {
                    alert(data.ErrorInfo);
                }
            },
            "json");//这里返回的类型有：json,html,xml,text
    },
});