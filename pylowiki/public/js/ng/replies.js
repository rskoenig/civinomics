
var app = angular.module('civ', ['ngSanitize', 'infinite-scroll']);

app.factory('editService', function ($rootScope) {
    var commentEdit = {};
 
    commentEdit.prepBroadcast = function() {
        this.sendBroadcast();
    };   
    commentEdit.sendBroadcast = function() {
        $rootScope.$broadcast('editDone');
    };
    
    return commentEdit;
});

app.controller('RepliesController', ['$scope', '$http', function($scope, $http) {
    console.log("this is a controller");
    $scope.showReplies = false;
    $scope.loading = false;
        
    $scope.getReplies = function(item){
        $scope.loading = true;
        var url = "/getReplies/"+ item.urlCode;
        $http.get(url).success(
            function (data) {
                $scope.loading = false;
                $scope.replyList = data.replies;  
            }
        );
    };

    $scope.toggleReplies = function(item){ 
        $scope.showReplies = !$scope.showReplies;  
        if ($scope.showReplies){
            $scope.getReplies(item);
        };
    };
}]);