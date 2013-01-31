$(document).ready(function() {
	
	$('button.delete').click(function(event){
		$(this).parent().parent().remove();
		event.preventDefault();
	});
	
	$('button.add').click(function(){
		$('#education tr:last').clone().appendTo('#education');
		event.preventDefault();
	});
	
});
