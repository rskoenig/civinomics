/*global $:true, jQuery:true */
$(document).ready(function()
{
    $('#voteShareModal').modal({ show: false})
    function activateVoteShareModal(data) {
        // only activates if vote is cast
        //console.log(data);
        var json = JSON.parse(data);
        console.log(json);
        if (json.statusCode == 0) {
            changePie(json.result);
            if (json.result != 0) {
                $('#voteShareModal').modal('show');
            }
        } else {
            console.log("error activateVoteShareModal, something didn't work");
        }
    }
    // images for the Yes No icons are set by CSS - the javascript just adds or removes the 'voted' class
    $(".noVote").click(function(event)
    {
        event.preventDefault();
        if ($(this).hasClass('voted'))
        {
            // removing a noVote, we will bring the score back up
            // it will also reduce the total vote tally by 1 since the user has retracted their vote
            $(this).attr("class", "noVote");

            //get the total votes
            var totalVotes = ($(this).siblings(".totalVotesWrapper").children(".totalVotes").html()*1);
            var noScore = ($(this).children(".ynScoreWrapper").children(".noScore").html()*1);
            noVotes = Math.round(noScore / 100 * totalVotes);
            noVotes -= 1;
            totalVotes -= 1;
            noScore = Math.round(noVotes / totalVotes * 100)
            $(this).children(".ynScoreWrapper").children(".noScore").html(noScore); 
            $(this).siblings(".totalVotesWrapper").children(".totalVotes").html(totalVotes);

            var yesScore = ($(this).siblings(".yesVote").children(".ynScoreWrapper").children(".yesScore").html()*1);
            yesScore = 100 - noScore;
            $(this).siblings(".yesVote").children(".ynScoreWrapper").children(".yesScore").html(yesScore);

            //having no longer cast a vote yes/no totals are hidden
            $(this).siblings(".totalVotesWrapper").children(".orange").attr("class", "orange");
            $(this).children(".ynScoreWrapper").attr("class", "ynScoreWrapper hidden");
            $(this).siblings('.yesVote').children(".ynScoreWrapper").attr("class", "ynScoreWrapper hidden");
        }
        else
        {
            $(this).attr("class", "noVote voted");
            if ($(this).siblings('.yesVote').hasClass('voted')) {
                // replacing a yesVote with a noVote will bring the score down
                // total votes remains unchanged
                $(this).siblings('.yesVote').attr("class", "yesVote");

                var totalVotes = ($(this).siblings(".totalVotesWrapper").children(".totalVotes").html()*1);
                var noScore = ($(this).children(".ynScoreWrapper").children(".noScore").html()*1);
                noScore = noScore + Math.round((1/totalVotes * 100));
                $(this).children(".ynScoreWrapper").children(".noScore").html(noScore); 

                var yesScore = ($(this).siblings(".yesVote").children(".ynScoreWrapper").children(".yesScore").html()*1);
                yesScore = 100 - noScore;
                $(this).siblings(".yesVote").children(".ynScoreWrapper").children(".yesScore").html(yesScore);  


            } else {
                // a noVote from a neutral vote will increase the no %
                // the total votes goes up by 1

                var totalVotes = ($(this).siblings(".totalVotesWrapper").children(".totalVotes").html()*1);
                var noScore = ($(this).children(".ynScoreWrapper").children(".noScore").html()*1);
                noVotes = noScore / 100 * totalVotes;
                noVotes += 1;
                totalVotes += 1;
                noScore = Math.round(noVotes / totalVotes * 100);
                $(this).children(".ynScoreWrapper").children(".noScore").html(noScore);
                $(this).siblings(".totalVotesWrapper").children(".totalVotes").html(totalVotes);

                var yesScore = ($(this).siblings(".yesVote").children(".ynScoreWrapper").children(".yesScore").html()*1);
                yesScore = 100 - noScore;
                $(this).siblings(".yesVote").children(".ynScoreWrapper").children(".yesScore").html(yesScore);

                //remove class hiding the yes/no votes
                $(this).siblings(".totalVotesWrapper").children(".orange").attr("class", "orange hidden");
                $(this).children(".ynScoreWrapper").attr("class", "ynScoreWrapper");
                $(this).siblings(".yesVote").children(".ynScoreWrapper").attr("class", "ynScoreWrapper");
            }
        }
        //$.post($(this).attr('href'));
        $.post( $(this).attr('href'), function( data ) {
            activateVoteShareModal(data);
        }); 
    });
    
    $(".yesVote").click(function(event)
    {
        event.preventDefault();
        if ($(this).hasClass('voted'))
        {
            // removing a yes vote
            // the user removes their vote so the vote count goes down
            $(this).attr("class", "yesVote");
            
            var totalVotes = ($(this).siblings(".totalVotesWrapper").children(".totalVotes").html()*1);
            var yesScore = ($(this).children(".ynScoreWrapper").children(".yesScore").html()*1);
            yesVotes = yesScore / 100 * totalVotes;
            yesVotes -= 1;
            totalVotes = totalVotes - 1;
            yesScore = Math.round(yesVotes / totalVotes * 100);
            $(this).children(".ynScoreWrapper").children(".yesScore").html(yesScore); 
            $(this).siblings(".totalVotesWrapper").children(".totalVotes").html(totalVotes);

            // now adjust the no score
            var noScore = ($(this).siblings(".noVote").children(".ynScoreWrapper").children(".noScore").html()*1);
            noScore = 100 - yesScore;
            $(this).siblings(".noVote").children(".ynScoreWrapper").children(".noScore").html(noScore);

            //having no longer cast a vote yes/no totals are hidden
            $(this).siblings(".totalVotesWrapper").children(".orange").attr("class", "orange");
            $(this).siblings(".noVote").children(".ynScoreWrapper").attr("class", "ynScoreWrapper hidden");
            $(this).children(".ynScoreWrapper").attr("class", "ynScoreWrapper hidden");
        }
        else
        {   
            // replacing a noVote with a yesVote
            $(this).attr("class", "yesVote voted");
            if ($(this).siblings('.noVote').hasClass('voted')) {
                $(this).siblings('.noVote').attr("class", "noVote");

                var totalVotes = ($(this).siblings(".totalVotesWrapper").children(".totalVotes").html()*1);
                var yesScore = ($(this).children(".ynScoreWrapper").children(".yesScore").html()*1);
                yesScore = yesScore + Math.round(1/totalVotes * 100);
                $(this).children('.ynScoreWrapper').children(".yesScore").html(yesScore); 

                var noScore = ($(this).siblings(".noVote").children(".ynScoreWrapper").children(".noScore").html()*1);
                noScore = 100 - yesScore;
                $(this).siblings(".noVote").children(".ynScoreWrapper").children(".noScore").html(noScore); 


            } else {
                 // a yesVote from a neutral vote 
                 // it will also add to the total vote tally

                var totalVotes = ($(this).siblings(".totalVotesWrapper").children(".totalVotes").html()*1);
                var yesScore = ($(this).children('.ynScoreWrapper').children(".yesScore").html()*1);
                yesVotes = yesScore / 100 * totalVotes;
                yesVotes += 1;
                totalVotes += 1;
                yesScore = Math.round(yesVotes / totalVotes * 100);
                $(this).children(".ynScoreWrapper").children(".yesScore").html(yesScore);
                $(this).siblings(".totalVotesWrapper").children(".totalVotes").html(totalVotes);

                var noScore = ($(this).siblings('.noVote').children('.ynScoreWrapper').children('.noScore').html()*1);
                noScore = 100 - yesScore;
                $(this).siblings('.noVote').children('.ynScoreWrapper').children('.noScore').html(noScore);

                //remove class hiding the yes/no votes
                $(this).siblings(".totalVotesWrapper").children(".orange").attr("class", "orange hidden");
                $(this).siblings(".noVote").children(".ynScoreWrapper").attr("class", "ynScoreWrapper");
                $(this).children(".ynScoreWrapper").attr("class", "ynScoreWrapper");
            }
        }
        //$.post($(this).attr('href'));
        $.post($(this).attr('href'), function( data ) {
            activateVoteShareModal(data);
        });
    });
});
