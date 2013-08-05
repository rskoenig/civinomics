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
            // we will also reduce the total vote tally by 1 since the user has retracted their vote
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
                // replacing a yesVote with a noVote will bring the tally/score of no votes up 1 and the tally/score of yes votes down 1
                // total votes remains unchanged
                // (assuming there has not previously been a vote on this comment by this person)
                $(this).siblings('.yesVote').attr("class", "yesVote");
                var noScore = ($(this).children(".noScore").html()*1);
                noScore = noScore + 1;
                $(this).children(".noScore").html(noScore); 

                var yesScore = ($(this).siblings(".yesVote").children(".yesScore").html()*1);
                yesScore = yesScore - 1;
                $(this).siblings(".yesVote").children(".yesScore").html(yesScore);    
            } else {
                 // a noVote from a neutral vote will add to the no tally/score
                 // the total votes goes up by 1
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

            // having already placed a yesVote, we will bring the score back down one place
            // the user removes their vote so the vote count goes down
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
                // replacing a noVote with a yesVote will bring the yes score up 1 and the no score down 1
                // (assuming there has not previously been a vote on this comment by this person)
                $(this).siblings('.noVote').attr("class", "noVote");
                var noScore = ($(this).siblings(".noVote").children(".noScore").html()*1);
                noScore = noScore - 1;
                $(this).siblings(".noVote").children(".noScore").html(noScore); 

                var yesScore = ($(this).children(".yesScore").html()*1);
                yesScore = yesScore + 1;
                $(this).children(".yesScore").html(yesScore);    
            } else {
                 // a yesVote from a neutral vote will bring the score up 1 place
                 // it will also add to the total vote tally
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
