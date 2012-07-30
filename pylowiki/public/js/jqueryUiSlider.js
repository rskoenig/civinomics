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
	$.fn.jColorSlider = function(op) {
		function hexFromInput( i ) {
			// compute r, g and b from the input value (0..100)
			// r, g and b's final values will range between 0 and 255 (hex color range) 
			// g goes low to high from input 0 and 47:
			var iG = i;
			if (iG > 47) {
				iG = 47;
			}
			var cG = (iG * 255);
			if (cG != 0) {
				cG = (cG / 47); 
			}
			cG = Math.round(cG);
			// r goes high to low from input 53 to 100
			var iR = 100 - i;
			if (iR > 47) {
				iR = 47;
			}
			var cR = (iR * 255);
			if (cR != 0) {
				cR = (cR / 47);
			}
			cR = Math.round(cR);
			// b goes 0 to 85 from input 0 to 100
			var cB = (i * 85);
			if (cB != 0) {
				cB = (cB / 100); 
			}
			cB = Math.round(cB);
			var hex = [
				cR.toString( 16 ),
				cG.toString( 16 ),
				cB.toString( 16 )
			];
			$.each( hex, function( nr, val ) {
				if ( val.length === 1 ) {
					hex[ nr ] = "0" + val;
				}
			});
			return hex.join( "" ).toUpperCase();
		}
				
		if(this.length>0)
		this.each(function(idx, element) {
				var thisID = element.id,
                averageRating = parseFloat($(this).attr('data1').split('_')[0]),    // rating's average score
                thingCode = $(this).attr('data1').split('_')[1],    // this page's code
                myRating  = parseFloat($(this).attr('data1').split('_')[2]),    // user's own rating
                ratingType = $(this).attr('data1').split('_')[3],   // type of the rating
                isRated = $(this).attr('data1').split('_')[4];      // if user has rated this yet
                ratingHandler = $(this).attr('data1').split('_')[5],        // for the ajax handler URL below
                thingURL = $(this).attr('data2');   // this page's url
                var isMsie = $.browser.msie;

				$(this).slider({
					orientation: "horizontal",
					range: "min",
					max: 100,
					value: 50,
					step: 1,
                    start: function(event, ui) {
                        var sliderVal = ui.value;
                        hex = hexFromInput( sliderVal );
                        $(this).css( "background", "#" + hex );
                        $(this).children(" .ui-widget-header").css( "background", "#" + hex );
                        if (!isMsie) {
                            $(this).children(" .ui-slider-handle").html( '<span class="handleVal"></span>' );
                        }
                    },
                    slide: function(event, ui) {
                        var sliderVal = ui.value;
                        hex = hexFromInput( sliderVal );
                        $(this).css( "background", "#" + hex );
                        $(this).children(" .ui-widget-header").css( "background", "#" + hex );
                        if (!isMsie) {
                            $(this).children(" .ui-slider-handle").html( '<span class="handleVal">'+sliderVal+'</span>' );
                        }
                    },
					change: function(event, ui) {
						var sliderVal = ui.value;
						hex = hexFromInput( sliderVal );
						$(this).css( "background", "#" + hex );
						$(this).children(".ui-widget-header").css( "background", "#" + hex );
						$(this).children(".ui-slider-handle").html( '<span class="handleVal">'+sliderVal+'</span>' );
					},
					stop: function(event, ui) {
						var sliderVal = ui.value;
						hex = hexFromInput( sliderVal );
						$(this).children(".ui-widget-header").css( "background", "#" + hex );
						$(this).css( "background", "#" + hex );
						$(this).children(".ui-slider-handle").html( '<span class="handleVal">'+sliderVal+'</span>' );
						// this code isn't portable for other pages, but is a good example of how to update the rating on page if desired
						//$(this).parents('.gray rating wide').children('.yourRating_' + thisID).html('Your rating: '+sliderVal);
						$.ajax({
							type : 'POST',
							url  : "/"+ratingHandler+"/"+thingCode+"/"+thingURL+"/"+sliderVal,
							data : "rate=" + sliderVal + "&type=" + ratingType,
							async : false,
							success: function(result) {
								input_content = result;
							}
						});
					}
				});
				// if the user has rated this, we initialize the slider to reflect this value
				if (isRated == 'true') {
					myRating = parseInt(myRating);
					$(this).slider('value', myRating);
				}
				if ($(this).hasClass('survey_slider')) {
					$(this).children(".ui-slider-handle").css( "width", "44px" );
					$(this).children(".ui-slider-handle").css( "height", "41px" );
					$(this).children(".ui-slider-handle").css( "cursor", "default" );
					$(this).children(".ui-slider-handle").css( "margin-top", "5px" );
					$(this).children(".ui-slider-handle").css( "margin-right", "20px" );
					$(this).children(".ui-slider-handle").css( "margin-left", "-1em" );
					$(this).children(".ui-slider-handle").css( "border", "none" );
					$(this).children(".ui-slider-handle").css( "background-image", "url(/images/sliderHandle_survey.png)" );
				} else if ($(this).hasClass('normal_slider')) {
					$(this).children(".ui-slider-handle").css( "width", "20px" );
					$(this).children(".ui-slider-handle").css( "height", "31px" );
					$(this).children(".ui-slider-handle").css( "cursor", "default" );
					$(this).children(".ui-slider-handle").css( "margin-top", "4px" );
					$(this).children(".ui-slider-handle").css( "margin-right", "15px" );
					$(this).children(".ui-slider-handle").css( "border", "none" );
					$(this).children(".ui-slider-handle").css( "background-image", "url(/images/sliderHandle.png)" );
				} else {
					$(this).children(".ui-slider-handle").css( "width", "10px" );
					$(this).children(".ui-slider-handle").css( "height", "16px" );
					$(this).children(".ui-slider-handle").css( "cursor", "default" );
					$(this).children(".ui-slider-handle").css( "margin-top", "4px" );
					$(this).children(".ui-slider-handle").css( "margin-right", "15px" );
					$(this).children(".ui-slider-handle").css( "border", "none" );
					$(this).children(".ui-slider-handle").css( "background-image", "url(/images/sliderHandle_small.png)" );
				}
				
			});


	}
})(jQuery);
