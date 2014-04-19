
function shareController($scope, $http, $location, $timeout) {
    $scope.shareEmailShow     = false;
    
    $scope.shareEmail = function() {
        var shareURL = '/workshop/' + $scope.code + '/' + $scope.url + '/share/' + $scope.user + '/email/handler';
        var postData = {'itemURL':$scope.itemURL, 'itemCode':$scope.itemCode, 'recipientEmail':$scope.recipientEmail, 'memberMessage':$scope.memberMessage};
        $http.post(shareURL, postData).success(function(data){
            $scope.shareEmailShow = true;
            $scope.shareEmailResponse = data;
            $scope.recipientName = '';
            $scope.recipientEmail = '';
            $scope.memberMessage = 'I thought this might interest you!';
            var t = $timeout( function() { 
                $scope.shareEmailResponse = '';
                $scope.shareEmailShow = false;
            }, 8000);

        });
    };
}
