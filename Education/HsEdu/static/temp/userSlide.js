$(document).ready(function(){
	apepndListUser(listjsonUser);
});	

var listjsonUser = [
    {className:"telecomLogo"},
	{className:"mobileLogo"},
	{className:"unicomLogo"},
	{className:"powerLogo"},
	{className:"waterLogo"},
	{className:"sinopecLogo"},
	{className:"dianwangLogo"},
	{className:"toyotaLogo"},
	{className:"nanfangLogo"},
	{className:"tanglaiLogo"},
	{className:"sarftLogo"},
	{className:"mangoLogo"},
	{className:"huawei"},
	{className:"langchao"},
	{className:"citrix"},
	{className:"h3c"},
	{className:"ibm"},
	{className:"sap"},
	{className:"dell"},
	{className:"oracle"},
	{className:"dynatrace"},
	{className:"nsfocus"},
	{className:"suse"},
	{className:"symantec"},
	{className:"arcgis"},
	{className:"compuware"},
	{className:"wuzhou"}
]



var panel = null;
function apepndListUser(ListtjsonUs) {
	var itemContent = [];

	for (var i = 0; i < ListtjsonUs.length; i++) {
		
		itemContent.push(
				'<li class='+listjsonUser[i].className+'></li>'
		);
		
	}
	
	//初始化面板对象
	panel = new BasePanel('.successIndex ul', {
		/**面板可视范围内显示的元素个数，如果展开后，
		 * 则是disItem = disItem * expanRow*/
		//disItem:6,
		/**显示面板宽度*/
		//width:970,
		itemWidth:150,
		/**面板里需要承载的html内容*/
		contentHtml: itemContent,
		/**是否显示展开按钮*/
		isExpan: false,
		/**是否自动展开*/
		isAutoExpan: true,
		/**展开后显示的行数*/
		expanRows:3,
		/**箭头位置：top：顶部；middle：中间*/
		arrowAlign: 'none',
		/**面板移动完成后事件*/
		onmoveend: function (pageNo) {

		},
		
		//面板上的点击事件
       itemClick:function(){		   
			window.open('product.html');
			
        }
		
	});
	
	$(".pageArrow").remove();
	
	/*如果只有一页隐藏圆点*/
	var yuanTotal=$(".successIndex .pageNo").find("span").length;
	if(yuanTotal==1){
		$(".successIndex .pageNo").hide();
		}else{
			$(".successIndex .pageNo").show();
			};
	


}
