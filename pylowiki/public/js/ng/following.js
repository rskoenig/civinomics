function followCtrl($scope, $http) {
	$scope.followLoading = true;
	$scope.followSliceLoading = false;
	$scope.noMoreFollowSlices = false;
	$scope.followBusy = false;
	$scope.followingGeo = false;
	$scope.sliceSize = 10
	$scope.offset = 0
	$scope.limit = $scope.offset + $scope.sliceSize
	$scope.followLookupURL = '/getFollowInitiatives/' + $scope.offset + '/' + $scope.limit

	$scope.getFollowing = function() {
		$scope.followLoading = true;
		$http.get($scope.followLookupURL).success(function(data){
			if (data.statusCode == 1){
				$scope.noFollowingResult = true;
			}
			else if (data.statusCode === 0){
				$scope.noFollowingResult = false;
				$scope.followInitiatives = data.result;
			}
			$scope.followLoading = false;
			$scope.offset += $scope.sliceSize
			$scope.limit += $scope.sliceSize
		});
	}

	$scope.getFollowing()

	$scope.getFollowSlice = function() {
		if ($scope.followBusy || $scope.noMoreFollowSlices || $scope.noFollowingResult || $scope.followingGeo) return;
		$scope.followBusy = true;
		$scope.followAlertMsg = ''
		$scope.followSliceLoading = true;
		$http.get('/getFollowInitiatives/' + $scope.offset + '/' + $scope.limit).success(function(data){
			if (data.statusCode == 1){
				$scope.noMoreFollowSlices = true;
			} 
			else if (data.statusCode === 0){
				followSlice = data.result;
				for (var i = 0; i < followSlice.length; i++) {
				    $scope.followInitiatives.push(followSlice[i]);
				}
				$scope.noMoreFollowSlices = false;
			}
			$scope.followSliceLoading = false;
			$scope.followBusy = false;
			$scope.offset += $scope.sliceSize
			$scope.limit += $scope.sliceSize
		})
	};
	
	$scope.getFollowingGeo = function(scope){
		if ($scope.followBusy) return;
		$scope.followBusy = true;
		$scope.followAlertMsg = '';
		$scope.followSliceLoading = true;
		$scope.followLookupURL = '/getFollowInitiatives/geo/' + $scope.offset + '/' + $scope.limit + '/' + scope;
		$scope.getFollowing();
	};
	
	$scope.$watch(
		'geoScope',
		function(newValue, oldValue){
			if (!(newValue === oldValue)) { 
			$scope.followAlertMsg = '';
				if (newValue === ""){
					$scope.followAlertMsg = '';
					$scope.followingGeo = false;
					$scope.followInitiatives = null;
					$scope.followLoading = true;
					$scope.followSliceLoading = false;
					$scope.noMoreFollowSlices = false;
					$scope.followBusy = false;
					$scope.sliceSize = 10;
					$scope.offset = 0;
					$scope.limit = $scope.offset + $scope.sliceSize;
					$scope.followLookupURL = '/getFollowInitiatives/' + $scope.offset + '/' + $scope.limit
					$scope.getFollowing();
				}
				else{
					$scope.followAlertMsg = '';
					$scope.followingGeo = true;
					/*Do I really need all this?*/
					$scope.followInitiatives = null;
					$scope.followLoading = true;
					$scope.followSliceLoading = false;
					$scope.noMoreFollowSlices = false;
					$scope.followBusy = false;
					$scope.sliceSize = 10;
					$scope.offset = 0;
					$scope.limit = $scope.offset + $scope.sliceSize;
					$scope.getFollowingGeo(newValue);
					$scope.followSliceLoading = false;
					$scope.followBusy = false;
					/*Do stuff.
					We have to change whatever's in followInitiatives with whatever we get
					*/
				};
					
			};
		}
	);

}