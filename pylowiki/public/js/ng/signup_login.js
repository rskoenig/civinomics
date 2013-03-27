function signupController($scope) {
    $scope.postalCodeRegex = /^\d{5}$/;
    $scope.fullNameRegex = /^([A-Za-z0-9-_\s])+$/;
    $scope.email = 'me@example.com';
    
    $scope.clearEmail = function() {
        $scope.email = '';
    }
}