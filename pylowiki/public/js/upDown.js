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
            // NOTE: this code does not work - no image change happening
            // $(this).children('img').attr("src", downURL);
         
            // having already placed a downvote, we will bring the score back up one place
            // (assuming there has not previously been a vote on this comment by this person)   
            $(this).attr("class", "downVote");
            var currentScore = ($(this).siblings(".chevron-score").html()*1);
            currentScore = currentScore + 1;
            $(this).siblings(".chevron-score").html(currentScore);
        }
        else
        {
            // NOTE: this code does not work - no image change happening
            // $(this).children('img').attr("src", votedDownURL);
            // NOTE: this code does not work - no image change happening
            // $(this).siblings('.upVote').children('img').attr('src', upURL);

            $(this).attr("class", "downVote voted");
            if ($(this).siblings('.upVote').hasClass('voted')) {
                // replacing an upVote with a downVote will bring the score down two places
                // (assuming there has not previously been a vote on this comment by this person)
                $(this).siblings('.upVote').attr("class", "upVote");
                var currentScore = ($(this).siblings(".chevron-score").html()*1);
                currentScore = currentScore - 2;
                $(this).siblings(".chevron-score").html(currentScore);    
            } else {
                 // a downvote from a neutral vote will bring the score down one place
                 // (assuming there has not previously been a vote on this comment by this person)
                var currentScore = ($(this).siblings(".chevron-score").html()*1);
                currentScore = currentScore - 1;
                $(this).siblings(".chevron-score").html(currentScore);
            }
        }
        $.post($(this).attr('href'));
    });
    
    $(".upVote").click(function(event)
    {
        event.preventDefault();
        if ($(this).hasClass('voted'))
        {
            // NOTE: this code does not work - no image change happening
            // $(this).children('img').attr("src", upURL);

            // having already placed an upVote, we will bring the score back down one place
            // (assuming there has not previously been a vote on this comment by this person)
            $(this).attr("class", "upVote");
            var currentScore = ($(this).siblings(".chevron-score").html()*1);
            currentScore = currentScore - 1;
            $(this).siblings(".chevron-score").html(currentScore);
        }
        else
        {
            // NOTE: this code does not work - no image change happening
            // $(this).children('img').attr("src", votedUpURL);
            // NOTE: this code does not work - no image change happening
            // $(this).siblings('.downVote').children('img').attr('src', downURL);

            $(this).attr("class", "upVote voted");
            if ($(this).siblings('.downVote').hasClass('voted')) {
                // replacing a downVote with an upVote will bring the score up two places
                // (assuming there has not previously been a vote on this comment by this person)
                $(this).siblings('.downVote').attr("class", "downVote");
                var currentScore = ($(this).siblings(".chevron-score").html()*1);
                currentScore = currentScore + 2;
                $(this).siblings(".chevron-score").html(currentScore);    
            } else {
                 // an upVote from a neutral vote will bring the score up one place
                 // (assuming there has not previously been a vote on this comment by this person)
                var currentScore = ($(this).siblings(".chevron-score").html()*1);
                currentScore = currentScore + 1;
                $(this).siblings(".chevron-score").html(currentScore);
            }
        }
        $.post($(this).attr('href'));
    });
});
