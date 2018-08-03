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
    viewOrgInfo:function (orgcode) {
        alert("viewOrgInfo->" + orgcode);
    },

    exitOrganization:function (orgcode) {
        alert("exitOrganization->" + orgcode);
    },
    scanEWM:function () {
        alert("scanEWM->");
    },
});