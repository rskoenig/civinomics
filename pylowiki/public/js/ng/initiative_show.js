var app = angular.module('civ', []);

app.controller('showInitiativeController', function($scope, $http){
//function showInitiativeController($scope, $http) {
    
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

//}
});

app.directive("myWatchButton", function($compile, $parse) {
    return { 
        restrict: 'E', 
        compile: function(element, attrs) {
            var inSessionGetter = $parse(attrs.userInSession);
            var followingGetter = $parse(attrs.following);
            var objCodeGetter = $parse(attrs.objCode);
            var objUrlGetter = $parse(attrs.objUrl);

            return function (scope, element, attrs) {
                var inSession = inSessionGetter(scope);
                console.log("inSession: " + inSession);
                var following = followingGetter(scope);
                console.log("following: " + following);
                var objCode = objCodeGetter(scope);
                console.log("objCode: " + objCode);
                var objUrl = objUrlGetter(scope);
                var isFollowingClass = (following) ? " following" : "";
                var isFollowingText = (following) ? "Following" : "Follow";
                var template = (inSession) ? '<button class="btn btn-civ pull-right followButton' + isFollowingClass + '"' +
                        'data-URL-list="initiative_' + objCode + '_' + objUrl + '" rel="tooltip"' +
                        'data-placement="bottom" data-original-title="this initiative" id="initiativeBookmark">' +
                        '<span><i class="icon-bookmark btn-height icon-light"></i><strong>' +
                        isFollowingText + '</strong></span></button>' : '';
                element.replaceWith($compile(template)(scope));
            }
        }
    }
});