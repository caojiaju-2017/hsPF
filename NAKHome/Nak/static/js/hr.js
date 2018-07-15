$(function(){
	//人力资源
	$('.hrMenu li').click(function(){
		$('.hrMenu li').removeClass('select');
		$(this).addClass('select');
		var index = $(".hrMenu li").index(this);
		TabExchange(index);

	});
	
	
	function TabExchange(num){
	$(".tabMain").hide();
	$(".tabMain").eq(num).fadeIn();
	}
	
	/*$('.jobList h1,.jobList button').click(function(){
		window.open('jobDetail.html');
	});*/
	
	
	$('.jobFunction li').click(function(){
		$('.jobFunction li').removeClass('select');
		$(this).addClass('select');
		var index = $(".jobFunction li").index(this);
		$('body,html').scrollTop(0);
		TabSecond(index);
	});
	
	function TabSecond(num){
	$(".tabSecond").hide();
	$(".tabSecond").eq(num).fadeIn();
	}
	
	$(window).scroll(function () {
		if ($(window).scrollTop() >10) {
			$('.jobfunDiv').css({top:0});
		} else {
			$('.jobfunDiv').css({top:150});
		}
	});
});