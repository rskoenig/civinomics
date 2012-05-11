/*
    Author: Edolfo Garza-Licudine
    Contact: edolfo@civinomics.com
    Date: 4 May 2012
    
    Inelegant and brute-forced =(.
*/

/*global $:true, jQuery:true */
$(document).ready(function()
{
    var upURL = '/images/icons/glyphicons/glyphicons_343_thumbs_up.png';
    var votedUpURL = '/images/icons/glyphicons/glyphicons_343_thumbs_up_green.png';
    
    var downURL = '/images/icons/glyphicons/glyphicons_344_thumbs_down.png';
    var votedDownURL = '/images/icons/glyphicons/glyphicons_344_thumbs_down_red.png';
    
    $(".downVote").click(function(event)
    {
        event.preventDefault();
        if ($(this).hasClass('voted'))
        {
            $(this).children('img').attr("src", downURL);
            $(this).attr("class", "downVote");
        }
        else
        {
            $(this).children('img').attr("src", votedDownURL);
            $(this).attr("class", "downVote voted");
            $(this).siblings('.upVote').children('img').attr('src', upURL);
            $(this).siblings('.upVote').attr('class', 'upVote');
        }
        $.post($(this).attr('href'));
    });
    
    $(".upVote").click(function(event)
    {
        event.preventDefault();
        if ($(this).hasClass('voted'))
        {
            $(this).children('img').attr("src", upURL);
            $(this).attr("class", "upVote");
        }
        else
        {
            $(this).children('img').attr("src", votedUpURL);
            $(this).attr("class", "upVote voted");
            $(this).siblings('.downVote').children('img').attr('src', downURL);
            $(this).siblings('.downVote').attr('class', 'downVote');
        }
        $.post($(this).attr('href'));
    });
});
