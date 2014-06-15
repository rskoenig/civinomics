function electionsController($scope, $http) {
    $scope.getBallotsURL = '/getBallots/' + $scope.code + '/' + $scope.url + '/';

    $scope.getBallots = function() {
		$scope.loading = true;
		$http.get($scope.getBallotsURL).success(function(data){
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

	$scope.getBallots();
}

