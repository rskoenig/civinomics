function signupController($scope) {
    $scope.word = /^\d{5}/;
    $scope.email = 'me@example.com';
    
    $scope.clearEmail = function() {
        $scope.email = '';
    }
}