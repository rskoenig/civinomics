/************************************************************************
*************************************************************************
@Name :         custom jquery UI Slider
@Revison :      1.0
@Date :         12/04/2012
@Author:         Todd Anderson / Civinomics 
@License :       
 
Changelog:
15 June 2012: Edolfo Garza-Licudine: Changed data parameters for online survey functionality

**************************************************************************
*************************************************************************/
(function($) {
    $.fn.jColorSlider = function(op) {
        function hexFromInput( i ) {
            // compute r, g and b from the input value (0..100)
            // in order to easily separate the color line functions at the midpoint, I'm shifting i down 50

            i = i - 50;
            var cR = 0;
            var cG = 0;
            var cB = 0;
            if (i < 0) {
                // input of -50 -> -1 (color line functions for the left side of slider's midpoint)
                // RED: 185 -> 235
                cR = 0.6 * i + 235;
                // GREEN: 70 -> 234
                cG = 3.7 * i + 234;
                // BLUE: 70 -> 234
                cB = 3.7 * i + 234;
            } else {
                // input of 0 -> 50 (color line functions for the right side of slider's midpoint)
                cR = -2.8 * i + 235;
                // GREEN: 234 -> 135
                cG = -0.9 * i + 234;
                // BLUE: 135 -> 69
                cB = -2.8 * i + 234;
            }
            cR = Math.round(cR);
            cG = Math.round(cG);
            cB = Math.round(cB);

            // convert these values to hex for the webpage
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
                surveyCode = $(this).attr('surveyCode'),    // this survey's code
                surveyURL = $(this).attr('surveyURL'), // this survey's URL
                slideCode = $(this).attr('slideCode'), // this slide's code
                myRating  = parseFloat($(this).attr('rating')),    // user's own rating
                isRated = $(this).attr('isRated'),      // if user has rated this yet
                handler = $(this).attr('href'), // The handler for the ajax
                sliderLabel = $(this).attr('sliderLabel'),  // Unique identifier for the slider
                isMsie = $.browser.msie;

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
                            url  : "/"+handler+"/"+surveyCode+"/"+surveyURL+"/"+slideCode+"/"+sliderVal,
                            data : "rate=" + sliderVal + "&sliderLabel=" + sliderLabel,
                            async : false,
                            success: function(result) {
                                //input_content = result;
                                $('.message').empty().append(result);
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
                    $(this).children(".ui-slider-handle").css( "width", "41px" );
                    $(this).children(".ui-slider-handle").css( "height", "41px" );
                    $(this).children(".ui-slider-handle").css( "cursor", "default" );
                    $(this).children(".ui-slider-handle").css( "margin-top", "5px" );
                    $(this).children(".ui-slider-handle").css( "margin-right", "20px" );
                    $(this).children(".ui-slider-handle").css( "margin-left", "-1em" );
                    $(this).children(".ui-slider-handle").css( "border", "none" );
                    $(this).children(".ui-slider-handle").css( "background-image", "url(/images/sliderHandle.png)" );
                } else if ($(this).hasClass('survey_multiSlider')) {
                    $(this).children(".ui-slider-handle").css( "width", "34px" );
                    $(this).children(".ui-slider-handle").css( "height", "31px" );
                    $(this).children(".ui-slider-handle").css( "cursor", "default" );
                    $(this).children(".ui-slider-handle").css( "margin-top", "5px" );
                    $(this).children(".ui-slider-handle").css( "margin-right", "14px" );
                    $(this).children(".ui-slider-handle").css( "margin-left", "-0.8em" );
                    $(this).children(".ui-slider-handle").css( "border", "none" );
                    $(this).children(".ui-slider-handle").css( "background-image", "url(/images/sliderHandleMulti_survey.png)" );
                }
            });


    }
})(jQuery);
