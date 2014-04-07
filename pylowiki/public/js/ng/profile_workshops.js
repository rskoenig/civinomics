function profileWorkshopsCtrl($scope, $http) {

    $scope.getWorkshopStats = function() {
        $scope.alertMsg = '';
        $scope.workshopDataLoading = true;
        $http.get('/workshop/' + $scope.code + '/' + $scope.url + '/' + '/publicStats?json=1').success(function(data){

            if (data.statusCode == 1){
                //console.log('data.statusCode == 1');
                $scope.statsNoResult = true;
                $scope.stats = []
                $scope.alertMsg = data.alertMsg;
                $scope.alertType = data.alertType;
            } 
            else if (data.statusCode === 0){
                //console.log('data.statusCode == 0');
                $scope.statsNoResult = false;
                $scope.stats = data.result;
                console.log($scope.stats);
            }
            $scope.workshopDataLoading = false;
        })
    };    

}