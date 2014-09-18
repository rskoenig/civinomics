function positionsCtrl($scope, $http) {
  
    $scope.getPositionsUrl = '/getPositions/' + $scope.objType + '/' + $scope.code
    $scope.getPositions = function(){
        $scope.positionsLoading = true;
        $http.get($scope.getPositionsUrl).success(function(data){
            $scope.support = data.support
            $scope.oppose = data.oppose
            $scope.positionsLoading = false;

            $scope.userStatement = data.userStatement;
            $scope.checkingMadeStatement = false;

        });
    }

    $scope.checkingMadeStatement = true
    $scope.userStatement = {}
    $scope.userStatement.madeStatement = false

    $scope.getPositions()

};