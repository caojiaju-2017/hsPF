$.extend({
    changeState: function (data)
    {
        var listParams = new Array();
        listParams[0] = "command=RESOURCE_CHANGE_STATE";
        listParams[1] = "code=" + data.code;

        var urlCmd = $.buildGetParam("/api/resource/?" ,listParams);

        var params = {};

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

    checkValid:function () {
      var inputDatas = new Array();
      var valData = $("#itemindex").val();

      if (valData == null || valData=="")
      {
          alert("未输入章节索引");
          return false;
      }

      valData = $("#itemtitle").val();
      if (valData == null || valData=="")
      {
          alert("未输入章节标题");
          return false;
      }

      valData = $("#iteminfo").val();
      if (valData == null || valData=="")
      {
          alert("未输入章节详情");
          return false;
      }

      return true;
    },

    addItems:function () {
        if (!$.checkValid())
        {
            return;
        }


        var listParams = new Array();
        listParams[0] = "command=RESOURCE_ADD_ITEM";
        listParams[1] = "code=" + code;

        var urlCmd = $.buildGetParam("/api/resource/?" ,listParams);

        var params = {};
        var postParams = new Array();
        postParams[0] = "itemindex=" + $("#itemindex").val();
        postParams[1] = "itemtitle=" + $("#itemtitle").val();
        postParams[2] = "iteminfo=" + $("#iteminfo").val();
        postParams[3] = "itemcode=" + itemcode;

        params = $.buildPostParam(postParams);

        $.post(urlCmd, params,
            function (data) {

                var ErrorId = data.ErrorId;
                var Result = data.Result;

                if (ErrorId == 200) {
                    itemcode = null;
                    alert("操作成功!");
                    location.reload();
                }
                else {
                    alert(data.ErrorInfo);
                }

            },
            "json");
    },

    deleItem:function (datas) {
        var listParams = new Array();
        listParams[0] = "command=RESOURCE_DELE_ITEM";
        listParams[1] = "code=" + datas.code;

        var urlCmd = $.buildGetParam("/api/resource/?" ,listParams);

        var params = {};

        $.post(urlCmd, params,
            function (data) {

                var ErrorId = data.ErrorId;
                var Result = data.Result;

                if (ErrorId == 200) {
                    alert("操作成功!");
                }
                else {
                    alert(data.ErrorInfo);
                }

            },
            "json");
    },

    eidtResourceItem:function (datas) {
        itemcode = datas.code;
        $("#itemindex").val(datas.index);
        $("#itemtitle").val(datas.title);
        $("#iteminfo").val(datas.introduce);
    },
});