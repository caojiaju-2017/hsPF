/**
 * Created by jiaju_cao on 2017/6/7.
 */
window.onload=function()
{
};

$(document).ready(function()
{

});

$(window).resize(function(){
});

// 自定义函数
$.extend({
    commitQuestion:function () {
        var OpenId = "abc" ;
        var title = $("#title").val();
        var customname = $("#customname").val();
        var customphone = $("#customphone").val();
        var infodetail = $("#infodetail").val();

        if ($.isEmptyObject(title))
        {
            alert("亲~，你还没输入标题！");
            return;
        }
        if ($.isEmptyObject(customname))
        {
            alert("亲~，你还没输入联系信息！");
            return;
        }

        if ($.isEmptyObject(customphone))
        {
            alert("亲~，你还没输入联系信息！");
            return;
        }

        if ($.isEmptyObject(infodetail))
        {
            alert("亲~，你还没输入详细建议描述！");
            return;
        }
        var rtnCmd = "/api/ctm/?Command=Release_Suggest";

        $.post(rtnCmd, {ucode: OpenId, title: title, customname: customname, customphone: customphone, detail: infodetail},
            function (data)
            {

                var  ErrorId = data.ErrorId;
                var  Result = data.Result;

                if (ErrorId == 200)
                {
                    alert("感谢您的宝贵意见！");
                //    返回上一页
                //     window.location.href=document.referrer;
                    history.back() ;
                }
                else
                {
                    alert(data.ErrorInfo);
                }

            },
            "json");//这里返回的类型有：json,html,xml,text
    },
});