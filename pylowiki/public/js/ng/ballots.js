function ballotsController($scope, $http) {
    
    if ($scope.ballotSlate == 'measures') {
        $scope.getBallotItemsURL = '/getBallotMeasures/' + $scope.code + '/' + $scope.url;
    } else {
        $scope.getBallotItemsURL = '/getBallotCandidates/' + $scope.code + '/' + $scope.url;
    }

    $scope.updateCandidateVote = function(code, url) {
        var checkVote = $scope.mycandidateVotes[code];
        if (checkVote == 'voted') {
            // they have voted on this item and are reversing their vote
            // which is always okay
            $scope.mycandidateVotes[code] = 'nvote';
            totalVotes = parseInt($scope.totalcandidateVotes[code]);
            totalVotes -= 1;
            $scope.totalcandidateVotes[code] = totalVotes;
            $.post('/rate/ballotcandidate/' + code + '/' + url + '/1');
        } else {
            // they are voting on this item, which is only okay if they have note 
            // already voted the max number of times
            var totalVotes = 0;
            var thisVote = 0;
            for (var key in $scope.mycandidateVotes) {
                thisVote = $scope.mycandidateVotes[key];
                if (thisVote == 'voted') {
                    totalVotes += 1;
                }
            }
            if (totalVotes >= $scope.candidateMax) {
                alert("You have already voted for the maximum number of " + $scope.candidateMax + " items on this ballot.");
            } else {
                $scope.mycandidateVotes[code] = 'voted';
                totalVotes = parseInt($scope.totalcandidateVotes[code]);
                totalVotes += 1;
                $scope.totalcandidateVotes[code] = totalVotes;
                $.post('/rate/ballotcandidate/' + code + '/' + url + '/1');
            }
            
        }

        

    };
    
    $scope.getBallotItems = function() {
		$scope.loading = true;
		$http.get($scope.getBallotItemsURL).success(function(data){
			if (data.statusCode == 1){
				$scope.activity = [];
				$scope.alertMsg = data.alertMsg;
				$scope.alertType = data.alertType;
			} 
			else if (data.statusCode === 0){
				$scope.activity = data.result;
				if ($scope.ballotSlate == 'candidates') {
                    $scope.mycandidateVotes = data.mycandidateVotes;
                    $scope.totalcandidateVotes = data.totalcandidateVotes;
                    $scope.candidateMax = parseInt(data.candidateMax);
				}
			}
			$scope.loading = false;
		});
	};

	$scope.getBallotItems();
}

