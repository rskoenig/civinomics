function zipLookupCtrl($scope, $http) {
	$scope.loading = true;
	$scope.zipValueRegex = /^\d{5}$/;

	// if user in session, use ng-init to default to their zip code otherwise, default to 95060
	if (!$scope.zipValue){
		$scope.zipValue= '95060';
	}

	// for flipboard style layout
	if ($scope.photos){
		$scope.zipLookupURL = '/zip/lookup/' + $scope.zipValue + '/photos';
	} else{
		$scope.zipLookupURL = '/zip/lookup/' + $scope.zipValue; 
	}
	
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