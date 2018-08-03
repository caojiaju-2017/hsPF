var oneArticleTemp = "<div style=\"margin-top:10px;clear:both;height: 60px;width: 90%;\">\n" +
+
    "    <div style=\"width: 100%;height: 60px;margin-left: 5%;color: #8c8a90\">\n" +
    "\n" +
    "        <div style=\"margin-top:10px;border-radius: 20px; float:left;width: 40px;height: 40px;background-size: cover;\n" +
    "        background-image: url('{headimage}')\"></div>\n" +
    "\n" +
    "\n" +
    "        <div style=\"float: left;text-align: left\">\n" +
    "\n" +
    "            <div style=\"width: 100%;height: 20px;line-height: 20px;margin-left: 20px;margin-top: 10px\">{title}</div>\n" +
    "\n" +
    "\n" +
    "            <div style=\"width: 100%;height: 20px;line-height: 20px;margin-left: 20px;margin-top: 10px\">{time}  来自 {school}</div>\n" +
    "        </div>\n" +
    "\n" +
    "\n" +
    "\n" +
    "    </div>\n" +
    "\n" +
    "\n" +
    "    <div style=\"width: 100%;margin-left: 5%;margin-top:10px;margin-right: 5%;max-height: 180px;color: black\">{simplecontent}</div>\n" +
    "\n" +
    "\n" +
    "    <div style=\"width: 100%;height: 180px;margin-top:20px;margin-left:5%;border-radius:10px;background-size: cover;background-image: url('{articleimage}')\">\n" +
    "\n" +
    "    </div>\n" +
    "\n" +
    "\n" +
    "    <div style=\"width: 90%;height: 60px;margin-left: 5%\">\n" +
    "\n" +
    "        <div style=\"float: left;text-align: center;width: 100px\">\n" +
    "            <img src=\"/static/Images/2.png\" style=\"width: 20px;height: 20px;background-size: cover;margin-top: 10px\">\n" +
    "            <div style=\"height: 20px;line-height: 20px;text-align: center;font-size: 10px;\">{readcount}</div>\n" +
    "        </div>\n" +
    "\n" +
    "\n" +
    "        <div style=\"float: right;text-align: center;width: 100px;\">\n" +
    "            <img src=\"/static/Images/2.png\" style=\"width: 20px;height: 20px;background-size: cover;margin-top: 10px\">\n" +
    "            <div style=\"height: 20px;line-height: 20px;text-align: center;font-size: 10px;\">{favcount}</div>\n" +
    "        </div>\n" +
    "    </div>\n" +
    "\n" +
    "\n" +
    "</div>\n" +
    "<div style=\"clear:both;width: 90%;height: 5px;background-color: #92B8B1;margin-left: 5%\"></div>";


var isResLoadFinishLoad = false;
var currentResLoadPageIndex = 0;
var currentResLoadPageSize = 10;
var queryResLoadLock = false;
window.onload=function()
{

};

$(document).ready(function()
{
    $.initLoading();
    $(window).scroll(function () {
        var srollPos = $(window).scrollTop();
        var documentHd = $(document).height();
        var winHd = $(window).height();


        totalheight = parseFloat($(window).height()) + parseFloat(srollPos);

        // if (srollPos + winHd > documentHd * 0.9) {
        //     if (!isResLoadFinishLoad && !queryResLoadLock) {
        //             queryResLoadLock = true;
        //             // 加载数据
        //             currentResLoadPageIndex = currentResLoadPageIndex + 1;
        //             $.searchArticle();
        //         }
        // }
    });

    $.searchArticle();
    //
    alert("search123");
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

    beginSearch: function () {
        isResLoadFinishLoad = false;
        currentResLoadPageIndex = 0;
        currentResLoadPageSize = 10;
        queryResLoadLock = false;
        $(".body").html("");
        $.searchArticle();

    },
    get_resquery_cmd: function (filter) {

        var rtnCmd = "/api/school/?Command=List_Article&pageindex={0}&pagesize={1}&filter={2}";
        rtnCmd = $.StringFormat(rtnCmd, currentResLoadPageIndex, currentResLoadPageSize, filter);
        currentResLoadPageIndex = currentResLoadPageIndex + 1;
        return rtnCmd;
    },
    searchArticle: function () {

        //var fliter = $("#fliter_input").val();
        var fliter = "";
        // 准备发送查询指令
        var cmdString = $.get_resquery_cmd(fliter);
        // 提取用户名
        //$("#loading").modal("show");
        $.get(cmdString,
            function (data) {
                // 检查查询状态
                var ErrorId = data.ErrorId;
                var Result = data.Result;
                var Datas = Result;
                //$("#loading").modal("hide");
                if (ErrorId == 200) {
                    if (Datas.length <= 0 || Datas.length < currentResLoadPageSize) {
                        isResLoadFinishLoad = true;
                    }
                    for (i = 0; i < Datas.length; i++) {
                        var oneCode1 = Datas[i];

                        var abcTemp = {};
                        abcTemp["headimage"] = oneCode1.headimage;
                        abcTemp["title"] = oneCode1.title;
                        abcTemp["time"] = oneCode1.time;
                        abcTemp["school"] = oneCode1.school;
                        abcTemp["favvalue"] = oneCode1.favvalue;
                        abcTemp["favimage"] = oneCode1.favimage;
                        abcTemp["simplecontent"] = oneCode1.simplecontent;
                        abcTemp["articleimage"] = oneCode1.articleimage;
                        abcTemp["readcount"] = oneCode1.readcount;
                        abcTemp["favcount"] = oneCode1.favcount;
                        var oneT = $("body").html();

                        var newOne = $.format(oneArticleTemp, abcTemp);
;

                        $("body").html(oneT + newOne);
                    }
                    queryResLoadLock = false;
                }

            },
            "json");//这里返回的类型有：json,html,xml,text
    },
    example:function () {

        },

});