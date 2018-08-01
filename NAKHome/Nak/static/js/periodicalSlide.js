$(document).ready(function(){
	apepndListUser(listjsonUser);
});	

var listjsonUser = [
    {pdfUrl:"",src:"images/periodical/201401.jpg",text:"《NAK科技》2014年01期"},
	{pdfUrl:"",src:"images/periodical/201402.jpg",text:"《NAK科技》2014年02期"},
	{pdfUrl:"",src:"images/periodical/201403.jpg",text:"《NAK科技》2014年03期"},
	{pdfUrl:"",src:"images/periodical/201301.jpg",text:"《NAK乐园》2013年01期"},
	{pdfUrl:"",src:"images/periodical/201302.jpg",text:"《NAK乐园》2013年02期"},
	{pdfUrl:"",src:"images/periodical/201303.jpg",text:"《NAK乐园》2013年03期"},
	{pdfUrl:"",src:"images/periodical/201304.jpg",text:"《NAK乐园》2013年04期"},
	{pdfUrl:"",src:"images/periodical/201305.jpg",text:"《NAK乐园》2013年05期"},
	{pdfUrl:"",src:"images/periodical/201306.jpg",text:"《NAK乐园》2013年06期"},
	{pdfUrl:"",src:"images/periodical/201307.jpg",text:"《NAK乐园》2013年07期"},
	{pdfUrl:"",src:"images/periodical/201308.jpg",text:"《NAK乐园》2013年08期"},
	{pdfUrl:"",src:"images/periodical/201309.jpg",text:"《NAK乐园》2013年09期"},
	{pdfUrl:"",src:"images/periodical/201310.jpg",text:"《NAK乐园》2013年10期"},
	{pdfUrl:"",src:"images/periodical/201311.jpg",text:"《NAK乐园》2013年11期"},
	{pdfUrl:"",src:"images/periodical/201312.jpg",text:"《NAK乐园》2013年12期"},
	{pdfUrl:"",src:"images/periodical/201313.jpg",text:"《NAK乐园》2013年13期"}
]



var panel = null;
function apepndListUser(ListtjsonUs) {
	var itemContent = [];

	for (var i = 0; i < ListtjsonUs.length; i++) {
		
		itemContent.push(
				'<li pdf="'+listjsonUser[i].pdfUrl+'"><img src="'+ listjsonUser[i].src+'"><h1>'+listjsonUser[i].text+'</h1></li>'
		);
		
		
		
	}
	

	
	//初始化面板对象
	panel = new BasePanel('.periodical', {
		/**面板可视范围内显示的元素个数，如果展开后，
		 * 则是disItem = disItem * expanRow*/
		//disItem:6,
		/**显示面板宽度*/
		//width:970,
		itemWidth:160,
		/**面板里需要承载的html内容*/
		contentHtml: itemContent,
		/**是否显示展开按钮*/
		isExpan: false,
		/**是否自动展开*/
		isAutoExpan: true,
		/**展开后显示的行数*/
		expanRows:2,
		/**箭头位置：top：顶部；middle：中间*/
		arrowAlign: 'none',
		/**面板移动完成后事件*/
		onmoveend: function (pageNo) {

		},
		
		
		//面板上的点击事件
       /*itemClick:function(idx,item){		   
			var pdfv = item.parent().attr('pdf');
			window.open(pdfv);
			
        }*/
	});
	
	
	
	$(".pageArrow").remove();
	
	
	/*如果只有一页隐藏圆点*/
	var yuanTotal=$(".periodical .pageNo").find("span").length;
	if(yuanTotal==1){
		$(".periodical .pageNo").hide();
		}else{
			$(".periodical .pageNo").show();
			};
	


}
