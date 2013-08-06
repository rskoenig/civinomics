/*global $:true, jQuery:true */
$(document).ready(function()
{
    // images for the Yes No icons are set by CSS - the javascript just adds or removes the 'voted' class
    $(".noVote").click(function(event)
    {
        event.preventDefault();
        if ($(this).hasClass('voted'))
        {
            // having already placed a noVote, we will bring the score back up one place
            // we will also reduce the total vote tally by 1 since the user has retracted their vote
            $(this).attr("class", "noVote");
            var noScore = ($(this).children(".noScore").html()*1);
            noScore = noScore - 1;
            $(this).children(".noScore").html(noScore);

            var totalVotes = ($(this).siblings(".totalVotesWrapper").children(".totalVotes").html()*1);
            totalVotes = totalVotes - 1;
            $(this).siblings(".totalVotesWrapper").children(".totalVotes").html(totalVotes)

            //having no longer cast a vote yes/no totals are hidden
            $(this).children(".noScore").attr("class", "noScore hidden");
            $(this).siblings('.yesVote').children(".yesScore").attr("class", "yesScore hidden");
        }
        else
        {
            $(this).attr("class", "noVote voted");
            if ($(this).siblings('.yesVote').hasClass('voted')) {
                // replacing a yesVote with a noVote will bring the tally/score of no votes up 1 and the tally/score of yes votes down 1
                // total votes remains unchanged
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
                var noScore = ($(this).children(".noScore").html()*1);
                noScore = noScore + 1;
                $(this).children(".noScore").html(noScore);

                var totalVotes = ($(this).siblings(".totalVotesWrapper").children(".totalVotes").html()*1);
                totalVotes = totalVotes + 1;
                $(this).siblings(".totalVotesWrapper").children(".totalVotes").html(totalVotes)

                //remove class hiding the yes/no votes
                $(this).children(".noScore").attr("class", "noScore");
                $(this).siblings('.yesVote').children(".yesScore").attr("class", "yesScore");
            }
        }
        $.post($(this).attr('href'));
    });
    
    $(".yesVote").click(function(event)
    {
        event.preventDefault();
        if ($(this).hasClass('voted'))
        {
            // having already placed a yesVote, we will bring the score back down one place
            // the user removes their vote so the vote count goes down
            $(this).attr("class", "yesVote");
            var yesScore = ($(this).children(".yesScore").html()*1);
            yesScore = yesScore - 1;
            $(this).children(".yesScore").html(yesScore);

            var totalVotes = ($(this).siblings(".totalVotesWrapper").children(".totalVotes").html()*1);
            totalVotes = totalVotes - 1;
            $(this).siblings(".totalVotesWrapper").children(".totalVotes").html(totalVotes)

            //having no longer cast a vote yes/no totals are hidden
            $(this).siblings(".noVote").children(".noScore").attr("class", "noScore hidden");
            $(this).children(".yesScore").attr("class", "yesScore hidden");
        }
        else
        {
            $(this).attr("class", "yesVote voted");
            if ($(this).siblings('.noVote').hasClass('voted')) {
                // replacing a noVote with a yesVote will bring the yes score up 1 and the no score down 1
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
                var yesScore = ($(this).children(".yesScore").html()*1);
                yesScore = yesScore + 1;
                $(this).children(".yesScore").html(yesScore);

                var totalVotes = ($(this).siblings(".totalVotesWrapper").children(".totalVotes").html()*1);
                totalVotes = totalVotes + 1;
                $(this).siblings(".totalVotesWrapper").children(".totalVotes").html(totalVotes)

                //remove class hiding the yes/no votes
                $(this).siblings(".noVote").children(".noScore").attr("class", "noScore");
                $(this).children(".yesScore").attr("class", "yesScore");
            }
        }
        $.post($(this).attr('href'));
    });
});
