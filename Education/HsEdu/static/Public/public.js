$.extend({
    getUrlData: function (url,params) {

    },

    postCommand: function (url,params) {

    },
    showMsg:function (layer,msg) {
        layer.open({
            type: 1
            , id: 'layerMsg' //防止重复弹出
            , content: '<div style="padding: 20px 100px;">' + msg + '</div>'
            , btn: '关闭全部'
            , btnAlign: 'c' //按钮居中
            , shade: 0 //不显示遮罩
            , yes: function () {
                layer.closeAll();
            }
        });
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
    signString:function(params){
        var signString = "";
        for (var index = 0 ; index< params.length; index++ )
        {
            signString = signString + params[index];
        }

        signString = signString + $.getSecretKey();

        console.log(signString);
        return $.md5(signString);
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
        // alert("fdsaf");
        history.go(-1);
    },
    getSecretKey:function () {
      //  真实情况需要 动态生成
      return "g^4)=h@ir_n!azd^wh8*+p6*y1#uvsjd%d4lzyv_egwyj^$hi_";
    },
    buildGetParam :function (preUrl,params) {
        var rtnUrl = preUrl;
        for (var index = 0 ; index < params.length ; index++)
        {

            if (index != 0)
            {
                rtnUrl = rtnUrl + "&" + params[index];
            }
            else {
                rtnUrl = rtnUrl + params[index];
            }
        }

        return rtnUrl;
    },
    buildPostParam :function (params) {
        var rtnDict = {}
        for (var index = 0 ; index < params.length ; index++)
        {
            var oneParam = params[index];

            var paramInfos = oneParam.split("=");
            if (paramInfos.length == 2)
            {
                rtnDict[paramInfos[0]] = paramInfos[1];
            }
            else
            {
                rtnDict[paramInfos[0]] = "";
            }

        }

        return rtnDict;
    },
    checkDuplate:function (datas,starttime,stoptime,keyValue) {
        for (var index = 0 ; index < datas.length ; index ++)
        {
            var oneCfg = datas[index];
            if (oneCfg.length <= 0)
            {
                continue;
            }
            var cfgStartTime = oneCfg.starttime;
            var cfgStopTime = oneCfg.stoptime;

            if (keyValue == oneCfg.valuekey) {


                if ((starttime >= cfgStartTime && starttime <= cfgStopTime) || (stoptime >= cfgStartTime && stoptime <= cfgStopTime)) {
                    return true;
                }
            }
        }

        return false;
    },
    getWeekName :function (index) {
        if (index == 0)
        {
            return "星期日";
        }
        else if (index == 1)
        {
            return "星期一"
        }
        else if (index == 2)
        {
            return "星期二"
        }
        else if (index == 3)
        {
            return "星期三"
        }
        else if (index == 4)
        {
            return "星期四"
        }
        else if (index == 5)
        {
            return "星期五"
        }
        else if (index == 6)
        {
            return "星期六"
        }
    },

    checkNumber: function (theObj) {
        var reg = /^[0-9]+.?[0-9]*$/;
        if (reg.test(theObj)) {
            return true;
        }
        return false;
    },
    alginString:function (len, pre,srcValue) {
        srcValue = "" + srcValue;

        while (srcValue.length < len)
        {
            srcValue = pre + srcValue
        }
        return srcValue;
    },
    showElement: function (privs) {
        // 判断是否为特殊权限组
        var specialKeys = privs["00000"];

        $("#menu_11000").hide();
        $("#menu_11001").hide();
        $("#menu_11002").hide();
        $("#menu_11003").hide();
        $("#menu_11004").hide();
        $("#menu_11005").hide();
        $("#menu_11006").hide();

        if (specialKeys == "0")
        {
            return;
        }
        else if (specialKeys == "1"){
                $("#menu_11000").show();
                $("#menu_11001").show();
                $("#menu_11002").show();
                $("#menu_11003").show();
                $("#menu_11004").show();
                $("#menu_11005").show();
                $("#menu_11006").show();

                return;
        }

        for(var key in privs)
        {
            var keyName = "#menu_" + key;
            var keyValue = privs[key];

            if ($.hasAnyPriv(keyValue))
            {
                $(keyName).show();
            }
            else
            {
                $(keyName).hide();
            }

        }
    },

    hasAnyPriv : function (privFlag) {
        var privValue = privFlag.substring(0,6);

        var intPrivValue = parseInt(privValue);

        if (intPrivValue > 0)
        {
            return true
        }

        return false;
    },
    
    listToString :function (params, sep) {
        var rtnString = null;
        for (var index = 0 ; index < params.length; index ++)
        {
            if (rtnString == null)
            {
                rtnString  = params[index];
            }
            else {
                rtnString  =  rtnString + sep + params[index];
            }
        }

        if (rtnString == null)
        {
            return "";
        }

        return rtnString;
    }
});
