function geoProfileController($scope, $http) {
	$scope.listingType = 'activity';
	$scope.activityLoading = true;
	$scope.activitySliceLoading = false;
	$scope.noMoreSlices = false;
	$scope.busy = false;
	$scope.sliceSize = 7;
	$scope.offset = $scope.sliceSize;
	$scope.rightAlertMsg = "";
	$scope.showConditional = false;
	$scope.showConditionalType = "";

	$scope.getActivity = function() {
		$scope.alertMsg = ''
		$scope.activityLoading = true;
		console.log($scope.activityType);
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
			console.log($scope.activityLoading);
		})
	};

	console.log($scope.activityLoading);

	$scope.geoScope = '';
	$scope.geoFlagUrl = '/images/flags/homeFlag.gif';
	$scope.geoPopulation = '';

	$scope.getAllActivity = function(){
		$scope.geoScope = '';
		$scope.activityType = '/all';
		$scope.geoFlagUrl = '/images/flags/homeFlag.gif';
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
	
	$scope.getGeoScopedActivity = function(scope, name, url, population, href, photo){
		$scope.activityType = '/geo/'+scope;
		$scope.geoScope = scope;
		$scope.geoScopeName = name;
		$scope.geoFlagUrl = url;
		$scope.geoPopulation = population;
		$scope.geoHref = href;
		$scope.geoPhoto = photo;
		$scope.getActivity();
		$scope.offset = $scope.sliceSize;
	};
	
	
	$scope.getGeoScopedActivityType = function(scope, type){
		$scope.activityType = '/geo/'+scope + '/' + type;
		$scope.getActivity();
		$scope.offset = $scope.sliceSize;
	};
	
	$scope.getMeetingActivity = function(scope){
		$scope.oldActivityType = $scope.activityType;
		$scope.activityType = '/geomeetings/'+scope;
		$scope.rightAlertMsg = ''
		$scope.meetingsLoading = true;
		console.log($scope.activityType);
		$http.get('/getSiteActivity' + $scope.activityType).success(function(data){
			if (data.statusCode == 1){
				$scope.rightAlertMsg = data.alertMsg;
				$scope.rightAlertType = data.alertType;
			} 
			else if (data.statusCode === 0){
				$scope.meetings = data.result;
				
			}
			$scope.meetingsLoading = false;
			$scope.activityType = $scope.oldActivityType;
		})
	};

	$scope.browseInitiatives = function(){
		$scope.activityType = '/initiatives';
		$scope.getActivity();
		$scope.offset = $scope.sliceSize;
	};

	$scope.getActivitySlice = function() {
		console.log("Hiya!");
		if ($scope.busy || $scope.noMoreSlices) return;
		$scope.busy = true;
		$scope.alertMsg = ''
		$scope.activitySliceLoading = true;
		console.log('/getActivitySlice/0' + $scope.activityType + '/' + $scope.offset);
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

	$scope.geoInit = function(scope){	
		console.log("I'm here");
		$scope.activity = null;
		$scope.activityType = '/geo/'+scope;
		$scope.isGeoInit = true;
		$scope.currentScope = scope;
		$scope.getActivity();
	};
	
	$scope.showOnly = function(type){
		if (type === 'all') {
/*
			$scope.showConditional = false;
			$scope.showConditionalType = "";
*/
			$scope.activityType = '/geo/'+$scope.currentScope;
			$scope.getActivity();
		} 
		else if (type === 'initiative') {
			$scope.browseInitiatives();	
		} 
		else {
			$scope.getGeoScopedActivityType($scope.currentScope, type);
/*	
			$scope.showConditional = true;
			$scope.showConditionalType = type;	
*/
		}
	};

}


