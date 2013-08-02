/*
    Author: Edolfo Garza-Licudine
    Contact: edolfo@civinomics.com
    Date: 4 May 2012
    
    Inelegant and brute-forced =(.
*/

/*global $:true, jQuery:true */
$(document).ready(function()
{
    var upURL = '/images/yes_blank.png';
    var votedUpURL = '/images/yes_selected.png';
    
    var downURL = '/images/no_blank.png';
    var votedDownURL = '/images/no_selected.png';
    
    $(".noVote").click(function(event)
    {
        event.preventDefault();
        if ($(this).hasClass('voted'))
        {
            $(this).children('img').attr("src", downURL);
         
            // having already placed a noVote, we will bring the score back up one place
            // (assuming there has not previously been a vote on this comment by this person)   
            $(this).attr("class", "noVote");
            var currentScore = ($(this).siblings(".yesNo-score").html()*1);
            currentScore = currentScore + 1;
            $(this).siblings(".yesNo-score").html(currentScore);
        }
        else
        {
            $(this).children('img').attr("src", votedDownURL);
            $(this).siblings('.yesVote').children('img').attr('src', upURL);

            $(this).attr("class", "noVote voted");
            if ($(this).siblings('.yesVote').hasClass('voted')) {
                // replacing a yesVote with a noVote will bring the score down two places
                // (assuming there has not previously been a vote on this comment by this person)
                $(this).siblings('.yesVote').attr("class", "yesVote");
                var currentScore = ($(this).siblings(".yesNo-score").html()*1);
                currentScore = currentScore - 2;
                $(this).siblings(".yesNo-score").html(currentScore);    
            } else {
                 // a noVote from a neutral vote will bring the score down one place
                 // (assuming there has not previously been a vote on this comment by this person)
                var currentScore = ($(this).siblings(".yesNo-score").html()*1);
                currentScore = currentScore - 1;
                $(this).siblings(".yesNo-score").html(currentScore);
            }
        }
        $.post($(this).attr('href'));
    });
    
    $(".yesVote").click(function(event)
    {
        event.preventDefault();
        if ($(this).hasClass('voted'))
        {
            $(this).children('img').attr("src", upURL);

            // having already placed an yesVote, we will bring the score back down one place
            // (assuming there has not previously been a vote on this comment by this person)
            $(this).attr("class", "yesVote");
            var currentScore = ($(this).siblings(".yesNo-score").html()*1);
            currentScore = currentScore - 1;
            $(this).siblings(".yesNo-score").html(currentScore);
        }
        else
        {
            $(this).children('img').attr("src", votedUpURL);
            $(this).siblings('.noVote').children('img').attr('src', downURL);

            $(this).attr("class", "yesVote voted");
            if ($(this).siblings('.noVote').hasClass('voted')) {
                // replacing a noVote with an yesVote will bring the score up two places
                // (assuming there has not previously been a vote on this comment by this person)
                $(this).siblings('.noVote').attr("class", "noVote");
                var currentScore = ($(this).siblings(".yesNo-score").html()*1);
                currentScore = currentScore + 2;
                $(this).siblings(".yesNo-score").html(currentScore);    
            } else {
                 // an yesVote from a neutral vote will bring the score up one place
                 // (assuming there has not previously been a vote on this comment by this person)
                var currentScore = ($(this).siblings(".yesNo-score").html()*1);
                currentScore = currentScore + 1;
                $(this).siblings(".yesNo-score").html(currentScore);
            }
        }
        $.post($(this).attr('href'));
    });
});
