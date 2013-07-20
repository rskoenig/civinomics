
function shareController($scope, $http, $location) {
    $scope.shareEmailShow     = false;
    
    $scope.shareEmail = function() {
        var emailURL = '/workshop/' + $scope.code + '/' + $scope.url + '/share/' + $scope.user + '/email/handler';
        var postData = {'urlCode':$scope.itemURL, 'memberMessage':$scope.memberMessage};
        $http.post(emailURL, postData).success(function(data){
            $scope.shareEmailShow = true;
            $scope.shareEmailResponse = data;
        });
    };
}
  
