window.onload=function()
{

};

$(document).ready(function()
{
    var docHeight = $(document).height();
    var docWidth = $(document).width();

    $("#step1_body").height(docHeight - 200);

    $('#next_step').css('marginTop',50);
    $('#next_step').css('marginLeft',(docWidth - 260)/2);

    $('#head_img').css('marginLeft',(docWidth - 180)/2);

});

$.extend({
    example:function () {

        },
    
    goNext:function () {

        var userName = $("#fullname").val();
        var phoneId = $("#phoneId").val();
        var email = $("#email").val();

        var province = $("#province").val();
        var city = $("#city").val();
        var zone = $("#zone").val();

        location.href = "step2.html?username=" + userName + "&phone=" + phoneId + "&email=" + email + "&province=" + province + "&city=" + city + "&zone=" + zone;
    }
});