function ballotsController($scope, $http) {
    $scope.getBallotItemsURL = '/getBallotItems/' + $scope.code + '/' + $scope.url;

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

