var newCode = null;
var oldCode = null;
var code = null;
$(document).ready(function(e) {
    oldCode = $.GetQueryString("code");

    if (oldCode == null || oldCode == "null")
    {
        newCode = $.newUUID();
        newCode = newCode.replace(/-/g,"");
        // alert(newCode);
        code = newCode;
    }
    else {
        code = oldCode;
    }

    $.setTestValue();
});
$.extend({

    GetQueryString:function (name)
    {
         var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
         var r = window.location.search.substr(1).match(reg);
         if(r!=null)return  unescape(r[2]); return null;
    },
    newUUID: function () {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
            var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    },
    setTestValue:function () {
        $("#resname").val("测试资源");
        $("#resgrade").val(5);
        $("#resclass").val(3);
        $("#resprice").val(103);
        $("#respeople").val("曹先生");
        $("#resviewcount").val(22);
        $("#resdownloadurl").val("www.nak-soft.com");
        $("#respassword").val("123456");
        $("#respreviewurl").val("www.h-sen.com");
        $("#resorgname").val("XXX教育咨询")
        $("#resinfo").val("这是一个好资源");
        $("#orginfo").val("这是一个好单位");
    },
    getInputData:function () {
      var inputDatas = new Array();
      inputDatas[0] =  "resname="  + $("#resname").val();
      inputDatas[1] = "resgrade="  + $("#resgrade").val();
      inputDatas[2] = "resclass="  + $("#resclass").val();
      inputDatas[3] = "resprice="  + $("#resprice").val();
      inputDatas[4] = "respeople="  + $("#respeople").val();
      inputDatas[5] = "resviewcount="  + $("#resviewcount").val();
      inputDatas[6] = "resdownloadurl="  + $("#resdownloadurl").val();
      inputDatas[7] = "respassword="  + $("#respassword").val();
      inputDatas[8] = "respreviewurl="  + $("#respreviewurl").val();
      inputDatas[9] = "resorgname="  + $("#resorgname").val();
      inputDatas[10] = "resinfo="  + $("#resinfo").val();
      inputDatas[11] = "orginfo="  + $("#orginfo").val();

      return inputDatas;
    },
    checkValid:function () {
      var inputDatas = new Array();
      var valData = $("#resname").val();

      if (valData == null || valData=="")
      {
          alert("请输入资源名");
          return false;
      }

      valData = $("#resgrade").val();
      if (valData == null || valData=="")
      {
          alert("这是几年级的资源？请选择");
          return false;
      }

      valData = $("#resclass").val();
      if (valData == null || valData=="")
      {
          alert("这是什么科目的资源？请选择");
          return false;
      }

      valData = $("#resprice").val();
      if (valData == null || valData=="")
      {
          alert("未给资源定价");
          return false;
      }

      valData = $("#respeople").val();
      if (valData == null || valData=="")
      {
          alert("未设置资源提供者");
          return false;
      }

      valData = $("#resviewcount").val();
      if (valData == null || valData=="")
      {
          alert("请给资源设置被查看次数");
          return;
      }

      valData = $("#resdownloadurl").val();
      if (valData == null || valData=="")
      {
          alert("未给定资源下载URL");
          return false;
      }

      valData = $("#respassword").val();
      if (valData == null || valData=="")
      {
          alert("未设置资源下载密码");
          return false;
      }

      valData = $("#respreviewurl").val();
      if (valData == null || valData=="")
      {
          alert("未设置资源试看链接");
          return false;
      }

      valData = $("#resinfo").val();
      if (valData == null || valData=="")
      {
          alert("未设置资描述");
          return false;
      }


      valData = $("#resorgname").val();
      if (valData == null || valData=="")
      {
          alert("未设置单位名称");
          return false;
      }
      valData = $("#orginfo").val();
      if (valData == null || valData=="")
      {
          alert("未设置单位描述");
          return false;
      }
      return true;
    },
    saveInfo: function ()
    {

        if (!$.checkValid())
        {
            return;
        }

        var listParams = new Array();

        listParams[0] = "command=ADD_RESOURCE";

        if (oldCode != null && oldCode != "null")
        {
            listParams[1] = "code=" + oldCode;
        }
        else if (newCode != null && newCode != "null")
        {
            listParams[1] = "code=" + newCode;
        }

        var urlCmd = $.buildGetParam("/api/resource/?" ,listParams);

        var postParam = $.getInputData();
        var params = null;
        params = $.buildPostParam(postParam);

        $.post(urlCmd, params,
            function (data) {

                var ErrorId = data.ErrorId;
                var Result = data.Result;

                if (ErrorId == 200) {
                    alert("操作成功!");
                    var index = parent.layer.getFrameIndex(window.name);
                    parent.layer.close(index);
                    parent.location.reload();
                }
                else {
                    alert(data.ErrorInfo);
                }

            },
            "json");
    },
    openLink:function ()
    {
        var cfgUrl = $("#respreviewurl").val();
        if (cfgUrl.search("http://") != -1)
        {
        }
        else
        {
            cfgUrl = "http://" + cfgUrl;
        }
        window.open(cfgUrl);
    },

    openDownLink:function () {
        var cfgUrl = $("#resdownloadurl").val();
        if (cfgUrl.search("http://") != -1)
        {
        }
        else
        {
            cfgUrl = "http://" + cfgUrl;
        }
        window.open(cfgUrl);
    },

    loadResource:function (datas) {
        oldCode = datas.code;
        $("#resname").val(datas.resname);
        $("#resgrade").val(datas.resgrade);
        $("#resclass").val(datas.resclass);
        $("#resprice").val(datas.resprice);
        $("#respeople").val(datas.respeople);
        $("#resviewcount").val(datas.resviewcount);
        $("#resdownloadurl").val(datas.resdownloadurlabsolute);
        $("#respassword").val(datas.respassword);
        $("#respreviewurl").val(datas.previewurlabsolute);
        $("#resorgname").val(datas.resorgname);
        $("#resinfo").val(datas.resinfo);
        $("#orginfo").val(datas.orginfo);
    },
});