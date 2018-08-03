$.extend({

    ReleaseRemark: function (codeName) {
        var openId = $.cookie("OpenId");
        var remark_body = $("#remark_body").val();

        var rtnCmd = "/api/ctm/?Command=Release_Remark";

        $.post(rtnCmd, {openid: openId, body: remark_body,rcode:codeName},
            function (data)
            {

                var  ErrorId = data.ErrorId;
                var  Result = data.Result;

                if (ErrorId == 200)
                {
                    alert("Success!");
                    window.location.reload()
                }
                else
                {
                    alert(data.ErrorInfo);
                }

            },
            "json");//���ﷵ�ص������У�json,html,xml,text
    },
});