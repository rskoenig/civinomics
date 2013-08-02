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
            var noScore = ($(this).children(".noScore").html()*1);
            noScore = noScore - 1;
            $(this).children(".noScore").html(noScore);

            var totalVotes = ($(this).siblings(".totalVotesWrapper").children(".totalVotes").html()*1);
            totalVotes = totalVotes - 1;
            $(this).siblings(".totalVotesWrapper").children(".totalVotes").html(totalVotes)
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
                var noScore = ($(this).children(".noScore").html()*1);
                noScore = noScore + 1;
                $(this).children(".noScore").html(noScore); 

                var yesScore = ($(this).children(".yesScore").html()*1);
                yesScore = yesScore - 1;
                $(this).children(".yesScore").html(yesScore);    
            } else {
                 // a noVote from a neutral vote will bring the score down one place
                 // (assuming there has not previously been a vote on this comment by this person)
                var noScore = ($(this).children(".noScore").html()*1);
                noScore = noScore + 1;
                $(this).children(".noScore").html(noScore);

                var totalVotes = ($(this).siblings(".totalVotesWrapper").children(".totalVotes").html()*1);
                totalVotes = totalVotes + 1;
                $(this).siblings(".totalVotesWrapper").children(".totalVotes").html(totalVotes)
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
            var yesScore = ($(this).children(".yesScore").html()*1);
            yesScore = yesScore - 1;
            $(this).children(".yesScore").html(yesScore);

            var totalVotes = ($(this).siblings(".totalVotesWrapper").children(".totalVotes").html()*1);
            totalVotes = totalVotes - 1;
            $(this).siblings(".totalVotesWrapper").children(".totalVotes").html(totalVotes)
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
                var noScore = ($(this).children(".noScore").html()*1);
                noScore = noScore - 1;
                $(this).children(".noScore").html(noScore); 

                var yesScore = ($(this).children(".yesScore").html()*1);
                yesScore = yesScore + 1;
                $(this).children(".yesScore").html(yesScore);    
            } else {
                 // an yesVote from a neutral vote will bring the score up one place
                 // (assuming there has not previously been a vote on this comment by this person)
                var yesScore = ($(this).children(".yesScore").html()*1);
                yesScore = yesScore + 1;
                $(this).children(".yesScore").html(yesScore);

                var totalVotes = ($(this).siblings(".totalVotesWrapper").children(".totalVotes").html()*1);
                totalVotes = totalVotes + 1;
                $(this).siblings(".totalVotesWrapper").children(".totalVotes").html(totalVotes)
            }
        }
        $.post($(this).attr('href'));
    });
});
