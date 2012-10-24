$(document).ready(function() {
	
	// sets the two column heights equal
	var columnTwo = $('.mail.content>ul').innerHeight();
	var listHeight = $('.mail.list>ul').innerHeight()
	var h3Height = $('.mail.list>h3').innerHeight();
	var columnOne = listHeight + h3Height;
	
	if (columnTwo > columnOne)
	{
		$('.mail.list>ul').height(columnTwo - h3Height - 1); //subtract 1 for the extra border side
	}
	else
	{
		$('.mail.content>ul').height(columnOne + 1); //same as above
	}
});
