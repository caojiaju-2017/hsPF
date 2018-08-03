window.onload=function()
{
    var docHeight = $(document).height();

    $("#left_menu").height(docHeight - 20);
    $("#right_context").height(docHeight - 20);
    $("#test").height(docHeight - 30);
};

$.extend({
    test: function (codeName) {
        alert("s");
    },

});