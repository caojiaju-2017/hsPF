var isFinishLoad = false;
var currentPageIndex = 0;
var currentPageSize = 10;
var queryLock = false;
var openid;
var OneWordTmpl= '<div class="error_item" onclick="$.viewErrorWord(\'{words}\')">\n' +
    '                    {words}&nbsp&nbsp {meaning}\n' +
    '                        <img src="/static/Images/game/view_word.png"\n' +
    '                             style="float: right;margin-right: 20px;height: 60px;width: 60px;margin-top: 20px">\n';
window.onload=function()
{

};

$(document).ready(function(e) {
    openid = $.cookie('WX_OpenId');
    // $('body').on('touchmove',function(event){event.preventDefault();});
    // $('#error_word_item').on('touchmove', function(e) {e.stopPropagation();}, false);

    //520
    var docHeight = $(document).height();
    $("#error_word_item").height(docHeight - 500);

    $.initLoading();

    var nScrollHight = 0; //滚动距离总长(注意不是滚动条的长度)
        var nScrollTop = 0;   //滚动到的当前位置
        var nDivHight = $("#error_word_item").height();
        $("#error_word_item").scroll(function(){
          nScrollHight = $(this)[0].scrollHeight;
          nScrollTop = $(this)[0].scrollTop;
          if(nScrollTop + nDivHight >= nScrollHight)
            if (!isFinishLoad && !queryLock) {
                queryLock = true;
                // 加载数据
                $.seartErrorBook();
            }
          });

    // $(window).scroll(function () {
    //     var srollPos = $(window).scrollTop();
    //     var documentHd = $(document).height();
    //     var winHd = $(window).height();
    //
    //
    //     totalheight = parseFloat($(window).height()) + parseFloat(srollPos);
    //
    //     if (srollPos + winHd > documentHd * 0.9) {
    //         // alert(currentType);
    //
    //         if (!isFinishLoad && !queryLock) {
    //             queryLock = true;
    //             // 加载数据
    //             $.seartErrorBook();
    //         }
    //
    //     }
    // });

    // 首次主动发起查询
    queryLock = true;
    $.seartErrorBook();

});

$.extend({
    test: function () {
        //location.href = "game_setting.html";
    },

    initLoading:function () {
        $("body").append("<!-- loading -->" +
            "<div class='modal fade' id='loading' tabindex='-1' role='dialog' aria-labelledby='myModalLabel' data-backdrop='static'>" +
            "<div class='modal-dialog' role='document'>" +
            "<div class='modal-content'>" +
            "<div class='modal-header'>" +
            "<h4 class='modal-title' id='myModalLabel' style='font-size: 32px'>提示</h4>" +
            "</div>" +
            "<div id='loadingText' class='modal-body' style='font-size: 36px'>" +

            "数据处理中，请稍候 . . ." +
            "</div>" +
            "</div>" +
            "</div>" +
            "</div>"
        );
    },
    viewErrorWord: function (word) {
        // var openid = $.cookie('WX_OpenId');
        // openid = "abcdef";
        location.href = "game_view_word.html?wcode=" + word + "&openid=" + openid;
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

    seartErrorBook: function () {
        $("#loading").modal("show");
        // var openid = $.cookie('WX_OpenId');
        // openid = "abcdef";

        var cmdString = "/api/game/?Command=Open_Error_Book&pageindex={0}&pagesize={1}&openid={2}";
        var rtnCmd = $.StringFormat(cmdString, currentPageIndex, currentPageSize,openid);
        // alert(cmdString);
        // 提取用户名
        $.get(rtnCmd,
            function (data) {
            $("#loading").modal("hide");
                // 检查查询状态
                var ErrorId = data.ErrorId;
                var Result = data.Result;
                var Datas = Result;
                if (ErrorId == 200) {

                    if (Datas.length <= 0 || Datas.length < currentPageSize) {
                        isFinishLoad = true;
                    }

                    currentPageIndex = currentPageIndex + 1;
                    for (i = 0; i < Datas.length; i++) {
                        var oneCode1 = Datas[i];

                        var abcTemp = {};
                        abcTemp["words"] = oneCode1.wcode;
                        abcTemp["meaning"] = oneCode1.meaning;

                        var oneT = $("#error_word_item").html();

                        $("#error_word_item").html(oneT + $.format(OneWordTmpl, abcTemp));
                    }
                    queryLock = false;
                }

            },
            "json");//这里返回的类型有：json,html,xml,text
    },
    goBackPage: function () {
        // alert("fdsaf");
        history.go(-1);
    },
});