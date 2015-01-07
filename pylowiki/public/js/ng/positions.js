function positionsCtrl($scope, $http) {
  
    $scope.getPositionsUrl = '/getProCons/' + $scope.code;
    $scope.checkingMadeStatement = true;
    $scope.userStatement = {};
    $scope.userStatement.madeStatement = false;
    
    $scope.getPositions = function(){
        $scope.positionsLoading = true;
        $http.get($scope.getPositionsUrl).success(function(data){
            $scope.support = data.pros
            $scope.oppose = data.cons
            $scope.positionsLoading = false;

            $scope.userStatement = data.userStatement;
            $scope.checkingMadeStatement = false;

        });
    }    
    
    $scope.flag = function(item){
        var url = "/flag/comment/" + item.urlCode;
        $http.get(url).success(
            function (data) {
                item.resultFlag = data.result;
                item.notFlagged = false;
            }
        );
    };
    
    $scope.getReplies = function(){
        $scope.item.loading = true;
        var url = "/getReplies/"+ $scope.item.urlCode;
        $http.get(url).success(
            function (data) {
                console.log(data);
                $scope.item.loading = false;
                $scope.item.replyList = data.replies;  
            }
        );
    };

    $scope.toggleReplies = function(item){ 
        if (typeof $scope.item.showReplies === 'undefined') {
            $scope.item = item;
            $scope.item.showReplies = false;
            $scope.item.loading = false;
        };
        $scope.item.showReplies = !$scope.item.showReplies;  
        if ($scope.item.showReplies && item.replies.length != 0){
            $scope.getReplies();
        };
    
    };

    
    $scope.getPositions()

};