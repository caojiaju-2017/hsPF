//获取url get 参数
// function getUrlParam(name) {
//     var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); //构造一个含有目标参数的正则表达式对象
//     var r = window.location.search.substr(1).match(reg);  //匹配目标参数
//     if (r != null) return unescape(r[2]); return null; //返回参数值
// }
//


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

});