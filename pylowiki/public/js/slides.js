$(document).ready(function() {
    
    $('.slideshow_launch').click(function(event){
        $('#pop').css({
            'height':$(document).height(),
            'width':$(document).width()
        });
        $('#slideshow,#pop').css({
			'display':'block'
		});
        $slideshow = $('#slideshow h2>p:nth-child(3)'); //since it's float: right, choose 3rd child, not 1st
		$close = $('#close');
		a = $($slideshow).innerWidth();
		b = $($close).innerWidth();
		c = Math.max(a,b);
		$($slideshow).width(c);
		$($close).width(c);
		$h3 = $('.slidetitle').parent();
		border = $($close).innerWidth()-$($close).width();
		$('.slidetitle').width($($h3).innerWidth()-2*c-3*border); //WHY IS IT 3*BORDER AND NOT 2*BORDER!?!?
		event.preventDefault();
    });
    
    $('.suggestion').click(function(event){
		$('#pop').css({
			'display':'block',
			'height':$(document).height(),
			'width':$(document).width()
		});
		$('#suggestion').css({
			'display':'block',
			'height':'450',
			'width':'680'
		});
		event.preventDefault();
	});
	
	$('button#sign_up_submit').click(function(event){
		$('#pop').css({
			'display':'block',
			'height':$(document).height(),
			'width':$(document).width()
		});
		$('#registered').css({
			'display':'block',
		});
		event.preventDefault();
	});
	
	$('.invite_friends').click(function(event){
		$('#pop').css({
			'display':'block',
			'height':$(document).height(),
			'width':$(document).width()
		});
		$('#invite_pop').css({
			'display':'block'
		});
		event.preventDefault();
	});
	
	$('.compose_message_button').click(function(event){
		$('#pop').css({
			'display':'block',
			'height':$(document).height(),
			'width':$(document).width()
		});
		$('#compose_message_popup').css({
			'display':'block'
		});
		event.preventDefault();
	});
	
	$('.media').click(function(event){
		$('#pop').css({
			'display':'block',
			'height':$(document).height(),
			'width':$(document).width()
		});
		$('#add_media').css({
			'display':'block'
		});
		event.preventDefault();
	});
	
	$('.contribute').click(function(event){
		$('#pop').css({
			'display':'block',
			'height':$(document).height(),
			'width':$(document).width()
		});
		$('#contribute').css({
			'display':'block'
		});
		event.preventDefault();
	});
    
    $('.close>a.x,button.close').click(function(event){
        $('#pop, #pop>div').css({
            'display':'none'
        });
        event.preventDefault();
    });
});

