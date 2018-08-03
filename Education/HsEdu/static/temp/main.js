$(function () {
	
	//杩斿洖椤堕儴鎸夐挳
	$(window).scroll(function () {
		if ($(window).scrollTop() > 50) {
			$(".gotoTop").fadeIn(1000);
		} else {
			$(".gotoTop").fadeOut();
		}
	});
	$(".gotoTop").click(function () {
		$('body,html').scrollTop(0);
	});
	
	//缈婚〉灞呬腑
	var pageWid=$('.holder').parent().width();
	var holderWid=$('.holder').outerWidth();
	$('.holder').css({marginLeft:(pageWid-holderWid)/2});
	

	/*var viewport = document.querySelector('meta[name="viewport"]');
	viewport.setAttribute('content', 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0'	    );
*/

	
	
	
});
	
	
	