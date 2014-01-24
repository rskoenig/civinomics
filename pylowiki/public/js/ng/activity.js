function activityController($scope, $http) {
	$scope.activityLoading = true
	$scope.testing = '1 2 3 4'

	$scope.getActivity = function() {
		$scope.activityLoading = true;
		$http.get('/getSiteActivity').success(function(data){
			if (data.statusCode == 1){
				$scope.activityNoResult = true;
			} 
			else if (data.statusCode === 0){
				$scope.activityNoResult = false;
				$scope.activity = data.result;
			}
			$scope.activityLoading = false;
		})
	}

	$scope.getActivity()

}