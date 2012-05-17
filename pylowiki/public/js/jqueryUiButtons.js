/************************************************************************
*************************************************************************
@Name :       	custom jquery UI Slider
@Revison :    	1.0
@Date : 		12/04/2012
@Author:     	 Todd Anderson / Civinomics 
@License :		 
 


**************************************************************************
*************************************************************************/
(function($) {	
	$.fn.jUpButton = function(op) {
				
		if(this.length>0)
		this.each(function(idx, element) {
			var thisID = element.id,
			thingCode = $(this).attr('data').split('_')[0], 	// this page's code
			thingURL = $(this).attr('data').split('_')[1], 	// this page's url
			ratingType = $(this).attr('data').split('_')[2];
				
			$(this).button({ 
					
			})
			.click(function() {
				$.ajax({
					type : 'POST',
					url  : "/rating/rate/"+ thingCode +"/"+ thingURL +"/${c.authuser['urlCode']}/${c.authuser['url']}",
					data : "rate=" + 1 + "&type=" + ratingType,
					async : false,
					success: function(result) {
						input_content = result;
					}
				});
			});				
			/*
			$(this).css( "width", "16px" );
			$(this).css( "height", "19px" );
			$(this).css( "background-image", "url(/images/thumb_up_green.gif)" );
			*/
		});

	}
	$.fn.jDownButton = function(op) {
				
		if(this.length>0)
		this.each(function(idx, element) {
			var thisID = element.id,
			thingCode = $(this).attr('data').split('_')[0], 	// this page's code
			thingURL = $(this).attr('data').split('_')[1], 	// this page's url
			ratingType = $(this).attr('data').split('_')[2];
				
			$(this).button({ 
					
			})
			.click(function() {
				$.ajax({
					type : 'POST',
					url  : "/rating/rate/"+ thingCode +"/"+ thingURL +"/${c.authuser['urlCode']}/${c.authuser['url']}",
					data : "rate=" + -1 + "&type=" + ratingType,
					async : false,
					success: function(result) {
						input_content = result;
					}
				});
			});				
			/*
			$(this).css( "width", "16px" );
			$(this).css( "height", "19px" );
			$(this).css( "background-image", "url(/images/thumb_down_red.gif)" );
			*/
		});

	}
})(jQuery);