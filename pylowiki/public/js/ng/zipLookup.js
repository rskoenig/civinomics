function testCtrl($scope, $http) {
	$scope.test2 = "testing testing 3 2 1 4";
	$scope.zipValue = '95076';
	$scope.zipLookupURL = '/zip/lookup/' + $scope.zipValue;
	$http.get($scope.zipLookupURL).success(function(data){
		if (data.statusCode == 1){
			$scope.noResult = true;
		}
		else if (data.statusCode === 0){
			$scope.noResult = false;
			$scope.geos = data.result;
		}
	});

	$scope.lookup = function() {
		$scope.zipLookupURL = '/zip/lookup/' + $scope.zipValue;
		$http.get($scope.zipLookupURL).success(function(data){
			if (data.statusCode == 1){
				$scope.noResult = true;
			}
			else if (data.statusCode === 0){
				$scope.noResult = false;
				$scope.geos = data.result;
			}
		});
	}

}