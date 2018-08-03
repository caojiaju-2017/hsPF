var currentType = 10;
window.onload=function()
{

};

$(document).ready(function()
{
    var docHeight = $(document).height();
    var docWidth = $(document).width();

    $(".body_frame1").height(docHeight - 41);

    $(".body_frame2").height(docHeight - 41);
    // $(".body_frame2").css("src","mb_home.html");

    $(".body_frame3").height(docHeight - 41);

    $.showResource(10);
});

$.extend({
    example:function () {

        },
    setUserInfo: function (openid, username, headimg) {
            $.cookie("OpenId", openid);
            $.cookie("WxName", username);
            $.cookie("HeadImg", headimg);
        },


showResource: function (index) {
        currentType = index;
        $.cookie("BrowserIndex", currentType);
        // 设置背景色
        $("#abc_" + 2).css("color","#4C555A");
        $("#abc_" + 4).css("color","#4C555A");
        $("#abc_" + 10).css("color","#4C555A");

        $("#abc_" + 2).css("background-color","#FFFFFF");
        $("#abc_" + 4).css("background-color","#FFFFFF");
        $("#abc_" + 10).css("background-color","#FFFFFF");

        $("#abc_" + currentType).css("color","#FFFFFF");
        $("#abc_" + currentType).css("background-color","#06BBD0");

        if (currentType == 10)
        {
            $("#body_frame1").prop("hidden",true);
            $("#body_frame2").prop("hidden",false);
            $("#body_frame3").prop("hidden",true);

            $("#abc_10_img").attr("src","/static/myschool/Images/home_focus.png")
        }
        else if(currentType == 2)
        {
            $("#body_frame1").prop("hidden",false);
            $("#body_frame2").prop("hidden",true);
            $("#body_frame3").prop("hidden",true);

            $("#abc_10_img").attr("src","/static/myschool/Images/home_nofocus.png")
        }
        else if(currentType == 4)
        {
            $("#body_frame1").prop("hidden",true);
            $("#body_frame2").prop("hidden",true);
            $("#body_frame3").prop("hidden",false);
            $("#abc_10_img").attr("src","/static/myschool/Images/home_nofocus.png")
        }

    },
});