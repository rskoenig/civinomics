function positionsCtrl($scope, $http) {
  
    $scope.objType = 'initiative'
    $scope.getPositionsUrl = '/getPositions/' + $scope.objType + '/' + $scope.code
    $scope.getPositions = function(){
        $scope.positionsLoading = true;
        $http.get($scope.getPositionsUrl).success(function(data){
            $scope.support = data.support
            $scope.oppose = data.oppose
            $scope.positionsLoading = false;
        });
    }
    
    $scope.getPositions()
    
};