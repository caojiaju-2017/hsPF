var openid ;

$(document).ready(function(e) {
    openid = $.cookie('WX_OpenId');
    // $('body').on('touchmove',function(event){event.preventDefault();});
    // $('#word_table_div').addEventListener('touchmove', function(e) {e.stopPropagation();}, false);

    var docHeight = $(document).height();
    $("#word_table_div").height(docHeight - 700);

    // = $.cookie('WX_OpenId')

    $.initLoading();
});

$.extend({
    openGameSetting: function () {
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


    goBackPage: function () {
        location.href = "game_home.html";
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
    loadData:function (unitcode) {
        $("#loading").modal("show");

        var cmdString = "/api/game/?Command=Get_Result&unitcode={0}&openid={1}";
        var rtnCmd = $.StringFormat(cmdString, unitcode,openid);
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
                    right = Datas.right;
                    noanswers = Datas.noanswer;
                    errors = Datas.error;

                    $.fillData(right,noanswers,errors);
                    }
            },
            "json");//这里返回的类型有：json,html,xml,text
    },
    fillData:function (rights,noanswers,errors) {
        // alert(rights);
        var indexGlobal = 1;
        var existValue = $("#content_table").html();
        for (var index = 0 ; index < rights.length; index++)
        {
            var oneResult = rights[index];
            existValue = existValue + "<tr>";
            existValue = existValue + "<td>" + indexGlobal +"</td>";
            existValue = existValue + "<td>" + oneResult.word +"</td>";
            existValue = existValue + "<td>" + oneResult.mykey +"</td>";
            existValue = existValue + "</tr>";

            indexGlobal = indexGlobal + 1;
        }

        for (var index = 0 ; index < noanswers.length; index++)
        {
            var oneResult = noanswers[index];
            existValue = existValue + "<tr style='background-color: orangered;color: red'>";
            existValue = existValue + "<td style='background-color: orangered;color: white'>" + indexGlobal +"</td>";
            existValue = existValue + "<td style='background-color: orangered;color: white'>" + oneResult.word +"</td>";
            existValue = existValue + "<td style='background-color: orangered;color: white'>" + oneResult.mykey +"</td>";
            existValue = existValue + "</tr>";

            indexGlobal = indexGlobal + 1;
        }

        for (var index = 0 ; index < errors.length; index++)
        {
            var oneResult = errors[index];
            existValue = existValue + "<tr style='background-color: #ec971f;color: white'>";
            existValue = existValue + "<td style='background-color: #ec971f;color: white'>" + indexGlobal +"</td>";
            existValue = existValue + "<td style='background-color: #ec971f;color: white'>" + oneResult.word +"</td>";
            existValue = existValue + "<td style='background-color: #ec971f;color: white'>" + oneResult.mykey +"</td>";
            existValue = existValue + "</tr>";

            indexGlobal = indexGlobal + 1;
        }

        $("#content_table").html(existValue);

        // 计算得分
        var countTotal = rights.length + noanswers.length + errors.length;
        var result = (rights.length) / countTotal;
        $("#result_score").text(parseInt(result*100) + "分");

        // 设置简要信息
        $("#result_info").text(countTotal + "个单词，答对" +rights.length+ "个，" + noanswers.length + "个未答，" + errors.length + "个答错");
    },
});