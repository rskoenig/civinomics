function follow_unfollowCtrl($scope, $http) {
    $scope.following = true
    $scope.trashed = false
    $scope.follow_unfollowURL = '/initiative/' + $scope.code + '/' + $scope.url + '/follow/handler'
    $scope.trashURL = '/trash/' + $scope.code + '/' + $scope.url
    
    $scope.changeFollow = function(){
        $http.post($scope.follow_unfollowURL).success(function(){
            $scope.following = !$scope.following
        });
    };
    
    $scope.trashThing = function(){
        $http.post($scope.trashURL).success(function(){
            $scope.trashed = !$scope.trashed
        });
    };
    
}