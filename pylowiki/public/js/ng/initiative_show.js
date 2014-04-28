var app = angular.module('civ', []);

app.controller('showInitiativeController', function($scope, $http){
    
    console.log('in showInitiativeController');
    $scope.initiativeLoading = true;

    $scope.getInitiative = function() {
        $scope.alertMsg = '';
        $scope.initiativeLoading = true;
        $http.get('/initiative/' + $scope.code + '/' + $scope.url + '/get').success(function(data){
            if (data.statusCode == 1){
                //console.log('data.statusCode == 1');
                $scope.initiativeNoResult = true;
                $scope.initiative = []
                $scope.alertMsg = data.alertMsg;
                $scope.alertType = data.alertType;
            } 
            else if (data.statusCode === 0){
                console.log(data.result);
                $scope.initiativeNoResult = false;
                $scope.initiativeData = data.result;
                $scope.followButtonDisabled = ($scope.initiativeData.user.uSession) ? false : true;
                $scope.followButtonClass = isFollowingClass($scope.initiativeData.user.isFollowing);
                $scope.followButtonText = isFollowingText($scope.initiativeData.user.isFollowing);
                if (!$scope.initiativeData.initiative.iPrivs && $scope.initiativeData.initiative.home && $scope.initiativeData.initiative.objType != 'revision') {
                    $scope.iPrivsNoiHomeYesiOnjTypeNo = true
                } else {
                    $scope.iPrivsNoiHomeYesiOnjTypeNo = false
                }    
            } else if (data.statusCode === 2){
                //console.log('data.statusCode == 2');
                $scope.initiativeNoResult = true;
                $scope.initiative = []
                $scope.alertMsg = data.alertMsg;
                $scope.alertType = data.alertType;
            }
            $scope.initiativeLoading = false;
        })
    };

    $scope.getInitiative();

    function isFollowingClass(isFollowing) {
        return (isFollowing) ? " following" : "";
    }
    function isFollowingText(isFollowing) {
        return (isFollowing) ? "Following" : "Follow";
    }

    $scope.follow_unfollowURL = '/initiative/' + $scope.code + '/' + $scope.url + '/follow/handler'
    $scope.followPushed = function(){
        $scope.followButtonDisabled = true
        $http.post($scope.follow_unfollowURL).success(function(data){
            // toggle class and text for follow button
            $scope.initiativeData.user.isFollowing = !$scope.initiativeData.user.isFollowing;
            $scope.followButtonClass = isFollowingClass($scope.initiativeData.user.isFollowing);
            $scope.followButtonText = isFollowingText($scope.initiativeData.user.isFollowing);
            $scope.followButtonDisabled = false
        });
    };

});