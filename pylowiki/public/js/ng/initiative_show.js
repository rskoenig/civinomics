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
            //var inSessionGetter = $parse(attrs.userInSession);
            //console.log("inSessionGetter: " + inSessionGetter);
            //var followingGetter = $parse(attrs.following);
            //console.log("followingGetter: " + followingGetter);
            //var objCodeGetter = $parse(attrs.objCode);
            //console.log("objCodeGetter: " + objCodeGetter);
            //var objUrlGetter = $parse(attrs.objUrl);
            //console.log("objUrlGetter: " + objUrlGetter);
            return function (scope, element, attrs) {
                //var inSession = inSessionGetter(scope);
                var inSession = scope.initiativeData.user.uSession;
                console.log("inSession: " + inSession);
                //var objCode = objCodeGetter(scope);
                var objCode = scope.initiativeData.initiative.urlCode;
                console.log("objCode: " + objCode);
                //var objUrl = objUrlGetter(scope);
                var objUrl = scope.initiativeData.initiative.url;
                console.log("objUrl: " + objUrl);
                var isFollowingClass = (scope.initiativeData.user.isFollowing) ? " following" : "";
                var isFollowingText = (scope.initiativeData.user.isFollowing) ? "Following" : "Follow";
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