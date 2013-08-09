function photoUploadController($scope) {
    
    $scope.validateForm = function() {
        document.getElementById('photoUploadResult').innerHTML = 'Got ' + $scope.userCode + " and " + $scope.userURL;
    };
}