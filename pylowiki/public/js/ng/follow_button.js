app.controller('followButtonCtrl', function($scope, $http){
    
    function isFollowingClass(isFollowing) {
        return (isFollowing) ? " following" : "";
    }
    function isFollowingText(isFollowing) {
        return (isFollowing) ? "Following" : "Follow";
    }

    $scope.initializeFollowButton = function() {
        console.log('huh');
        $scope.followButtonClass = isFollowingClass($scope.isFollowing);
        $scope.followButtonText = isFollowingText($scope.isFollowing);
    };

    $scope.initializeFollowButton();

    $scope.follow_unfollowURL = '/initiative/' + $scope.code + '/' + $scope.url + '/follow/handler'
    $scope.followPushed = function(){
        $scope.followButtonDisabled = true
        $http.post($scope.follow_unfollowURL).success(function(data){
            // toggle the follow state and load new class/text for the button
            $scope.isFollowing = !$scope.isFollowing;
            $scope.followButtonClass = isFollowingClass($scope.isFollowing);
            $scope.followButtonText = isFollowingText($scope.isFollowing);
            $scope.followButtonDisabled = false
        });
    };

};