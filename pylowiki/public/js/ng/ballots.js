function ballotsController($scope, $http) {
    
    if ($scope.ballotSlate == 'measures') {
        $scope.getBallotItemsURL = '/getBallotMeasures/' + $scope.code + '/' + $scope.url;
    } else {
        $scope.getBallotItemsURL = '/getBallotCandidates/' + $scope.code + '/' + $scope.url;
    }

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
			}
			$scope.loading = false;
		});
	};

	$scope.getBallotItems();
}

