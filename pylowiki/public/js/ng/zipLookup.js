function zipLookupCtrl($scope, $http) {
	$scope.loading = true;
	$scope.zipValueRegex = /^\d{5}$/;
	$scope.zipValue = '95060';
	$scope.zipLookupURL = '/zip/lookup/' + $scope.zipValue;
	$http.get($scope.zipLookupURL).success(function(data){
		if (data.statusCode == 1){
			$scope.noResult = true;
		}
		else if (data.statusCode === 0){
			$scope.noResult = false;
			$scope.geos = data.result;
		}
		$scope.loading = false;
	});

	$scope.lookup = function() {
		$scope.loading = true;
		$scope.zipLookupURL = '/zip/lookup/' + $scope.zipValue;
		$http.get($scope.zipLookupURL).success(function(data){
			if (data.statusCode == 1){
				$scope.noResult = true;
			}
			else if (data.statusCode === 0){
				$scope.noResult = false;
				$scope.geos = data.result;
			}
			$scope.loading = false;
		});
	}

}