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
                //console.log(data.result);
                $scope.initiativeNoResult = false;
                $scope.initiativeData = data.result;
                if ($scope.initiativeData.initiative.iPrivs != 'True' && $scope.initiativeData.initiative.home == 'True' && $scope.initiativeData.initiative.objType != 'revision') {
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

}