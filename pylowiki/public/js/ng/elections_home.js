function electionsHomeController($scope, $http) {
    var getElectionsURL = '/getElectionsForPostalCode/' + $scope.postalCode;

	$scope.getElections = function() {
		$scope.electionLoading = true;
		$http.get(getElectionsURL).success(function(data){
			if (data.statusCode == 1){
				$scope.noElectionResult = true;
			}
			else if (data.statusCode === 0){
				$scope.noElectionResult = false;
				$scope.elections = data.result;
			}
			$scope.electionLoading = false;
		});
	}

	$scope.getElections()
}

