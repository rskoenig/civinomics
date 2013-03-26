function SearchCtrl($scope, $http) {
    $scope.workshopsURL = '/search/workshops'
    $scope.searchQuery = window.location.search
    
    $http.get($scope.workshopsURL + $scope.searchQuery).success(function(data){
        $scope.workshops = data;
        $scope.showingWorkshops = true;
    })
    
    $scope.searchWorkshops = function() {
        $http.get($scope.workshopsURL + $scope.searchQuery).success(function(data){
            $scope.workshops = data;
            $scope.showingWorkshops = true;
        })
    }
}