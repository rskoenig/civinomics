function activityController($scope, $http) {
	$scope.listingType = 'activity';

	if ($scope.activityType == undefined) {
	    $scope.activityType = 'all';
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
		if ($scope.code){
	        $scope.activityUrl = '/getObjActivity/' + $scope.activityType + '/' + $scope.code + '/' + $scope.url
	    }else{
	    	$scope.activityUrl = '/getSiteActivity/' + $scope.activityType;
	    }
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

        
    $scope.getActivity(); 

	$scope.geoScope = '';
	$scope.geoFlagUrl = '/images/flags/homeFlag.gif';
	$scope.geoPopulation = '';

	$scope.getAllActivity = function(){
		$scope.geoScope = '';
		$scope.activityType = 'all';
		$scope.geoFlagUrl = '/images/flags/homeFlag.gif';
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
	
	$scope.getGeoScopedActivity = function(scope, name, url, population, href, photo){
		$scope.activityType = 'geo/'+ scope;
		$scope.geoScope = scope;
		$scope.geoScopeName = name;
		$scope.geoFlagUrl = url;
		$scope.geoPopulation = population;
		$scope.geoHref = href;
		$scope.geoPhoto = photo;
		$scope.getActivity();
		$scope.offset = $scope.sliceSize;
	};
	
	$scope.getMeetingActivity = function(){
		$scope.activityType = 'meetings';
		$scope.getActivity();
		$scope.offset = $scope.sliceSize;
	};

	$scope.getMemberActivity = function(){
		$scope.activityType = 'member';
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
		    $scope.sliceUrl = '/getObjActivitySlice/0/' + $scope.activityType + '/' + $scope.code + '/' + $scope.url + '/' + $scope.offset;
		}else{
		    $scope.sliceUrl = '/getActivitySlice/0/' + $scope.activityType + '/' + $scope.offset;
		}
		$http.get($scope.sliceUrl).success(function(data){
			if (data.statusCode == 1){
				$scope.noMoreSlices = true;
				$scope.alertMsg = data.alertMsg;
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
			console.log($scope.offset);
		})
	};
}


