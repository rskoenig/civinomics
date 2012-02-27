$(document).ready(function() {
	
	$('.thumbs').children('a').toggle(function(event) { // change thumb images on click
		var thumb = $(this).parents('div.comment_data');
		thumb.find('.thumbs.up>a').css("background","url('/images/thumb_up_green.gif')");
		thumb.find('.thumbs.down>a').css("background","url('/images/thumb_down_red.gif')");
		event.preventDefault();
	}, function(event) {
		var thumb = $(this).parents('div.comment_data');
		thumb.find('.thumbs.up>a').css("background","url('/images/thumb_up_grey.png')");
		thumb.find('.thumbs.down>a').css("background","url('/images/thumb_down_grey.png')");
	});
	
	$('a.flag').toggle(function(event) { //show and hide the flag content dialog
		$(this).parent().parent().parent().children('.flag.content')
		.css({
			"display":"block"
		})
		.animate({
			height: "60px",
			paddingTop: "10px",
			paddingBottom: "10px",
			paddingLeft: "10px"
		});
		event.preventDefault();
	}, function(event) {
		$(this).parent().parent().parent().children('.flag.content').animate({
			height: "0px",
			paddingTop: "0px",
			paddingBottom: "0px",
			paddingLeft: "0px"
		}, function(){
			$(this).css('display','none');
		});
		event.preventDefault();
	});
	
	$('a.reply').toggle(function(event) { //show and hide the reply content dialog
		$(this).parent().parent().parent().children('.reply.content').css({
			"display":"block"
		})
		.animate({
			height: "40px",
			paddingTop: "10px",
			paddingBottom: "10px",
			paddingLeft: "10px"
		});
		event.preventDefault();
	}, function(event) {
		$(this).parent().parent().parent().children('.reply.content').animate({
			height: "0px",
			paddingTop: "0px",
			paddingBottom: "0px",
			paddingLeft: "0px"
		}, function(){
			$(this).css('display','none');
		});
		event.preventDefault();
	});
	
	$('div.flag>form').submit(function(event) { //show "comment flagged" after submission
		$(this).parent().parent().find('a.flag').first().parent('p').prepend('Comment flagged').children('a.flag').remove();
		$(this).closest('.content').animate({
			height: "0px",
			paddingTop: "0px",
			paddingBottom: "0px",
			paddingLeft: "0px"
		}, function() {
			$(this).css('display','none');
		});
		event.preventDefault();
	});
	
});
