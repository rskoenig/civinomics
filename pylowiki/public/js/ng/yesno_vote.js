function yesNoVoteCtrl($scope) {
    // initialize the yes/no percentages
    if ($scope.totalVotes == 0){
        $scope.yesPercent = 0;
        $scope.noPercent = 0;
    }
    else if(!($scope.inPage)){
        $scope.yesPercent = $scope.yesVotes / $scope.totalVotes * 100;
        $scope.noPercent = $scope.noVotes / $scope.totalVotes * 100;
    }

    // set the appropriate voting icon
    if ($scope.rated == 0) {
        $scope.voted = '';
    }
    else if ($scope.rated == 1){
        $scope.voted = 'yesVoted';
    }
    else if ($scope.rated == -1){
        $scope.voted = 'noVoted';
    }

    $scope.updateYesVote = function(){
        if ($scope.voted == ''){
            // the user is voting yes from a neutral vote; the score goes up by one
            activateVoteShareModal(1);
            $scope.totalVotes += 1;
            $scope.netVotes += 1;
            $scope.yesVotes += 1;
            $scope.voted = 'yesVoted';
            $scope.rated = 1;
        } else if ($scope.voted == 'noVoted'){
            // the user is switching a no vote to a yes vote; the score goes up by two
            activateVoteShareModal(1);
            $scope.netVotes += 2;
            $scope.yesVotes += 1;
            $scope.noVotes -= 1; 
            $scope.voted = 'yesVoted';
            $scope.rated = 1;
        } else if ($scope.voted = 'yesVoted'){
            // the user is undoing their yes vote
            activateVoteShareModal(0);
            $scope.totalVotes -= 1;
            $scope.netVotes -= 1;
            $scope.yesVotes -= 1;
            $scope.voted = '';
            $scope.rated = 0;
        }

        // recalculate the yes/no percentages
        if ($scope.totalVotes == 0){
            $scope.yesPercent = 0;
            $scope.noPercent = 0;
        }
        else{
            $scope.yesPercent = $scope.yesVotes / $scope.totalVotes * 100;
            $scope.noPercent = $scope.noVotes / $scope.totalVotes * 100;
        }

        if ($scope.objType == 'comment') {
            $.post('/rate/' + $scope.objType + '/' + $scope.urlCode + '/1');
        } else {
            $.post('/rate/' + $scope.objType + '/' + $scope.urlCode + '/' + $scope.url + '/1');
        }
    }

    $scope.updateNoVote = function(){
        if ($scope.voted == ''){
            // the user is voting no from a neutral vote; the score goes down by one
            activateVoteShareModal(-1);
            $scope.totalVotes += 1;
            $scope.netVotes -= 1;
            $scope.noVotes += 1;
            $scope.voted = 'noVoted';
            $scope.rated = -1;
        }else if ($scope.voted == 'yesVoted'){
            // if the user had previously placed a yes vote, the score goes down by two
            activateVoteShareModal(-1);
            $scope.netVotes -= 2;
            $scope.yesVotes -= 1;
            $scope.noVotes += 1;
            $scope.voted = 'noVoted';
            $scope.rated = -1;
        }else if ($scope.voted = 'noVoted'){
            // the user is undoing a no vote
            activateVoteShareModal(0);
            $scope.totalVotes -= 1
            $scope.netVotes += 1
            $scope.noVotes -=1
            $scope.voted = '';
            $scope.rated = 0;
        }

        // recalculate the yes/no percentages
        if ($scope.totalVotes == 0){
            $scope.yesPercent = 0;
            $scope.noPercent = 0;
        }
        else{
            $scope.yesPercent = $scope.yesVotes / $scope.totalVotes * 100;
            $scope.noPercent = $scope.noVotes / $scope.totalVotes * 100;
        }

        if ($scope.objType == 'comment') {
            $.post('/rate/' + $scope.objType + '/' + $scope.urlCode + '/-1');
        } else {
            $.post('/rate/' + $scope.objType + '/' + $scope.urlCode + '/' + $scope.url + '/-1');
        }
    }

    // make sure modal doesn't show on load
    $('#voteShareModal').modal({show:false});
    function activateVoteShareModal(newVote) {
        // only activates if vote is cast
        //console.log("show me the modal!");
        changePie(newVote);
        if (newVote != 0) {
            $('#voteShareModal').modal({show:true});
        }
    }
};