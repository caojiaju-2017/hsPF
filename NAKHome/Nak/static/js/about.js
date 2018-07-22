$(function(){
	
//员工风采
	memberWidth();
	
//关于NAK菜单滑动
	var menuTop = 200;
	var itemTop = {};
	var itemArr = ['a', 'd', 'e', 'f', 'g'];

	itemTopInit(itemArr);
	
	
	$(".aboutMenu li").click(function() {
		$(".aboutMenu li").removeClass('select');
		$(this).addClass('select');
		var objId = $(this).attr('the-id');
		var topNum = $('#'+objId).offset().top;
		console.log(objId);
		$("html,body").stop().animate({
			scrollTop: topNum
		});

	});

//返回顶部按钮

        $(window).scroll(function() {
		var windowScrollTop = $(window).scrollTop();
		if (windowScrollTop > 50) {
			$(".gotoTop").fadeIn(1000);
		} else {
			$(".gotoTop").fadeOut();
		}
			//触发菜单选择
		menuSelect(windowScrollTop);
	});
	$(".gotoTop").click(function() {
		$('body,html').scrollTop(0);
	});
   
	
	
function itemTopInit(itemArr) {
		for (var i in itemArr) {
			itemTop[itemArr[i]] = $('#'+itemArr[i]).offset().top - menuTop;
		}
	}

	function menuSelect(windowScrollTop) {
		var scrollTop = Math.max(windowScrollTop, 10);
		for (var i = 1; i <= itemArr.length; i++) {
			var min = itemTop[itemArr[i - 1]];
			var max = itemTop[itemArr[i]] || 1000*1000;
			var theSelect = itemArr[i - 1];
			if (scrollTop >= min-5 && scrollTop < max-5) {//IE下增加偏移量 不然会出现bug
				$theSelect = $('[the-id='+theSelect+']');
				if (!$theSelect.hasClass('select')) {
					$(".aboutMenu li").removeClass('select');
					$theSelect.addClass('select');
				}
				break;
			}
		}
	}

});

//员工风采不同分辨率下的宽度
function memberWidth(){
	var winWid=$(window).width();
	
		if(screen.width<=1024){
			$('.styleMember li').css({width:(winWid-10-40)/4});
		}else{
			if(screen.width<=1280){
				$('.styleMember li').css({width:(winWid-10-50)/5});
			}else{
				if(screen.width<=1366){
				$('.styleMember li').css({width:(winWid-10-60)/6});
				}else{
					$('.styleMember li').css({width:(winWid-10-80)/8});
				}
		    }
		
	    }
	
};


/*function memberWidth(){
	if(screen.width<=1000){
		$('.styleMember li').css({width:235});
	}else{
		if(screen.width<=1024){
			$('.styleMember li').css({width:240});
		}else{
			if(screen.width<=1280){
				$('.styleMember li').css({width:241});
			}else{
				if(screen.width<=1366){
				$('.styleMember li').css({width:213});
				}else{
					$('.styleMember li').css({width:227});
				}
		    }
		
	    }
	}
};*/


