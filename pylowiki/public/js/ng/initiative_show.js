var app = angular.module('civ', []);

app.controller('showInitiativeController', function($scope, $http){
    
    function isFollowingClass(isFollowing) {
        return (isFollowing) ? " following" : "";
    }
    function isFollowingText(isFollowing) {
        return (isFollowing) ? "Following" : "Follow";
    }

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
                $scope.initiativeNoResult = false;
                $scope.initiativeData = data.result;
                $scope.followButtonDisabled = ($scope.initiativeData.user.uSession) ? false : true;
                $scope.followButtonClass = isFollowingClass($scope.initiativeData.user.isFollowing);
                $scope.followButtonText = isFollowingText($scope.initiativeData.user.isFollowing);
                $scope.iPrivsNoiHomeYesiObjTypeNoRev = false;
                if (!$scope.initiativeData.initiative.iPrivs && $scope.initiativeData.initiative.home && $scope.initiativeData.initiative.objType != 'revision') {
                    $scope.iPrivsNoiHomeYesiObjTypeNoRev = true;
                }
                $scope.editInitNoObjTypeNoRev = false;
                if (!$scope.initiativeData.initiative.editInitiative && $scope.initiativeData.initiative.objType != 'revision') {
                    $scope.editInitNoObjTypeNoRev = true;
                }
                $scope.editInitNoObjTypeNoRevElse = false;
                if (!$scope.initiativeData.initiative.editInitiative && !$scope.editInitNoObjTypeNoRev) {
                    $scope.editInitNoObjTypeNoRevElse = true;
                }
                $scope.iPrivsEditInitObjTypeNoUnpub = false;
                if ($scope.initiativeData.initiative.iPrivs && $scope.initiativeData.initiative.editInitiative && $scope.initiativeData.initiative.objType != 'initiativeUnpublished') {
                    $scope.iPrivsEditInitObjTypeNoUnpub = true;
                }
                $scope.iLastNoEditNoObjTypeInit = false;
                if (!$scope.iPrivsEditInitObjTypeNoUnpub && !$scope.initiativeData.initiative.editInitiative && $scope.initiativeData.initiative.objType != 'initiative') {
                    $scope.iLastNoEditNoObjTypeInit = true;
                }
                $scope.initPubNoComplete = false;
                if ($scope.initiativeData.initiative.public == '0' && $scope.initiativeData.complete) {
                    $scope.initPubNoComplete = true;
                }
                $scope.iLastNoPubNo = false;
                if (!$scope.initPubNoComplete && $scope.initiativeData.initiative.public == '0') {
                    $scope.iLastNoPubNo = true;
                }
                $scope.iLastTwoNo = false;
                if (!$scope.initPubNoComplete && !$scope.iLastNoPubNo) {
                    $scope.iLastTwoNo = true;
                }
                $scope.emailSubject = 'Vote on "' + $scope.initiativeData.initiative.title  + '"';
                $scope.emailBody = $scope.initiativeData.initiative.link;

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

    $scope.follow_unfollowURL = '/initiative/' + $scope.code + '/' + $scope.url + '/follow/handler'
    $scope.followPushed = function(){
        $scope.followButtonDisabled = true
        $http.post($scope.follow_unfollowURL).success(function(data){
            // toggle the follow state and load new class/text for the button
            $scope.initiativeData.user.isFollowing = !$scope.initiativeData.user.isFollowing;
            $scope.followButtonClass = isFollowingClass($scope.initiativeData.user.isFollowing);
            $scope.followButtonText = isFollowingText($scope.initiativeData.user.isFollowing);
            $scope.followButtonDisabled = false
        });
    };

});