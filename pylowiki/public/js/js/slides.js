$(document).ready(function() {
    
    $('a.slide').click(function(event){
        $('#pop').css({
            'display':'block',
            'height':$(document).height(),
            'width':$(document).width()
        });
        $('#show').css({
			'display':'block',
			'height':'700',
			'width':'840'
		});
		//$slideshow = $('#show h2>p:first-child');
        $slideshow = $('#show h2>p:nth-child(3)'); //since it's float: right, choose 3rd child, not 1st
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
    
    
    $('.close>button').click(function(){
        $('#pop,#suggestion,#show').css({
            'display':'none',
            'height':0,
            'width':0
        });
    });
});
