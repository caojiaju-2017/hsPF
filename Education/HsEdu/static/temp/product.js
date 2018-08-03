$(function(){
	TabExchange(0);
	TabSecond1(0);
	TabSecond2(0);
	procontentWidth();
	
	
	$('.productMenu li').click(function(){
		$('.productMenu li').removeClass('select');
		$(this).addClass('select');
		var index = $(".productMenu li").index(this);
		TabExchange(index);
		procontentWidth();
		
	});
	
	
	$('.xw_jobFunction1 li').click(function(){
		$('.xw_jobFunction1 li').removeClass('select');
		$(this).addClass('select');
		var index = $(".xw_jobFunction1 li").index(this);
		$('body,html').scrollTop(0);
		TabSecond1(index);
		procontentWidth();
	});
	
	$('.xw_jobFunction2 li').click(function(){
		$('.xw_jobFunction2 li').removeClass('select');
		$(this).addClass('select');
		var index = $(".xw_jobFunction2 li").index(this);
		$('body,html').scrollTop(0);
		TabSecond2(index);
		procontentWidth();
	});
	
//显示隐藏左菜单
	$('.proArrowLeft').click(function(){
		$('.productMenu').animate({left:-200});
		$(this).hide();
		$('.proArrowRight').show();
	});	
	$('.proArrowRight').click(function(){
		$('.productMenu').animate({left:20});
		$(this).hide();
		$('.proArrowLeft').show();
	});		
	
	
});


function procontentWidth(){
	if(screen.width<=1024){
		$('.productRight').css({marginLeft:200});
	}else{
		if(screen.width<=1280){
			$('.productRight').css({marginLeft:100});
		}else{
			$('.productRight').css({marginLeft:50});
		}
		
	}
};


//菜单tab切换
function TabExchange(num){
	$(".tabProduct").hide();
	$(".tabProduct").eq(num).fadeIn();
	};
	
	
	
	
function TabSecond1(num){
$(".xw_tabSecond1").hide();
$(".xw_tabSecond1").eq(num).fadeIn();
};


function TabSecond2(num){
$(".xw_tabSecond2").hide();
$(".xw_tabSecond2").eq(num).fadeIn();
};
	
