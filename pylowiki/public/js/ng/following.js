function followCtrl($scope, $http) {
	$scope.followLoading = true;
	$scope.followSliceLoading = false;
	$scope.noMoreFollowSlices = false;
	$scope.followBusy = false;
	$scope.sliceSize = 10
	$scope.offset = 0
	$scope.limit = $scope.offset + $scope.sliceSize
	$scope.followLookupURL = '/getFollowInitiatives/' + $scope.offset + '/' + $scope.limit

	$scope.getFollow = function() {
		$scope.followLoading = true;
		$http.get($scope.followLookupURL).success(function(data){
			if (data.statusCode == 1){
				$scope.noResult = true;
			}
			else if (data.statusCode === 0){
				$scope.noResult = false;
				$scope.followInitiatives = data.result;
			}
			$scope.followLoading = false;
			$scope.offset += $scope.sliceSize
			$scope.limit += $scope.sliceSize
		});
	}

	$scope.getFollow()

	$scope.getFollowSlice = function() {
		if ($scope.followBusy || $scope.noMoreFollowSlices) return;
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

}