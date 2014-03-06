function profileController($scope, $http) {	
	$scope.activityLoading = true;
	$scope.activitySliceLoading = false;
	$scope.noMoreSlices = false;
	$scope.busy = false;
	$scope.sliceSize = 7;
	$scope.offset = $scope.sliceSize;

	$scope.getMemberActivity = function() {
		$scope.alertMsg = ''
		$scope.activityLoading = true;
		$http.get('/getMemberActivity/' + $scope.memberCode + '/' + $scope.memberURL).success(function(data){
			if (data.statusCode == 1){
				$scope.activityNoResult = true;
				$scope.alertMsg = data.alertMsg;
				$scope.alertType = data.alertType;
			} 
			else if (data.statusCode === 0){
				$scope.activityNoResult = false;
				$scope.memberActivity = data.result;		
			}
			$scope.activityLoading = false;
		})
	};

	$scope.getMemberActivity()
}