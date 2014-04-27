function activityController($scope, $http) {
	$scope.listingType = 'activity';
	$scope.activityLoading = true;
	$scope.activitySliceLoading = false;
	$scope.noMoreSlices = false;
	$scope.busy = false;
	$scope.sliceSize = 7;
	$scope.offset = $scope.sliceSize;
	$scope.activityUrl = '/getActivity/' + $scope.activityType

	$scope.getActivity = function() {
		$scope.alertMsg = ''
		$scope.activityLoading = true;
		$http.get($scope.activityUrl).success(function(data){
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

    if ($scope.code){
        $scope.activityUrl = '/getActivity/' + $scope.activityType + '/' + $scope.code + '/' + $scope.url
        $scope.getActivity();
    }else{
        $scope.getActivity();
    }
        

	$scope.getAllActivity = function(){
		$scope.activityType = 'all';
		$scope.getActivity();
		$scope.offset = $scope.sliceSize;
	};

	$scope.getFollowingActivity = function(){
		$scope.activityType = 'following';
		$scope.getActivity();
		$scope.offset = $scope.sliceSize;
	};

	$scope.getGeoActivity = function(){
		$scope.activityType = 'geo';
		$scope.getActivity();
		$scope.offset = $scope.sliceSize;
	};

	$scope.browseInitiatives = function(){
		$scope.activityType = 'initiatives';
		$scope.getActivity();
		$scope.offset = $scope.sliceSize;
	};

	$scope.getActivitySlice = function() {
		if ($scope.busy || $scope.noMoreSlices) return;
		$scope.busy = true;
		$scope.alertMsg = ''
		$scope.activitySliceLoading = true;
		if ($scope.code){
		    $scope.sliceUrl = '/getActivitySlice/0/' + $scope.activityType + '/' + $scope.code + '/' + $scope.url + '/' + $scope.offset;
		}else{
		    $scope.sliceUrl = '/getActivitySlice/0/' + $scope.activityType + '/' + $scope.offset;
		}
		$http.get($scope.sliceUrl).success(function(data){
			if (data.statusCode == 1){
				$scope.noMoreSlices = true;
			} 
			else if (data.statusCode === 0){
				activitySlice = data.result;
				for (var i = 0; i < activitySlice.length; i++) {
				    $scope.activity.push(activitySlice[i]);
				}
				$scope.noMoreSlices = false;
			}
			$scope.activitySliceLoading = false;
			$scope.busy = false;
			$scope.offset += $scope.sliceSize;
		})
	};

}