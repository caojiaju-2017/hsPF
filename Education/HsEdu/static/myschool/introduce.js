window.onload=function()
{

};

$(document).ready(function()
{
    var docHeight = $(document).height();
    var docWidth = $(document).width();

    $("#introduct_body").height(docHeight - 200);

    $('#enter_button').css('marginTop',50);
    $('#enter_button').css('marginLeft',(docWidth - 260)/2);

    $("#introduce_img").height($("#introduct_body").height());
    $('#introduce_img').css('marginLeft',20);
    $("#introduce_img").width($("#introduct_body").width() - 40);

});

$.extend({
    example:function () {

        },

    writeCookie:function(openid,name,imagepath)
    {
        $.cookie('WX_OpenId_HS', openid);
        $.cookie('WX_Name_HS', name);
        $.cookie('WX_Image_HS',imagepath);
    }
});