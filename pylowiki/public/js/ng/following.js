function followCtrl($scope, $http) {
	$scope.followLoading = true;
	$scope.followSliceLoading = false;
	$scope.noMoreFollowSlices = false;
	$scope.followBusy = false;
	$scope.sliceSize = 10
	$scope.offset = 0
	$scope.limit = $scope.offset + $scope.sliceSize
	$scope.followLookupURL = '/getFollowInitiatives/' + $scope.offset + '/' + $scope.limit

	$scope.getFollowing = function() {
	console.log("In get following");
	console.log($scope.followBusy);
		console.log($scope.noMoreFollowSlices);
		console.log($scope.noFollowingResult);
				console.log("Yep");

		$scope.followLoading = true;
		console.log($scope.followLookupURL);
		$http.get($scope.followLookupURL).success(function(data){
			console.log("alive");
			if (data.statusCode == 1){
			console.log("alive1");
				$scope.noFollowingResult = true;
			}
			else if (data.statusCode === 0){
			console.log("alive2");
				$scope.noFollowingResult = false;
				$scope.followInitiatives = data.result;
				console.log(data.result);
			}
			console.log("alive3");
			$scope.followLoading = false;
			$scope.offset += $scope.sliceSize
			$scope.limit += $scope.sliceSize
		});
	}

	$scope.getFollowing()

	$scope.getFollowSlice = function() {
		if ($scope.followBusy || $scope.noMoreFollowSlices || $scope.noFollowingResult) return;
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
		if ($scope.followBusy || $scope.noMoreFollowSlices || $scope.noFollowingResult) return;
		console.log("In getFollowingGeo");
		$scope.followBusy = true;
		$scope.followAlertMsg = '';
		$scope.followSliceLoading = true;
		$scope.followLookupURL = '/getFollowInitiatives/geo/' + $scope.offset + '/' + $scope.limit + '/' + scope;
		console.log($scope.followLookupURL);
		$scope.getFollowing();
	};
	
	$scope.$watch(
		'geoScope',
		function(newValue, oldValue){
			if (!(newValue === oldValue)) { 
				/*Does this actually work?*/
				console.log("There has been a change in the scope");
				$scope.sliceSize = 10;
				$scope.offset = 0;
				$scope.limit = $scope.offset + $scope.sliceSize;
				$scope.getFollowingGeo(newValue);
				/*Do stuff.
				We have to change whatever's in followInitiatives with whatever we get
				*/
					
			};
		}
	);

}