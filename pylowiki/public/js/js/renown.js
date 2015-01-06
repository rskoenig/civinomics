$(document).ready(function(){

	var w = $(document).innerWidth();
	$('#renown').css({
		'right':w,
	});
	
	$('#renown>p>a>span').hover( //orange on hover
	function(){ //handler in
		$(this).addClass('darkorange')
		$(this).parent().css({
				'text-decoration':'none',
			});
	},
	function(){ //handler out
		$(this).removeClass('darkorange');
	}
	);
	
	var renown_width = $('#renown').width();
	$('#renown>p>a').toggle(
		function() {
			$('#renown').width(400);
			$('#renown>ul').css({
				'display':'block',
				'width':'300',
			});
		},
		function() {
			$('#renown').width(renown_width);
			$('#renown>ul').css({
				'display':'none',
				'width':'0',
			});
		}); //instant transition?
	
	/*$('#renown>p>a').toggle(
		function() {
			$('#renown').width(400);
			$('#renown>ul')
				.css({
					'display':'block'
					})
				.animate({
					width:'300',
				});
			$('#renown>ul>li').css({'visibility':'visible'});
		},
		function() {
			$('#renown>ul>li').css({'visibility':'hidden'});
			$('#renown>ul')
				.animate({
					width:'0',
				}, function(){
				});
					$(this).css({'display':'none'});
		});*/ //smooth transitions?

});
