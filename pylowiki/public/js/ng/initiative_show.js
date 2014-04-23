function showInitiativeController($scope, $http) {
    
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

}