function followingCtrl($scope, $http) {
	$scope.followLoading = true;
	$scope.followingLookupURL = '/getFollowingInitiatives'

	$scope.getFollowing = function() {
		$scope.followLoading = true;
		$http.get($scope.followingLookupURL).success(function(data){
			if (data.statusCode == 1){
				$scope.noResult = true;
			}
			else if (data.statusCode === 0){
				$scope.noResult = false;
				$scope.followingInitiatives = data.result;
			}
			$scope.followLoading = false;
		});
	}

	$scope.getFollowing()

}