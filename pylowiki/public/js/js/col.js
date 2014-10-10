$(document).ready(function(){
    
    var onewid = $('.one').width();
    var oneht = $('.one>ul').outerHeight();
    var twowid = $('.two').width();
    var twoht = $('.two>ul').outerHeight();
    var threeht = $('.three').height(); //since there's no padding, margin or border
    var headht = $('#survey').outerHeight(); //since there's padding
    
    $('.one>ul>li, .two>ul>li').append('<hr />');
    $('.one hr').width(onewid);
    $('.two hr').width(twowid);
    
    threeht = threeht - headht; // normalizes third column's height to not include the h3 at the top
    
    if ( oneht > threeht ) // Check if first column's height is larger than third's
    {
        $('.one>ul').height(threeht); // Force first column to be the same height as third's
        $('.one>ul').css({ // Add vertical scrollbar
            'overflow':'hidden',
            'overflow-y':'scroll'
        });
    }
    
    if ( twoht > threeht ) // Same as for first column
    {
        $('.two>ul').height(threeht);
        $('.two>ul').css({
            'overflow':'hidden',
            'overflow-y':'scroll'
        });
    }
    
});