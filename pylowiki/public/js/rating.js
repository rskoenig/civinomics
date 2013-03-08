$(document).ready(function() {
	$('.star-rating>li').click(function(event){
		var w = $('a', this).width(); //remember which star user clicked
		var suggestionTitle = $(this).closest('li.sugg').find('span.colhd>a').html(); //Suggestion title
		var issueURL = $('div#img+ul>li:first-child>a').attr('href'); // Issue url
		$(this).parent().parent().find('li').removeClass('clicked').removeAttr('style');
		$(this).addClass('clicked').css('width',w); //fill all stars up to the above
		$(this).parent().parent().parent().find('.average').animate({
			height: '15'
		});
		$(this).parent().parent().find('p.you-rate').html('Your rating');
		event.preventDefault();
		thisURL = "/issue/" + issueURL + "/suggestion/" + suggestionTitle + "/rate/" + w/16; 
		$.ajax({type: "POST",
		url: thisURL})
	});
});
