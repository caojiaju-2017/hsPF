var openid;
window.onload=function()
{
    var docHeight = $(document).height();
    $("#middle_tree_cell").height(docHeight - 340);
};

$(document).ready(function(e) {
    openid = $.cookie('WX_OpenId');
    // $('body').on('touchmove',function(event){event.preventDefault();});
    // $('#middle_tree_cell').addEventListener('touchmove', function(e) {e.stopPropagation();}, false);

    //520
    var docHeight = $(document).height();
    $("#middle_tree_cell").height(docHeight - 340);

    // alert("afd");
    //设置 title
    kb_select_index = parseInt($.cookie("kb_select_index"));
    xl_select_index = parseInt($.cookie("xl_select_index"));
    xn_select_index = parseInt($.cookie("xn_select_index"));
    xq_select_index = parseInt($.cookie("xq_select_index"));

    if (kb_select_index < 0 || xl_select_index < 0 || xn_select_index < 0 || xq_select_index < 0)
    {
        alert("开始游戏前，请先设置范围，并保存后继续");
        location.href = "game_setting.html";
        return;
    }
    if (typeof(kb_select_index) == "undefined" || typeof(xl_select_index) == "undefined" || typeof(xn_select_index) == "undefined" || typeof(xq_select_index) == "undefined")
    {
        alert("开始游戏前，请先设置范围，并保存后继续");
        location.href = "game_setting.html";
        return;
    }

    if (isNaN(kb_select_index) || isNaN(xl_select_index) || isNaN(xn_select_index) || isNaN(xq_select_index))
    {
        alert("开始游戏前，请先设置范围，并保存后继续");
        location.href = "game_setting.html";
        return;
    }


    var kbstring = $.getTitleItemText(0,kb_select_index);
    var xlstring = $.getTitleItemText(1,xl_select_index);
    var xnstring = $.getTitleItemText(2,xn_select_index);
    var xqstring = $.getTitleItemText(3,xq_select_index);

    $("#map_title").text(kbstring + "-" + xlstring + "-" + xnstring + "-" + xqstring);
});

$.extend({
    test: function () {
        //location.href = "game_setting.html";
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

    checkConfig: function (haveconfig) {
        if (haveconfig == 0)
        {
            alert("用户未设置检测范围");
        }
    },
    getTitleItemText: function (type,index) {
        if (type == 0)
        {
            if (index == 0)
            {
                return "北师大";
            }
            else if(index == 1)
            {
                return "人教版";
            }
            else if (index == 2)
            {
                return "苏教版"
            }
        }
        else if(type == 1)
        {
            if (index == 0)
            {
                return "高中";
            }
            else if(index == 1)
            {
                return "初中";
            }
            else if (index == 2)
            {
                return "小学"
            }
        }
        else if(type == 2)
        {
            if (index == 1)
            {
                return "一年级";
            }
            else if(index == 2)
            {
                return "二年级";
            }
            else if (index == 3)
            {
                return "三年级"
            }
            else if (index == 4)
            {
                return "四年级";
            }
            else if(index == 5)
            {
                return "五年级";
            }
            else if (index == 6)
            {
                return "六年级"
            }
            else if (index == 7)
            {
                return "七年级";
            }
            else if(index == 8)
            {
                return "八年级";
            }
            else if (index == 9)
            {
                return "九年级"
            }
            else if (index == 10)
            {
                return "高一";
            }
            else if(index == 11)
            {
                return "高二";
            }
            else if(index == 12)
            {
                return "高三";
            }

        }
        else if(type == 3)
        {
            if (index == 0)
            {
                return "上学期";
            }
            else if(index == 1)
            {
                return "下学期";
            }
        }

    },
    startGame: function (unitcode) {
        location.href = "gamming.html?unitcode=" + unitcode;
    },
    goBackPage: function () {
        // alert("fdsaf");
        history.go(-1);
    },
});