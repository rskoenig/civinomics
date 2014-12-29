function positionsCtrl($scope, $http) {
  
    $scope.getPositionsUrl = '/getProCons/' + $scope.code
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
    $scope.notFlagged = true;
    
    $scope.flag = function(urlCode){
        var url = "/flag/comment/" + urlCode;
        $http.get(url).success(
            function (data) {
                $scope.resultFlag = data.result;
                $scope.notFlagged = false;
            }
        );
    }

    $scope.checkingMadeStatement = true
    $scope.userStatement = {}
    $scope.userStatement.madeStatement = false

    $scope.getPositions()

};