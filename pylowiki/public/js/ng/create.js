function createController($scope, $http) {

	$scope.createUrl = '/profile/' + $scope.authorCode + '/' + $scope.authorUrl + '/createInitiative'; 
	
	$scope.createNew = function() {
        var createData = {'submit':'submit', 'title': $scope.title, 'description': $scope.description, 'scope': $scope.scope, 'tags': $scope.tags};
		//$scope.newObjURL = '/add/' + $scope.objType + '/handler';
		$http.post($scope.createUrl, createData).success(function(data){
            $scope.success = true
            $scope.newObjUrl = data.newObjUrl
		});
	}

	$scope.getActivity = function() {
		$scope.alertMsg = ''
		$scope.activityLoading = true;
		$http.get('/getSiteActivity' + $scope.activityType).success(function(data){
			if (data.statusCode == 1){
				$scope.activityNoResult = true;
				$scope.activity = []
				$scope.alertMsg = data.alertMsg;
				$scope.alertType = data.alertType;
			} 
			else if (data.statusCode === 0){
				$scope.activityNoResult = false;
				$scope.noMoreSlices = false;
				$scope.activity = data.result;
				
			}
			$scope.activityLoading = false;
		})
	};

}