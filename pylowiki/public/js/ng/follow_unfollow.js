function follow_unfollowCtrl($scope, $http) {
    $scope.following = true
    $scope.follow_unfollowURL = '/initiative/' + $scope.code + '/' + $scope.url + '/follow/handler'
    
    $scope.changeFollow = function(){
        $http.post($scope.follow_unfollowURL).success(function(){
            $scope.following = !$scope.following
        });
    };
    
}