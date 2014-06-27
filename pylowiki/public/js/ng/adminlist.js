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

	$scope.sliceSize = 10;
	$scope.offset=0;
	$scope.activityLoading = false;
	$scope.list = [];
	$scope.activityType = '/users';

	$scope.getActivity = function() {
		if ($scope.activityLoading) return;
		$scope.activityLoading = true;
		alert('/getAdminList' + $scope.activityType + '/' + $scope.offset);
		$http.get('/getAdminList' + $scope.activityType + '/' + $scope.offset).success(function(data){	
	      var items = data.result;
	      for (var i = 0; i < items.length; i++) {
	        $scope.list.push(items[i].data);
	      }
	      $scope.offset = items.length;
	      $scope.activityLoading = false;
		})
	};
}