var openid;
var wordLists ;
var currentIndex = 0;
var currentUnit ;
var openId ;
var clickArray = new Array(30);
var deepthDiv = "<div style=\"float: left;width: 80px;height: 80px;margin-left: 10px;font-size: 38px;\">1/20</div>";
var imgTmp = "<img src=\"/static/Images/game/back.png\" onclick=\"$.backspaceLetter()\" style=\"width: 80px;height: 80px;margin-top: 20px;float: right;margin-right: 20px\">";
$(document).ready(function(e) {
    openid = $.cookie('WX_OpenId');
    $('body').on('touchmove',function(event){event.preventDefault();});
    $.initLoading();

//    canvas_pannel
    var docHeight = $(document).height();
    $("#canvas_pannel").height(docHeight - 620);

    $(".word_div").height((docHeight - 620) / 7 - 20);
     // $(".word_div").css('line-height',(docHeight - 620) / 7 - 20);

        // $('.word_div').height((docHeight - 620) / 7 - 10);

    // openId  = "abcdef";
    //$.initWord('sentence',0,25);
});

$.extend({
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

    windowLoading: function (unitcode) {
        currentUnit = unitcode;

        $("#loading").modal("show");
        // alert(unitcode);
        // alert(openid);
        var cmdString = "/api/game/?Command=Get_Unit_Code&unitcode={0}&openid={1}";
        // alert(cmdString);

        var rtnCmd = $.StringFormat(cmdString, unitcode,openid);
        // alert(cmdString);
        // 提取用户名
        // alert(rtnCmd);
        $.get(rtnCmd,
            function (data) {
                $("#loading").modal("hide");
                // 检查查询状态
                var ErrorId = data.ErrorId;
                var Result = data.Result;
                var Datas = Result;
                // alert(Datas.length);
                if (ErrorId == 200) {
                    $("#loading").modal("hide");
                    wordLists = Datas.unitwords;
                    $.loadWord();
                }
            },
            "json");//这里返回的类型有：json,html,xml,text
    },
    loadWord:function () {
        var wordOne = wordLists[currentIndex];
        $("#left_control").html(wordOne.meaning);

        if (wordLists.length - 1 == 0)
        {
            $("#next_button").hide();
            $("#switch_ctrl").text("完成");
        }

        $("#step_info").html((currentIndex + 1) + "/" + wordLists.length);

        $.initWord(wordOne.wcode,0,25);
    },
    terminalTest:function () {
        location.href = "game_home.html";
    },
    playSound:function () {
        var wordOne = wordLists[currentIndex];
        var soundurl = "http://dict.youdao.com/dictvoice?audio=" + wordOne.wcode;

        var audio = document.getElementsByTagName('audio')[0];
        var source = document.getElementsByTagName('source')[0];
        audio.src = soundurl;
        audio.paused && (audio.play());
    },
    goNext:function () {
        currentIndex = currentIndex + 1;

        $("#step_info").html((currentIndex + 1) + "/" + wordLists.length);

        // 向服务器推送检测结果
        var wordTemp = wordLists[currentIndex - 1];
        var mykey = $("#input_div").text();
        $.sendResult(wordTemp.wcode, mykey);

        if (currentIndex == wordLists.length - 1)
        {
            $("#next_button").hide();
            $("#switch_ctrl").text("完成");
        }
        else if (currentIndex > wordLists.length - 1)
        {
            location.href = "game_result.html?unitcode=" + currentUnit + "&openid=" + openId;
            return;
        }
        var wordOne = wordLists[currentIndex];
        $("#left_control").html(wordOne.meaning);

        // 清空选中状态
        for (var index = 0 ; index < clickArray.length; index ++)
        {
            $(clickArray[index]).css("background-color","#6682c2");
            clickArray[index] = "";
        }

        // 清空输入状态
        $("#input_div").html("");

        $.initWord(wordOne.wcode,0,25);
    },
    sendResult:function (right,error) {
        // if (right == error || error == "" || typeof (error) == "undefined")
        // {
        //     return;
        // }
        // if (right == error)
        // {
        //     return;
        // }
        $("#loading").modal("show");

        // var openid = $.cookie('WX_OpenId');
        // openid = "abcdef";

        var rtnCmd = "/api/game/?Command=Write_Error_Book";

        $.post(rtnCmd, {openid: openid, right: right, error: error},
            function (data)
            {
                var  ErrorId = data.ErrorId;
                var  Result = data.Result;

                if (ErrorId == 200)
                {
                    $("#loading").modal("hide");
                }
                else
                {
                    alert(data.ErrorInfo);
                }
            },
            "json");//这里返回的类型有：json,html,xml,text
    },
    clickLetter:function (letter,divid) {
        // alert(letter);
        // $(divid).css("background-color","#FF6600");
        // $(divid).css("color","#ffffff");

        // (new Beep(22050)).play(500, 0.2, [Beep.utils.amplify(8000)]);

        var existHtml = $("#input_div").text();
        if (typeof(existHtml) == "undefined")
        {
            existHtml = "";
        }
        clickArray[existHtml.length] = divid;
        var letter = $("#" + divid).text();
        letter = letter.toLowerCase();
        $("#input_div").html(existHtml + letter );
    },
    backspaceLetter:function () {
        var existHtml = $("#input_div").text();
        var existSize = existHtml.length;
        // var buttonId = clickArray[existSize - 1];

        // $(buttonId).css("background-color","#2D93CA");
        $("#input_div").html(existHtml.substr(0,existSize - 1));
    },
    initWord : function (word,min,max) {
        // 播放语音
        var soundurl = "http://dict.youdao.com/dictvoice?audio=" + word;

        var audio = document.getElementsByTagName('audio')[0];
        var source = document.getElementsByTagName('source')[0];
        audio.src = soundurl;
        audio.paused && (audio.play());

        return;
        // 得到随机字母
        // 决定获取字母个数
        min = parseInt(Math.random() * (max - word.length*2 + 1) + word.length*2);
        var letterSize = parseInt(Math.random() * (max - min + 1) + min);

        // 定义字母字典
        var letterArray = new Array(letterSize);
        var letter26Array = $.get26Letter();

        var wordLarg = word.toUpperCase();
        for (var index = 0 ; index < wordLarg.length; index++)
        {
            letterArray[index] = wordLarg[index];

            // 从26个字母中删除
            letter26Array.splice($.inArray(wordLarg[index],letter26Array),1);
        }

        var radomCount = letterSize - wordLarg.length;
        min = 0;
        max = max - wordLarg.length;
        for (var index = 0 ; index < radomCount ; index++)
        {
            var tempIndex = index+ wordLarg.length;
            var radomPos = parseInt(Math.random() * (max - min + 1) + min);

            letterArray[tempIndex] = letter26Array[radomPos];
            letter26Array.splice($.inArray(letter26Array[radomPos],letter26Array),1);
            max = max - 1;
        }

        var allLetter = letterSize;
        // 分成四组-第一组
        min = 1;
        max = allLetter *0.4;
        var groupOne = parseInt(Math.random() * (max - min + 1) + min);
        if (groupOne > 8)
        {
            groupOne = 8;
        }
        allLetter = allLetter -groupOne;

        // 第二组
        min = 1;
        max = allLetter *0.4;
        var groupTwo = parseInt(Math.random() * (max - min + 1) + min);
        if (groupTwo > 8)
        {
            groupTwo = 8;
        }
        allLetter = allLetter - groupTwo;

        // 第三组
        min = 1;
        max = allLetter *0.4;
        var groupThree = parseInt(Math.random() * (max - min + 1) + min);
        if (groupThree > 8)
        {
            groupThree = 8;
        }
        allLetter = allLetter - groupThree;

        // 第四组
        var groupFour = 0;
        if (allLetter > 8)
        {
            groupFour = 8;
        }
        else
        {
            groupFour = allLetter;
        }

        //
        var leftCount = allLetter - groupFour;
        for (var index = 0 ; index < leftCount; index ++)
        {
            var radominx = parseInt(Math.random() * (2 - 0 + 1) + 0);
            if (radominx == 0 && groupOne < 8)
            {
                groupOne = groupOne + 1;
            }
            else if(radominx == 1 && groupTwo < 8)
            {
                groupTwo = groupTwo + 1;
            }
            else if(radominx == 2 && groupThree < 8)
            {
                groupThree = groupThree + 1;
            }
            else
            {
                index--;
            }
            continue;
        }
        letterArray = $.setGroupView(letterArray,groupOne,1);
        letterArray = $.setGroupView(letterArray,groupTwo,2);
        letterArray = $.setGroupView(letterArray,groupThree,3);
        letterArray = $.setGroupView(letterArray,groupFour,4);


    },
    setGroupView: function (letters,size,type) {
        var letterSize = letters.length - 1;
        for(var index = 0 ; index < 8; index ++)
        {
            labelId = "#word_" + type + "_" + index;
            if (index >= size)
            {
                $(labelId).hide();
                $(labelId).text("");
                continue;
            }
            var radominx = parseInt(Math.random() * (letterSize - 0 + 1) + 0);
            $(labelId).text(letters[radominx]);
            $(labelId).removeAttr("onclick");
            $(labelId).attr("onclick","$.clickLetter('"+ letters[radominx] + "','" + labelId + "');");
            $(labelId).show();
            // 剔除
            letters.splice(radominx,1);

            letterSize = letterSize - 1;
        }

        return letters;
    },
});