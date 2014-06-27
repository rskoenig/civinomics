function adminlistController($scope, $http){
/*
	Not sure what this does yet, so I'll unlock it line by line.
	I want basic functionality first
	-----
	
	$scope.listingType = 'activity';
	$scope.activityType = '/all';
	$scope.activityLoading = true;
	$scope.activitySliceLoading = false;
	$scope.noMoreSlices = false;
	$scope.busy = false;
	$scope.sliceSize = 7;
	$scope.offset = $scope.sliceSize;
*/
	$scope.activityType = '/users';

	$scope.getActivity = function() {
		$scope.alertMsg = '';
		$scope.activityLoading = true;
		$http.get('/getAdminList' + $scope.activityType).success(function(data){
			if (data.statusCode == 1){
				$scope.activityNoResult = true;
				$scope.list = []
				$scope.alertMsg = data.alertMsg;
				$scope.alertType = data.alertType;
			} 
			else if (data.statusCode === 0){
				$scope.activityNoResult = false;
				$scope.noMoreSlices = false;
				$scope.list = data.result;
				
			}
			$scope.activityLoading = false;
		})
	};
	
	$scope.getActivity();
	
/*
	$scope.getAllActivity = function(){
		$scope.activityType = '/all';
		$scope.getActivity();
		$scope.offset = $scope.sliceSize;
	};

	$scope.getFollowingActivity = function(){
		$scope.activityType = '/following';
		$scope.getActivity();
		$scope.offset = $scope.sliceSize;
	};

	$scope.getGeoActivity = function(){
		$scope.activityType = '/geo';
		$scope.getActivity();
		$scope.offset = $scope.sliceSize;
	};

	$scope.browseInitiatives = function(){
		$scope.activityType = '/initiatives';
		$scope.getActivity();
		$scope.offset = $scope.sliceSize;
	};
*/

	$scope.getActivitySlice = function() {
		if ($scope.busy || $scope.noMoreSlices) return;
		$scope.busy = true;
		$scope.alertMsg = ''
		$scope.activitySliceLoading = true;
		$http.get('/getActivitySlice/0' + $scope.activityType + '/' + $scope.offset).success(function(data){
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
	
	$scope.render = function(e) {
    return $(e).html();
    }
	
}