function initiativeCtrl($scope, $http) {
	$scope.costRegex = /^(\-)?(([1-9]\d{0,2}(,\d{3})*)|(([1-9]\d*)?\d))$/;
    $scope.clearTitle = function() {
        if ($scope.initiativeTitle == 'New Initiative'){
            $scope.initiativeTitle = '';
        }
    };

    $scope.iTest = "rock a doozy";

    /*
    $scope.iCode (init)
    $scope.iUrl (init)*/
    $scope.getUrl = '/initiative/' + $scope.iCode + '/' + $scope.iUrl + '/json';

    $scope.getInitiativeData = function(){
    	$http.get($scope.getUrl).success(function(data){
			if (data.statusCode === 0){
				$scope.noResult = true;
			}
			else if (data.statusCode == 1){
				$scope.noResult = false;
				$scope.initiative = data.initiative;

				$scope.urlCode= $scope.initiative.urlCode;
				$scope.url= $scope.initiative.url;
				$scope.totalVotes= $scope.initiative.voteCount;
				$scope.yesVotes= $scope.initiative.ups;
				$scope.noVotes= $scope.initiative.downs;
				$scope.yesPercent = $scope.yesVotes / $scope.totalVotes * 100;
        		$scope.noPercent = $scope.noVotes / $scope.totalVotes * 100;
				$scope.objType= $scope.initiative.objType;
				$scope.rated= $scope.initiative.rated;
				$scope.goal= $scope.initiative.goal;
				if ($scope.rated == 0) {
			        $scope.voted = '';
			    }
			    else if ($scope.rated == 1){
			        $scope.voted = 'yesVoted';
			    }
			    else if ($scope.rated == -1){
			        $scope.voted = 'noVoted';
			    }

			}
			$scope.loading = false;
		});
    };

    $scope.getInitiativeData();
}
