function ballotsController($scope, $http) {
    $scope.getBallotMeasuresURL = '/getBallotMeasures/' + $scope.code + '/' + $scope.url;

    $scope.getBallotMeasures = function() {
		$scope.loading = true;
		$http.get($scope.getBallotMeasuresURL).success(function(data){
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

	$scope.getBallotMeasures();
}

