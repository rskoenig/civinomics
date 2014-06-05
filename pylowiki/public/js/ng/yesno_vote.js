function yesNoVoteCtrl($scope) {
    // initialize the yes/no percentages
    if ($scope.totalVotes == 0){
        $scope.yesPercent = 0;
        $scope.noPercent = 0;
    }
    else{
        $scope.yesPercent = $scope.yesVotes / $scope.totalVotes * 100;
        $scope.noPercent = $scope.noVotes / $scope.totalVotes * 100;
    }
    // set the appropriate voting icon
    if ($scope.rated == 0) {
        $scope.yesVoted = '';
        $scope.noVoted = '';
        $scope.display = 'hidden';
    }
    else if ($scope.rated == 1){
        $scope.yesVoted = 'voted';
        $scope.noVoted = '';
        $scope.display = '';
    }
    else if ($scope.rated == -1){
        $scope.yesVoted = '';
        $scope.noVoted = 'voted';
        $scope.display = '';
    }

    $scope.updateYesVote = function(){

        if ($scope.yesVoted == '')
        {
            // the user is voting yes from a neutral vote; the score goes up by one
            if ($scope.noVoted == ''){
                $scope.totalVotes += 1;
                $scope.netVotes += 1;
                $scope.yesVotes += 1;
                $scope.display = '';
            }
            // the user is switching a no vote to a yes vote; the score goes up by two
            else{
                $scope.netVotes += 2;
                $scope.yesVotes += 1;
                $scope.noVotes -= 1;
            }
            $scope.yesVoted = 'voted';
            $scope.noVoted = '';
        }

        // the user is undoing their yes vote
        else if ($scope.yesVoted = 'voted')
        {
            $scope.totalVotes -= 1;
            $scope.netVotes -= 1;
            $scope.yesVotes -= 1;
            $scope.yesVoted = '';
            $scope.display = 'hidden';
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
        if ($scope.noVoted == '')
        {
            // the user is voting no from a neutral vote; the score goes down by one
            if ($scope.yesVoted == ''){
                $scope.totalVotes += 1;
                $scope.netVotes -= 1;
                $scope.noVotes += 1;
                $scope.display = '';
            }
            // if the user had previously placed a yes vote, the score goes down by two
            else{
                $scope.netVotes -= 2;
                $scope.yesVotes -= 1;
                $scope.noVotes += 1;
            }
            $scope.noVoted = 'voted';
            $scope.yesVoted = ''
        }
        // the user is undoing a no vote
        else if ($scope.noVoted = 'voted')
        {
            $scope.totalVotes -= 1
            $scope.netVotes += 1
            $scope.noVotes -=1
            $scope.noVoted = '';
            $scope.display = 'hidden';
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
};