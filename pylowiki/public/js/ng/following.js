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
		console.log("In get following");
		$scope.followLoading = true;
		console.log($scope.followLookupURL);
		$http.get($scope.followLookupURL).success(function(data){
			if (data.statusCode == 1){
				$scope.noFollowingResult = true;
			}
			else if (data.statusCode === 0){
			console.log("alive2");
				$scope.noFollowingResult = false;
				$scope.followInitiatives = data.result;
				console.log(data.result);
			}
			$scope.followLoading = false;
			$scope.offset += $scope.sliceSize
			$scope.limit += $scope.sliceSize
		});
	}

	$scope.getFollowing()

	$scope.getFollowSlice = function() {
		console.log("in get follow slice");
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
				if (newValue === ""){
					console.log("Back to default");
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
					$scope.followingGeo = true;
					/*Do I really need all this?*/
					console.log("There has been a change in the scope");
					console.log(newValue)
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