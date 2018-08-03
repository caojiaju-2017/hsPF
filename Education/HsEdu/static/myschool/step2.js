var Hsusername;
var Hsphone;
var Hsemail;
var Hsprovince;
var Hscity;
var Hszone;

window.onload=function()
{

};

$(document).ready(function()
{
    var docHeight = $(document).height();
    var docWidth = $(document).width();

    $("#step2_body").height(docHeight - 430);

    $('#commit_res').css('marginTop',50);
    $('#commit_res').css('marginLeft',(docWidth - 260)/2);
});

$.extend({
    example:function () {

        },

    initPostInfo:function (username, phone,email,province,city,zone) {
        Hsusername = username;
        Hsphone = phone;
        Hsemail = email;
        Hsprovince = province;
        Hscity = city;
        Hszone = zone;
    },
    commitData:function () {
        var openid = $.cookie('WX_OpenId_HS');
        var name = $.cookie('WX_Name_HS');
        var imagepath = $.cookie('WX_Image_HS');

        var school = $("#schoolname").val();
        // alert("openid="  +openid);
        // alert("name="  +name);
        // alert("imagepath="  +imagepath);
        // alert("username="  +Hsusername);
        // alert("phone="  +Hsphone);
        // alert("email="  +Hsemail);
        // alert("province="  +Hsprovince);
        // alert("city="  +Hscity);
        // alert("zone="  +Hszone);
        // alert("school="  +school);

            //post
        var rtnCmd = "/api/school/?Command=Register_User";
        $.post(rtnCmd, {openid:openid,wxname:name,imgurl:imagepath,username: Hsusername, phone: Hsphone, email: Hsemail, province: Hsprovince, city: Hscity, zone: Hszone,school:school},
            function (data)
            {

                var  ErrorId = data.ErrorId;
                var  Result = data.Result;

                if (ErrorId == 200)
                {
                    location.href = "reg_direct_myschool.html";
                }
                else
                {
                    alert(data.ErrorInfo);
                }

            },
            "json");//这里返回的类型有：json,html,xml,text


        },
});