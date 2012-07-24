$(document).ready(function(){

$('li.dropdown a').toggle(
	function(){
		$('li.dropdown ul').animate({
			height: '120'
		}, 200);
	},
	function(){
		$('li.dropdown ul').animate({
			height: '0'
		}, 200);
	});

});