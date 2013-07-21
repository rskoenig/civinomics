
function shareController($scope, $http, $location) {
    $scope.shareEmailShow     = false;
    
    $scope.shareEmail = function() {
        var shareURL = '/workshop/' + $scope.code + '/' + $scope.url + '/share/' + $scope.user + '/email/handler';
        var postData = {'itemURL':$scope.itemURL, 'itemCode':$scope.itemCode, 'recipientName':$scope.recipientName, 'recipientEmail':$scope.recipientEmail, 'memberMessage':$scope.memberMessage};
        $http.post(shareURL, postData).success(function(data){
            $scope.shareEmailShow = true;
            $scope.shareEmailResponse = data;
        });
    };
}
