var currentword = ""
var haveprev = -1;
var havenext = -1;
var openid;
window.onload=function()
{
    // var docHeight = $(document).height();
    // $("#word_card").height(docHeight - 500);
    //
    // var word_card_hd = docHeight - 500;
    //
    // $("#word_sentence").height(430);
};

$(document).ready(function(e) {
    // $('body').on('touchmove',function(event){event.preventDefault();});
    // $('#word_meaning').addEventListener('touchmove', function(e) {e.stopPropagation();}, false);
    // $('#word_sentence').addEventListener('touchmove', function(e) {e.stopPropagation();}, false);

    var docHeight = $(document).height();
    $("#word_card").height(docHeight - 500);
    var word_card_hd = docHeight - 500;
    $("#word_sentence").height(word_card_hd - 430);


    openid = $.cookie('WX_OpenId');
    //520
    $.initLoading();

    var docHeight = $(document).height();
    $("#word_card").height(docHeight - 500);

    var word_card_hd = docHeight - 500;

    $("#word_sentence").height(word_card_hd - 430);

    // $.setIcon();
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

    initIcon: function (prv,next) {
        //location.href = "game_setting.html";
        haveprev = prv;
        havenext = next;
    },
    setIcon: function () {
        if (haveprev < 0)
        {
            $("#btnprev").attr('src','/static/Images/game/preview_0.png');
        }
        else
        {
            $("#btnprev").attr('src','/static/Images/game/preview.png');
        }
        if (havenext < 0)
        {
            $("#btnnext").attr('src','/static/Images/game/next_0.png');
        }
        else
        {
            $("#btnnext").attr('src','/static/Images/game/next.png');
        }
    },
    readWord: function (word) {
        //location.href = "game_setting.html";
        if (currentword == "")
        {
            currentword = word;
        }
        // alert("fd");
        var soundurl = "http://dict.youdao.com/dictvoice?audio=" + currentword;

        var audio = document.getElementsByTagName('audio')[0];
        var source = document.getElementsByTagName('source')[0];
        audio.src = soundurl;
        audio.paused && (audio.play());
    },
    getIPreWord: function (word) {
        if (haveprev < 0)
        {
            return;
        }
        $.getWord(word,-1);
    },
    iRemeber: function (word) {
        //location.href = "game_setting.html";
    },
    getINextWord: function (word) {
        // alert(havenext);
        if (havenext < 0)
        {
            return;
        }
        $.getWord(word,1);
    },
    getWord: function (word,type) {
        var rtnCmd = "/api/game/?Command=Get_Word_Info";

        // var openid = $.cookie('WX_OpenId');
        // openid = "abcdef";

        if (currentword == "")
        {
            currentword = word;
        }

        var cmdString = "/api/game/?Command=Get_Word_Info&wcode={0}&openid={1}&offset={2}";
        var rtnCmd = $.StringFormat(cmdString, currentword, openid,type);
        // alert(cmdString);
        // 提取用户名
        $("#loading").modal("show");
        $.get(rtnCmd,
            function (data) {
                $("#loading").modal("hide");
                // 检查查询状态
                var ErrorId = data.ErrorId;
                var Result = data.Result;
                var Datas = Result;
                if (ErrorId == 200) {
                    $("#error_spell").text(Datas.mykey);
                    $("#right_spell").text(Datas.wcode);
                    $("#word_meaning").html(Datas.meaning);
                    $("#word_sentence").html(Datas.sentence);

                    currentword = Datas.wcode
                    haveprev = Datas.havePre;
                    havenext = Datas.haveNext;

                    $.setIcon();
                }

            },
            "json");//这里返回的类型有：json,html,xml,text
    },
    goBackPage: function () {
        history.go(-1);
    },
});