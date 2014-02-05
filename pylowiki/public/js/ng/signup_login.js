function signupController($scope) {
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
}