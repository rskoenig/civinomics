function activityController($scope, $http) {
	$scope.listingType = 'activity';
	if ($scope.activityType == undefined) {
	    $scope.activityType = '/all';
	}
	$scope.activityLoading = true;
	$scope.activitySliceLoading = false;
	$scope.noMoreSlices = false;
	$scope.busy = false;
	$scope.sliceSize = 7;
	$scope.offset = $scope.sliceSize;

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

	$scope.getActivity();

	$scope.geoScope = '';
	$scope.geoFlagUrl = '';

	$scope.getAllActivity = function(){
		$scope.geoScope = '';
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
	
	$scope.getGeoScopedActivity = function(scope, name, url){
		$scope.activityType = '/geo/'+scope;
		$scope.geoScope = scope;
		$scope.geoScopeName = name;
		$scope.geoFlagUrl = url;
		$scope.getActivity();
		$scope.offset = $scope.sliceSize;
	};
	
	$scope.getMeetingActivity = function(){
		$scope.activityType = '/meetings';
		$scope.getActivity();
		$scope.offset = $scope.sliceSize;
	};

	$scope.browseInitiatives = function(){
		$scope.activityType = '/initiatives';
		$scope.getActivity();
		$scope.offset = $scope.sliceSize;
	};

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

}

