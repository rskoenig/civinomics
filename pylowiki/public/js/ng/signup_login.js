function signupController($scope, $http) {
    $scope.postalCodeRegex = /^\d{5}$/;
    $scope.fullNameRegex = /^([A-Za-z0-9-_\s])+$/;
    $scope.email = '';
    
    $scope.clearEmail = function() {
        $scope.email = '';
    };
    $scope.switchLoginTitle = function(){
    	$scope.showTitle = 'lTitle'
    }
    $scope.switchSignupTitle = function(){
    	$scope.showTitle = 'sTitle'
    }
    $scope.switchPasswordTitle = function(){
    	$scope.showTitle = 'pTitle'
    }
	$scope.lookup = function() {
		$scope.loading = true;
		$scope.zipLookupURL = '/zip/lookup/' + $scope.postalCode; 

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